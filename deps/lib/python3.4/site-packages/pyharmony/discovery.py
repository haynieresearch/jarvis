#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python port of JavaScript Harmony discovery here:
# https://github.com/swissmanu/harmonyhubjs-discover

import socket
import time
import threading
import logging

UDP_IP = '0.0.0.0'
PORT_TO_ANNOUNCE = 61991

logger = logging.getLogger(__name__)


class Discovery:

    def listen(self, hubs, listen_socket):
        while True:
            client_connection, client_address = listen_socket.accept()
            request = client_connection.recv(1024)
            if request:
                hub = self.deserialize_response(
                    request.decode('UTF-8'))

                if hub:
                    uuid = hub['uuid']
                    if uuid not in hubs:
                        logger.debug('Found new hub %s', uuid)
                        hubs[hub['uuid']] = hub
                    else:
                        logger.debug('Found existing hub %s', uuid)
            client_connection.close()

    def deserialize_response(self, response):
        """Parses `key:value;` formatted string into dictionary"""
        pairs = {}
        if not response.strip():
            return False

        for data_point in response.split(';'):
            key_value = data_point.split(':')
            pairs[key_value[0]] = key_value[1]
        return pairs

    def discover(self, scan_attempts, scan_interval):
        # https://ruslanspivak.com/lsbaws-part1/
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind((
            UDP_IP,
            PORT_TO_ANNOUNCE,
            ))
        listen_socket.listen(1)

        hubs = {}

        listen_thread = threading.Thread(
            target=self.listen,
            args=(hubs, listen_socket,),
            daemon=True)
        listen_thread.start()

        ping_sock = socket.socket(socket.AF_INET,       # Internet
                                  socket.SOCK_DGRAM)    # UDP
        ping_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Format of broadcast ported from @swissmanu
        # https://github.com/swissmanu/harmonyhubjs-discover
        MESSAGE = '_logitech-reverse-bonjour._tcp.local.\n{}'.format(
                        PORT_TO_ANNOUNCE).encode('utf-8')

        for scan in range(0, scan_attempts):
            try:
                logger.debug('Pinging network on port %s', PORT_TO_ANNOUNCE)
                ping_sock.sendto(MESSAGE, ('255.255.255.255', 5224))
            except Exception as e:
                logger.error('Error pinging network: %s', e)

            time.sleep(scan_interval)

        # Close the socket
        ping_sock.close()

        logger.info('Completed scan, %s hub(s) found.', len(hubs))
        return [hubs[h] for h in hubs]


def discover(scan_attempts=10, scan_interval=1):
    """Creates a Harmony client and initializes session.

    Args:
        scan_attempts (int): Number of times to scan the network
        scan_interval (int): Seconds between running each network scan

    Returns:
        A list of Hub devices found and their configs
    """
    return Discovery().discover(scan_attempts, scan_interval)
