#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Client class for connecting to Logitech Harmony devices."""

import json
import time
import re
import sleekxmpp
from sleekxmpp.xmlstream import ET
from sleekxmpp.xmlstream.handler.callback import Callback
from sleekxmpp.xmlstream.matcher.base import MatcherBase
import logging

logger = logging.getLogger(__name__)

class HarmonyClient(sleekxmpp.ClientXMPP):
    """An XMPP client for connecting to the Logitech Harmony devices."""

    def __init__(self):
        user = 'user@connect.logitech.com/gatorade.'
        password = 'password'
        plugin_config = {
            # Enables PLAIN authentication which is off by default.
            'feature_mechanisms': {'unencrypted_plain': True},
        }
        super(HarmonyClient, self).__init__(
            user, password, plugin_config=plugin_config)

    def get_config(self):
        """Retrieves the Harmony device configuration.

        Returns:
            A nested dictionary containing activities, devices, etc.
        """
        iq_cmd = self.Iq()
        iq_cmd['type'] = 'get'
        action_cmd = ET.Element('oa')
        action_cmd.attrib['xmlns'] = 'connect.logitech.com'
        action_cmd.attrib['mime'] = (
            'vnd.logitech.harmony/vnd.logitech.harmony.engine?config')
        iq_cmd.set_payload(action_cmd)
        retries = 3
        attempt = 0

        for _ in range(retries):
            try:
                result = iq_cmd.send(block=True)
                break
            except Exception:
                logger.critical('XMPP timeout, reattempting')
                attempt += 1
                pass
        if attempt == 3:
            raise ValueError('XMPP timeout with hub')

        payload = result.get_payload()
        assert len(payload) == 1
        action_cmd = payload[0]
        assert action_cmd.attrib['errorcode'] == '200'
        device_list = action_cmd.text
        return json.loads(device_list)

    def get_current_activity(self):
        """Retrieves the current activity ID.

        Returns:
            A int with the current activity ID.
        """
        iq_cmd = self.Iq()
        iq_cmd['type'] = 'get'
        action_cmd = ET.Element('oa')
        action_cmd.attrib['xmlns'] = 'connect.logitech.com'
        action_cmd.attrib['mime'] = (
            'vnd.logitech.harmony/vnd.logitech.harmony.engine?getCurrentActivity')
        iq_cmd.set_payload(action_cmd)
        try:
            result = iq_cmd.send(block=True)
        except Exception:
            logger.info('XMPP timeout, reattempting')
            result = iq_cmd.send(block=True)
        payload = result.get_payload()
        assert len(payload) == 1
        action_cmd = payload[0]
        assert action_cmd.attrib['errorcode'] == '200'
        activity = action_cmd.text.split("=")
        return int(activity[1])

    def start_activity(self, activity_id):
        """Starts an activity.

        Args:
            activity_id: An int or string identifying the activity to start

        Returns:
            True if activity started, otherwise False
        """
        iq_cmd = self.Iq()
        iq_cmd['type'] = 'get'
        action_cmd = ET.Element('oa')
        action_cmd.attrib['xmlns'] = 'connect.logitech.com'
        action_cmd.attrib['mime'] = ('harmony.engine?startactivity')
        cmd = 'activityId=' + str(activity_id) + ':timestamp=0'
        action_cmd.text = cmd
        iq_cmd.set_payload(action_cmd)
        try:
            result = iq_cmd.send(block=True)
        except Exception:
            logger.info('XMPP timeout, reattempting')
            result = iq_cmd.send(block=True)
        payload = result.get_payload()
        assert len(payload) == 1
        action_cmd = payload[0]
        if action_cmd.text == None:
            return True
        else:
            return False

    def sync(self):
        """Syncs the harmony hub with the web service.
        """
        iq_cmd = self.Iq()
        iq_cmd['type'] = 'get'
        action_cmd = ET.Element('oa')
        action_cmd.attrib['xmlns'] = 'connect.logitech.com'
        action_cmd.attrib['mime'] = ('setup.sync')
        iq_cmd.set_payload(action_cmd)
        try:
            result = iq_cmd.send(block=True)
        except Exception:
            logger.info('XMPP timeout, reattempting')
            result = iq_cmd.send(block=True)
        payload = result.get_payload()
        assert len(payload) == 1

    def send_command(self, device, command):
        """Send a simple command to the Harmony Hub.

        Args:
            device_id (str): Device ID from Harmony Hub configuration to control
            command (str): Command from Harmony Hub configuration to control

        Returns:
            None if successful
        """
        iq_cmd = self.Iq()
        iq_cmd['type'] = 'get'
        iq_cmd['id'] = '5e518d07-bcc2-4634-ba3d-c20f338d8927-2'
        action_cmd = ET.Element('oa')
        action_cmd.attrib['xmlns'] = 'connect.logitech.com'
        action_cmd.attrib['mime'] = (
            'vnd.logitech.harmony/vnd.logitech.harmony.engine?holdAction')
        action_cmd.text = 'action={"type"::"IRCommand","deviceId"::"' + device + '","command"::"' + command + '"}:status=press'
        iq_cmd.set_payload(action_cmd)
        result = iq_cmd.send(block=False)

        action_cmd.attrib['mime'] = (
            'vnd.logitech.harmony/vnd.logitech.harmony.engine?holdAction')
        action_cmd.text = 'action={"type"::"IRCommand","deviceId"::"' + device + '","command"::"' + command + '"}:status=release'
        iq_cmd.set_payload(action_cmd)
        result = iq_cmd.send(block=False)
        return result

    def change_channel(self, channel):
        """Changes a channel.
        Args:
            channel: Channel number
        Returns:
          An HTTP 200 response (hopefully)
        """
        iq_cmd = self.Iq()
        iq_cmd['type'] = 'get'
        action_cmd = ET.Element('oa')
        action_cmd.attrib['xmlns'] = 'connect.logitech.com'
        action_cmd.attrib['mime'] = ('harmony.engine?changeChannel')
        cmd = 'channel=' + str(channel) + ':timestamp=0'
        action_cmd.text = cmd
        iq_cmd.set_payload(action_cmd)
        try:
            result = iq_cmd.send(block=True)
        except Exception:
            logger.info('XMPP timeout, reattempting')
            result = iq_cmd.send(block=True)
        payload = result.get_payload()
        assert len(payload) == 1
        action_cmd = payload[0]
        if action_cmd.text == None:
            return True
        else:
            return False


    def power_off(self):
        """Turns the system off if it's on, otherwise it does nothing.

        Returns:
            True if the system becomes or is off
        """
        activity = self.get_current_activity()
        if activity != -1:
            return self.start_activity(-1)
        else:
            return True

    def register_activity_callback(self, activity_callback):
        """Register a callback that is executed on activity changes."""
        def hub_event(xml):
            match = re.search('activityId=(-?\d+)', xml.get_payload()[0].text)
            activity_id = match.group(1)
            if activity_id is not None:
                activity_callback(int(activity_id))

        self.registerHandler(Callback('Activity Finished', MatchHarmonyEvent('startActivityFinished'), hub_event))


class MatchHarmonyEvent(MatcherBase):
    def match(self, xml):
        """Check if a stanza matches the Harmony event criteria."""
        payload = xml.get_payload()
        if len(payload) == 1:
            msg = payload[0]
            if msg.tag == '{connect.logitech.com}event' and msg.attrib['type'] == 'harmony.engine?' + self._criteria:
                return True
        return False


def create_and_connect_client(ip_address, port, activity_callback=None):

    """Creates a Harmony client and initializes session.

    Args:
        ip_address (str): Harmony device IP address
        port (str): Harmony device port
        activity_callback (function): Function to call when the current activity has changed.


    Returns:
        A connected HarmonyClient instance
    """
    client = HarmonyClient()
    client.connect(address=(ip_address, port),
                   use_tls=False, use_ssl=False)
    client.process(block=False)
    client.whitespace_keepalive_interval = 30
    if activity_callback:
        client.register_activity_callback(activity_callback)
    while not client.sessionstarted:
        time.sleep(0.1)
    return client
