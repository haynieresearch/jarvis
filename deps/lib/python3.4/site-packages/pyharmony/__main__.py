#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module for querying and controlling Logitech Harmony devices."""

import argparse
import json
import logging
from pyharmony import client as harmony_client
from pyharmony import discovery as harmony_discovery
import sys
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# Trim down log file spam
logging.getLogger('sleekxmpp').setLevel(logging.CRITICAL)
logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('pyharmony').setLevel(logging.CRITICAL)


def pprint(obj):
    """Pretty JSON dump of an object."""
    print(json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))


def get_client(ip, port, activity_callback=None):
    """Connect to the Harmony and return a Client instance.

    Args:
        harmony_ip (str): Harmony hub IP address
        harmony_port (str): Harmony hub port
        activity_callback (function): Function to call when the current activity has changed.

    Returns:
        object: Authenticated client instance.
    """

    client = harmony_client.create_and_connect_client(ip, port, activity_callback)
    return client


# Functions for use when module is imported by Home Assistant
def ha_get_client(ip, port):
    """Connect to the Harmony and return a Client instance.

    Args:
        ip (str): Harmony hub IP address
        port (str): Harmony hub port
        token (str): Session token obtained from hub

    Returns:
        object: Authenticated client instance.
    """
    client = harmony_client.create_and_connect_client(ip, port)
    return client


def ha_get_config(ip, port):
    """Connects to the Harmony and generates a dictionary containing all activites and commands programmed to hub.

    Args:
        email (str):  Email address used to login to Logitech service
        password (str): Password used to login to Logitech service
        ip (str): Harmony hub IP address
        port (str): Harmony hub port

    Returns:
        Dictionary containing Harmony device configuration
    """
    client = ha_get_client(ip, port)
    config = client.get_config()
    client.disconnect(send_close=True)
    return config


def ha_write_config_file(config, path):
    """Connects to the Harmony huband generates a text file containing all activities and commands programmed to hub.

    Args:
        config (dict): Dictionary object containing configuration information obtained from function ha_get_config
        path (str): Full path to output file

    Returns:
        True
    """
    with open(path, 'w+', encoding='utf-8') as file_out:
        file_out.write('Activities\n')
        for activity in config['activity']:
            file_out.write('  ' + activity['id'] + ' - ' + activity['label'] + '\n')

        file_out.write('\nDevice Commands\n')
        for device in config['device']:
            file_out.write('  ' + device['id'] + ' - ' + device['label'] + '\n')
            for controlGroup in device['controlGroup']:
                for function in controlGroup['function']:
                    file_out.write('    ' + function['name'] + '\n')
    return True


def ha_get_activities(config):
    """Connects to the Harmony hub and returns configured activities.

    Args:
        config (dict): Dictionary object containing configuration information obtained from function ha_get_config

    Returns:
        Dictionary containing activity label and ID number.
    """
    activities = {}
    for activity in config['activity']:
        activities[activity['label']] = activity['id']
    if activities != {}:
        return activities
    else:
        logger.error('Unable to retrieve hub\'s activities')
        return activities


def ha_get_current_activity(config, ip, port):
    """Returns Harmony hub's current activity.

    Args:
        token (str): Session token obtained from hub
        config (dict): Dictionary object containing configuration information obtained from function ha_get_config
        ip (str): Harmony hub IP address
        port (str): Harmony hub port

    Returns:
        String containing hub's current activity.
    """
    client = ha_get_client(ip, port)
    current_activity_id = client.get_current_activity()
    client.disconnect(send_close=True)
    activity = [x for x in config['activity'] if int(x['id']) == current_activity_id][0]
    if type(activity) is dict:
        return activity['label']
    else:
        logger.error('Unable to retrieve current activity')
        return 'Unknown'


def ha_start_activity(ip, port, config, activity):
    """Connects to Harmony Hub and starts an activity

    Args:
        token (str): Session token obtained from hub
        ip (str): Harmony hub IP address
        port (str): Harmony hub port
        config (dict): Dictionary object containing configuration information obtained from function ha_get_config
        activity (str): Activity ID or label to start

    Returns:
        True if activity started, otherwise False
    """
    client = ha_get_client(ip, port)
    status = False

    if (activity.isdigit()) or (activity == '-1'):
        status = client.start_activity(activity)
        client.disconnect(send_close=True)
        if status:
            return True
        else:
            logger.info('Activity start failed')
            return False

    # provided activity string needs to be translated to activity ID from config
    else:
        activities = config['activity']
        labels_and_ids = dict([(a['label'], a['id']) for a in activities])
        matching = [label for label in list(labels_and_ids.keys())
                    if activity.lower() in label.lower()]
        if len(matching) == 1:
            activity = matching[0]
            logger.info('Found activity named %s (id %s)' % (activity, labels_and_ids[activity]))
            status = client.start_activity(labels_and_ids[activity])

    client.disconnect(send_close=True)
    if status:
        return True
    else:
        logger.error('Unable to find matching activity, start failed %s' % (' '.join(activity)))
        return False


def ha_power_off(ip, port):
    """Power off Harmony Hub.

    Args:
        token (str): Session token obtained from hub
        ip (str): Harmony hub IP address
        port (str): Harmony hub port

    Returns:
        True if PowerOff activity started, otherwise False

    """
    client = ha_get_client(ip, port)
    status = client.power_off()
    client.disconnect(send_close=True)
    if status:
        return True
    else:
        logger.error('Power Off failed')
        return False


def ha_send_command(ip, port, device, command, repeat_num=1, delay_secs=0.4):
    """Connects to the Harmony and send a simple command.

    Args:
        token (str): Session token obtained from hub
        ip (str): Harmony hub IP address
        port (str): Harmony hub port
        device (str): Device ID from Harmony Hub configuration to control
        command (str): Command from Harmony Hub configuration to control
        repeat_num (int) : Number of times to repeat the command. Defaults to 1
        delay_secs (float): Delay between sending repeated commands. Not used if only sending a single command. Defaults to 0.4 seconds

    Returns:
        Completion status
    """
    client = ha_get_client(ip, port)
    for i in range(repeat_num):
        client.send_command(device, command)
        time.sleep(delay_secs)

    time.sleep(1)
    client.disconnect(send_close=True)
    return 0


def ha_send_commands(ip, port, device, commands, repeat_num=1, delay_secs=0.4):
    """Connects to the Harmony and sends multiple simple commands.

    Args:
        token (str): Session token obtained from hub
        ip (str): Harmony hub IP address
        port (str): Harmony hub port
        device (str): Device ID from Harmony Hub configuration to control
        commands (list of str): List of commands from Harmony Hub configuration to send
        repeat_num (int) : Number of times to repeat the list of commands. Defaults to 1
        delay_secs (float): Delay between sending commands. Defaults to 0.4 seconds

    Returns:
        Completion status
    """
    client = ha_get_client(ip, port)
    for i in range(repeat_num):
        for command in commands:
            client.send_command(device, command)
            time.sleep(delay_secs)

    time.sleep(1)
    client.disconnect(send_close=True)
    return 0


def ha_sync(ip, port):
    """Syncs Harmony hub to web service.
    Args:
        ip (str): Harmony hub IP address
        port (str): Harmony hub port

    Returns:
        Completion status
    """
    client = ha_get_client(ip, port)
    client.sync()
    client.disconnect(send_close=True)
    return 0


def ha_change_channel(ip, port, channel):
    client = ha_get_client(ip, port)
    status = client.change_channel(channel)
    client.disconnect(send_close=True)
    if status:
        return True
    else:
        logger.error('Unable to change the channel')
        return False


def ha_discover(scan_attempts, scan_interval):
    """Discovers hubs on local network.
    Args:
        scan_attempts (int): Number of times to scan the network
        scan_interval (int): Seconds between running each network scan

    Returns:
        List of config info for any hubs found
    """
    hubs = harmony_discovery.discover(scan_attempts, scan_interval)
    return hubs


# Functions for use on command line
def show_config(args):
    """Connects to the Harmony and return current configuration.

    Args:
        args (argparse): Argparse object containing required variables from command line

    """

    client = get_client(args.harmony_ip, args.harmony_port)
    config = client.get_config()
    client.disconnect(send_close=True)
    pprint(config)


def show_current_activity(args):
    """Returns Harmony hub's current activity.

    Args:
        args (argparse): Argparse object containing required variables from command line

    """
    client = get_client(args.harmony_ip, args.harmony_port)
    config = client.get_config()
    current_activity_id = client.get_current_activity()
    client.disconnect(send_close=True)
    activity = [x for x in config['activity'] if int(x['id']) == current_activity_id][0]
    if type(activity) is dict:
        print(activity['label'])
    else:
        logger.error('Unable to retrieve current activity')
        print('Unknown')


def activity_name(config, activity_id):
    """Looks up an activity in the config, returning its name.

    Args:
        config (dict): Dictionary object containing configuration information obtained from function ha_get_config.
        activity_id (int): Harmony ID of the activity.

    Returns:
        The name of the activity, or None if not found.
    """

    ids_and_labels = dict([(int(a['id']), a['label']) for a in config['activity']])
    return ids_and_labels.get(int(activity_id))


def activity_id(config, activity):
    """Looks up an activity in the config, returning its ID.

    Args:
        config (dict): Dictionary object containing configuration information obtained from function ha_get_config.
        activity (string/int): Harmony name of the activity. Providing an ID returns itself.

    Returns:
        The ID of the activity, or None if not found.
    """

    if activity.isdigit() or activity == '-1':
        if activity_name(config, activity):
            return activity
    labels_and_ids = dict([(a['label'].lower(), int(a['id'])) for a in config['activity']])
    return labels_and_ids.get(activity.lower())


def start_activity(args):
    """Connects to Harmony Hub and starts an activity

    Args:
        args (argparse): Argparse object containing required variables from command line

    """
    client = get_client(args.harmony_ip, args.harmony_port)
    status = False

    if (args.activity.isdigit()) or (args.activity == '-1'):
        status = client.start_activity(args.activity)
        client.disconnect(send_close=True)
        if status:
            print('Started Actvivity')
        else:
            logger.info('Activity start failed')
    else:
        config = client.get_config()
        activities = config['activity']
        labels_and_ids = dict([(a['label'], a['id']) for a in activities])
        matching = [label for label in list(labels_and_ids.keys())
                    if args.activity.lower() in label.lower()]
        if len(matching) == 1:
            activity = matching[0]
            logger.info('Found activity named %s (id %s)' % (activity, labels_and_ids[activity]))
            status = client.start_activity(labels_and_ids[activity])
        client.disconnect(send_close=True)
        if status:
            print('Started:', args.activity)
        else:
            logger.error('found too many activities! %s' % (' '.join(matching)))


def power_off(args):
    """Power off Harmony Hub.

    Args:
        args (argparse): Argparse object containing required variables from command line

    """
    client = get_client(args.harmony_ip, args.harmony_port)
    status = client.power_off()
    client.disconnect(send_close=True)
    if status:
        print('Powered Off')
    else:
        logger.error('Power off failed')


def send_command(args):
    """Connects to the Harmony and send a simple command.

    Args:
        args (argparse): Argparse object containing required variables from command line

    """

    client = get_client(args.harmony_ip, args.harmony_port)
    for i in range(args.repeat_num):
        client.send_command(args.device_id, args.command)
        time.sleep(args.delay_secs)

    client.disconnect(send_close=True)
    print('Command Sent')


def discover(args):
    hubs = harmony_discovery.discover()
    pprint(hubs)


def sync(args):
    """Syncs Harmony hub to web service.
    Args:
        args (argparse): Argparse object containing required variables from command line

    Returns:
        Completion status
    """
    client = get_client(args.harmony_ip, args.harmony_port)
    client.sync()
    client.disconnect(send_close=True)
    print('Sync complete')


def main():
    """Main method for the script."""
    parser = argparse.ArgumentParser(description='Pyharmony - Harmony device control',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    required_flags = parser.add_mutually_exclusive_group(required=True)

    # Required flags go here.
    required_flags.add_argument('--harmony_ip',
                                help='IP Address of the Harmony device.')
    required_flags.add_argument('--discover',
                                action='store_true',
                                help='Scan for Harmony devices.')

    # Flags with default values go here.
    loglevels = dict((logging.getLevelName(level), level) for level in [10, 20, 30, 40, 50])
    parser.add_argument('--harmony_port',
                        required=False,
                        default=5222,
                        type=int,
                        help=('Network port that the Harmony is listening on.'))
    parser.add_argument('--loglevel',
                        default='INFO',
                        choices=list(loglevels.keys()),
                        help='Logging level to print to the console.')

    subparsers = parser.add_subparsers()

    show_config_parser = subparsers.add_parser('show_config', help='Print the Harmony device configuration.')
    show_config_parser.set_defaults(func=show_config)

    show_activity_parser = subparsers.add_parser('show_current_activity', help='Print the current activity config.')
    show_activity_parser.set_defaults(func=show_current_activity)

    start_activity_parser = subparsers.add_parser('start_activity', help='Switch to a different activity.')
    start_activity_parser.add_argument('--activity', help='Activity to switch to, id or label.')
    start_activity_parser.set_defaults(func=start_activity)

    power_off_parser = subparsers.add_parser('power_off', help='Stop the activity.')
    power_off_parser.set_defaults(func=power_off)

    sync_parser = subparsers.add_parser('sync', help='Sync the harmony.')
    sync_parser.set_defaults(func=sync)

    command_parser = subparsers.add_parser('send_command', help='Send a simple command.')
    command_parser.add_argument('--device_id', help='Specify the device id to which we will send the command.')
    command_parser.add_argument('--command', help='IR Command to send to the device.')
    command_parser.add_argument('--repeat_num', type=int, default=1, help='Number of times to repeat the command. Defaults to 1')
    command_parser.add_argument('--delay_secs', type=float, default=0.4, help='Delay between sending repeated commands. Not used if only sending a single command. Defaults to 0.4 seconds')
    command_parser.set_defaults(func=send_command)

    args = parser.parse_args()

    logging.basicConfig(
        level=loglevels[args.loglevel],
        format='%(levelname)s:\t%(name)s\t%(message)s')

    harmony_client.logger.setLevel(loglevels[args.loglevel])
    harmony_discovery.logger.setLevel(loglevels[args.loglevel])

    if args.discover:
        sys.exit(discover(args))
    else:
        sys.exit(args.func(args))


if __name__ == '__main__':
    main()
