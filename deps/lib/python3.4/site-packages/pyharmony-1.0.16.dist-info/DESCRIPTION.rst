pyharmony
=======

Python library for programmatically using a Logitech Harmony Link or Ultimate Hub.

A fork of [bkanuka/pyharmony](https://github.com/bkanuka/pyharmony) with the intent to:
- Make pip/setup.py installable.
- Unify improvments made in other forks.
- Configurable for Harmony Link/Hub differences.
- Better practices for project layout.
- Better error handling!
- Inclusion into Home Assistant (https://home-assistant.io)

Protocol
--------

As the harmony protocol is being worked out, notes are in PROTOCOL.md.

Status
------

* Authentication to Logitech's web service working.
* Authentication to harmony device working.
* Querying for entire device information
* Querying for activity information only
* Querying for current activity
* Starting Activity
* Sending Command

Usage
-----

Pyharmony - Harmony device control

```
usage: harmony [-h] (--harmony_ip HARMONY_IP | --discover)
               [--harmony_port HARMONY_PORT]
               [--loglevel {CRITICAL,ERROR,DEBUG,WARNING,INFO}]
               {show_config,show_current_activity,start_activity,power_off,sync,send_command}
               ...

Pyharmony - Harmony device control

positional arguments:
  {show_config,show_current_activity,start_activity,power_off,sync,send_command}
    show_config         Print the Harmony device configuration.
    show_current_activity
                        Print the current activity config.
    start_activity      Switch to a different activity.
    power_off           Stop the activity.
    sync                Sync the harmony.
    send_command        Send a simple command.

optional arguments:
  -h, --help            show this help message and exit
  --harmony_port HARMONY_PORT
                        Network port that the Harmony is listening on.
                        (default: 5222)
  --loglevel {CRITICAL,ERROR,DEBUG,WARNING,INFO}
                        Logging level to print to the console. (default: INFO)

required arguments:
  --harmony_ip HARMONY_IP
                        IP Address of the Harmony device. (default: None)
  OR
  --discover
                        Run a network scan to discover hubs
```

TODO
----

* Figure out how to detect when the session token expires so we can get a new
  one.
* Figure out a good way of sending commands based on sync state.
* Is it possible to update device configuration?


