"""
Top level functions
"""
# noqa
from pywink.api import set_bearer_token, refresh_access_token, \
    set_wink_credentials, set_user_agent, wink_api_fetch, get_devices, \
    get_subscription_key, get_user, get_authorization_url, \
    request_token, legacy_set_wink_credentials, get_current_oauth_credentials, \
    disable_local_control

from pywink.api import get_light_bulbs, get_garage_doors, get_locks, \
    get_powerstrips, get_shades, get_sirens, \
    get_switches, get_thermostats, get_fans, get_air_conditioners, \
    get_propane_tanks, get_robots, get_scenes, get_light_groups, \
    get_binary_switch_groups, get_water_heaters

from pywink.api import get_all_devices, get_eggtrays, get_sensors, \
    get_keys, get_piggy_banks, get_smoke_and_co_detectors, \
    get_hubs, get_door_bells, get_remotes, get_sprinklers, get_buttons, \
    get_gangs, get_cameras
