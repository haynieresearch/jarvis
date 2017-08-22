#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2013, Jeff Terrace
# All rights reserved.

"""Authentication routines to connect to Logitech web service and Harmony devices."""

import logging
import re
import sleekxmpp

from sleekxmpp.xmlstream import ET

logger = logging.getLogger(__name__)


class AuthToken(sleekxmpp.ClientXMPP):
    """An XMPP client for swapping a Login Token for a Session Token.

    After the client finishes processing, the uuid attribute of the class will
    contain the session token.
    """

    def __init__(self):
        """Initializes the client."""
        plugin_config = {
            # Enables PLAIN authentication which is off by default.
            'feature_mechanisms': {'unencrypted_plain': True},
        }
        super(AuthToken, self).__init__(
            'guest@connect.logitech.com/gatorade.', 'gatorade.', plugin_config=plugin_config)

        self.token = None
        self.uuid = None
        self.add_event_handler('session_start', self.session_start)

    def session_start(self, _):
        """Called when the XMPP session has been initialized."""
        iq_cmd = self.Iq()
        iq_cmd['type'] = 'get'
        action_cmd = ET.Element('oa')
        action_cmd.attrib['xmlns'] = 'connect.logitech.com'
        action_cmd.attrib['mime'] = 'vnd.logitech.connect/vnd.logitech.pair'
        action_cmd.text = 'token=%s:name=%s' % (self.token,
                                                'foo#iOS6.0.1#iPhone')
        iq_cmd.set_payload(action_cmd)
        result = iq_cmd.send(block=True)
        payload = result.get_payload()
        assert len(payload) == 1
        oa_resp = payload[0]
        assert oa_resp.attrib['errorcode'] == '200'
        match = re.search(r'identity=(?P<uuid>[\w-]+):status', oa_resp.text)
        assert match
        self.uuid = match.group('uuid')
        logger.info('Received UUID from device: %s', self.uuid)
        self.disconnect(send_close=False)


def get_auth_token(ip_address, port):
    """Swaps the Logitech auth token for a session token.

    Args:
        ip_address (str): IP Address of the Harmony device IP address
        port (str): Harmony device port

    Returns:
        A string containing the session token.
    """
    login_client = AuthToken()
    login_client.connect(address=(ip_address, port),use_tls=False, use_ssl=False)
    login_client.process(block=True)
    return login_client.uuid
