import json
import time
import logging
import urllib.parse

from pywink.devices import types as device_types
from pywink.devices.factory import build_device

import requests
try:
    import urllib3
    from urllib3.exceptions import InsecureRequestWarning
    urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    pass

CLIENT_ID = None
CLIENT_SECRET = None
REFRESH_TOKEN = None
USER_AGENT = "Manufacturer/python-wink python/3 Wink/3"
API_HEADERS = {"User-Agent": USER_AGENT}
ALL_DEVICES = None
LAST_UPDATE = None
OAUTH_AUTHORIZE = "{}/oauth2/authorize?client_id={}&redirect_uri={}"
LOCAL_API_HEADERS = {}
HUBS = {}
SUPPORTS_LOCAL_CONTROL = ["wink_hub", "wink_hub2"]
ALLOW_LOCAL_CONTROL = True

_LOGGER = logging.getLogger(__name__)


class WinkApiInterface(object):

    BASE_URL = "https://api.wink.com"
    api_headers = API_HEADERS

    def set_device_state(self, device, state, id_override=None, type_override=None):
        """
        Set device state via online API.

        Args:
            device (WinkDevice): The device the change is being requested for.
            state (Dict): The state being requested.
            id_override (String, optional): A device ID used to override the
                passed in device's ID. Used to make changes on sub-devices.
                i.e. Outlet in a Powerstrip. The Parent device's ID.
            type_override (String, optional): Used to override the device type
                when a device inherits from a device other than WinkDevice.
        Returns:
            response_json (Dict): The API's response in dictionary format
        """
        _LOGGER.info("Setting state via online API")
        object_id = id_override or device.object_id()
        object_type = type_override or device.object_type()
        url_string = "{}/{}s/{}".format(self.BASE_URL,
                                        object_type,
                                        object_id)
        if state is None or object_type == "group":
            url_string += "/activate"
            if state is None:
                arequest = requests.post(url_string,
                                         headers=API_HEADERS)
            else:
                arequest = requests.post(url_string,
                                         data=json.dumps(state),
                                         headers=API_HEADERS)
        else:
            arequest = requests.put(url_string,
                                    data=json.dumps(state),
                                    headers=API_HEADERS)
        if arequest.status_code == 401:
            new_token = refresh_access_token()
            if new_token:
                arequest = requests.put(url_string,
                                        data=json.dumps(state),
                                        headers=API_HEADERS)
            else:
                raise WinkAPIException("Failed to refresh access token.")
        response_json = arequest.json()
        _LOGGER.debug(response_json)
        return response_json

    # pylint: disable=bare-except
    def local_set_state(self, device, state, id_override=None, type_override=None):
        """
        Set device state via local API, and fall back to online API.

        Args:
            device (WinkDevice): The device the change is being requested for.
            state (Dict): The state being requested.
            id_override (String, optional): A device ID used to override the
                passed in device's ID. Used to make changes on sub-devices.
                i.e. Outlet in a Powerstrip. The Parent device's ID.
            type_override (String, optional): Used to override the device type
                when a device inherits from a device other than WinkDevice.
        Returns:
            response_json (Dict): The API's response in dictionary format
        """
        if ALLOW_LOCAL_CONTROL:
            if device.local_id() is not None:
                hub = HUBS.get(device.hub_id())
                if hub is None:
                    return self.set_device_state(device, state, id_override, type_override)
            else:
                return self.set_device_state(device, state, id_override, type_override)
            _LOGGER.info("Setting local state")
            local_id = id_override or device.local_id().split(".")[0]
            object_type = type_override or device.object_type()
            LOCAL_API_HEADERS['Authorization'] = "Bearer " + hub["token"]
            url_string = "https://{}:8888/{}s/{}".format(hub["ip"],
                                                         object_type,
                                                         local_id)
            try:
                arequest = requests.put(url_string,
                                        data=json.dumps(state),
                                        headers=LOCAL_API_HEADERS,
                                        verify=False, timeout=3)
            except:
                _LOGGER.error("Error sending local control request. Sending request online")
                return self.set_device_state(device, state, id_override, type_override)
            response_json = arequest.json()
            _LOGGER.debug(response_json)
            temp_state = device.json_state
            for key, value in response_json["data"]["last_reading"].items():
                temp_state["last_reading"][key] = value
            return temp_state
        else:
            return self.set_device_state(device, state, id_override, type_override)

    def get_device_state(self, device, id_override=None, type_override=None):
        """
        Get device state via online API.

        Args:
            device (WinkDevice): The device the change is being requested for.
            id_override (String, optional): A device ID used to override the
                passed in device's ID. Used to make changes on sub-devices.
                i.e. Outlet in a Powerstrip. The Parent device's ID.
            type_override (String, optional): Used to override the device type
                when a device inherits from a device other than WinkDevice.
        Returns:
            response_json (Dict): The API's response in dictionary format
        """
        _LOGGER.info("Getting state via online API")
        object_id = id_override or device.object_id()
        object_type = type_override or device.object_type()
        url_string = "{}/{}s/{}".format(self.BASE_URL,
                                        object_type, object_id)
        arequest = requests.get(url_string, headers=API_HEADERS)
        response_json = arequest.json()
        _LOGGER.debug(response_json)
        return response_json

    # pylint: disable=bare-except
    def local_get_state(self, device, id_override=None, type_override=None):
        """
        Get device state via local API, and fall back to online API.

        Args:
            device (WinkDevice): The device the change is being requested for.
            state (Dict): The state being requested.
            id_override (String, optional): A device ID used to override the
                passed in device's ID. Used to make changes on sub-devices.
                i.e. Outlet in a Powerstrip. The Parent device's ID.
            type_override (String, optional): Used to override the device type
                when a device inherits from a device other than WinkDevice.
        Returns:
            response_json (Dict): The API's response in dictionary format
        """
        if ALLOW_LOCAL_CONTROL:
            if device.local_id() is not None:
                hub = HUBS.get(device.hub_id())
                if hub is not None:
                    ip = hub["ip"]
                    access_token = hub["token"]
                else:
                    return self.get_device_state(device, id_override, type_override)
            else:
                return self.get_device_state(device, id_override, type_override)
            _LOGGER.info("Getting local state")
            local_id = id_override or device.local_id()
            object_type = type_override or device.object_type()
            LOCAL_API_HEADERS['Authorization'] = "Bearer " + access_token
            url_string = "https://{}:8888/{}s/{}".format(ip,
                                                         object_type,
                                                         local_id)
            try:
                arequest = requests.get(url_string,
                                        headers=LOCAL_API_HEADERS,
                                        verify=False, timeout=3)
            except:
                _LOGGER.error("Error sending local control request. Sending request online")
                return self.get_device_state(device, id_override, type_override)
            response_json = arequest.json()
            _LOGGER.debug(response_json)
            temp_state = device.json_state
            for key, value in response_json["data"]["last_reading"].items():
                temp_state["last_reading"][key] = value
            return temp_state
        else:
            return self.get_device_state(device, id_override, type_override)

    def update_firmware(self, device, id_override=None, type_override=None):
        """
        Make a call to the update_firmware endpoint. As far as I know this
        is only valid for Wink hubs.

        Args:
            device (WinkDevice): The device the change is being requested for.
            id_override (String, optional): A device ID used to override the
                passed in device's ID. Used to make changes on sub-devices.
                i.e. Outlet in a Powerstrip. The Parent device's ID.
            type_override (String, optional): Used to override the device type
                when a device inherits from a device other than WinkDevice.
        Returns:
            response_json (Dict): The API's response in dictionary format
        """
        object_id = id_override or device.object_id()
        object_type = type_override or device.object_type()
        url_string = "{}/{}s/{}/update_firmware".format(self.BASE_URL,
                                                        object_type,
                                                        object_id)
        arequest = requests.post(url_string,
                                 headers=API_HEADERS)
        response_json = arequest.json()
        return response_json

    def remove_device(self, device, id_override=None, type_override=None):
        """
        Remove a device.

        Args:
            device (WinkDevice): The device the change is being requested for.
            id_override (String, optional): A device ID used to override the
                passed in device's ID. Used to make changes on sub-devices.
                i.e. Outlet in a Powerstrip. The Parent device's ID.
            type_override (String, optional): Used to override the device type
                when a device inherits from a device other than WinkDevice.
        Returns:
            (boolean): True if the device was removed.
        """
        object_id = id_override or device.object_id()
        object_type = type_override or device.object_type()
        url_string = "{}/{}s/{}".format(self.BASE_URL,
                                        object_type,
                                        object_id)
        arequest = requests.delete(url_string,
                                   headers=API_HEADERS)
        if arequest.status_code == 204:
            return True
        _LOGGER.error("Failed to remove device. Status code: " + arequest.status_code)
        return False

    def create_lock_key(self, device, new_device_json, id_override=None, type_override=None):
        """
        Create a new lock key code.

        Args:
            device (WinkDevice): The device the change is being requested for.
            new_device_json (String): The JSON string required to create the device.
            id_override (String, optional): A device ID used to override the
                passed in device's ID. Used to make changes on sub-devices.
                i.e. Outlet in a Powerstrip. The Parent device's ID.
            type_override (String, optional): Used to override the device type
                when a device inherits from a device other than WinkDevice.
        Returns:
            response_json (Dict): The API's response in dictionary format
        """
        object_id = id_override or device.object_id()
        object_type = type_override or device.object_type()
        url_string = "{}/{}s/{}/keys".format(self.BASE_URL,
                                             object_type,
                                             object_id)
        arequest = requests.post(url_string,
                                 data=json.dumps(new_device_json),
                                 headers=API_HEADERS)
        response_json = arequest.json()
        return response_json


def disable_local_control():
    global ALLOW_LOCAL_CONTROL
    ALLOW_LOCAL_CONTROL = False


def set_user_agent(user_agent):
    _LOGGER.info("Setting user agent to " + user_agent)
    API_HEADERS["User-Agent"] = user_agent


def set_bearer_token(token):
    global LOCAL_API_HEADERS

    API_HEADERS["Content-Type"] = "application/json"
    API_HEADERS["Authorization"] = "Bearer {}".format(token)
    LOCAL_API_HEADERS = API_HEADERS


def legacy_set_wink_credentials(email, password, client_id, client_secret):
    log_string = "Email: %s Password: %s Client_id: %s Client_secret: %s" % (email, password, client_id, client_secret)
    _LOGGER.debug(log_string)
    global CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN

    CLIENT_ID = client_id
    CLIENT_SECRET = client_secret

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "password",
        "email": email,
        "password": password
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post('{}/oauth2/token'.format(WinkApiInterface.BASE_URL),
                             data=json.dumps(data),
                             headers=headers)
    response_json = response.json()
    access_token = response_json.get('access_token')
    REFRESH_TOKEN = response_json.get('refresh_token')
    set_bearer_token(access_token)


def set_wink_credentials(client_id, client_secret, access_token, refresh_token):
    log_string = "Client_id: %s Client_secret: %s Access_token: %s Refreash_token: %s" % (client_id, client_secret,
                                                                                          access_token, refresh_token)
    _LOGGER.debug(log_string)
    global CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN

    CLIENT_ID = client_id
    CLIENT_SECRET = client_secret
    REFRESH_TOKEN = refresh_token
    set_bearer_token(access_token)


def get_current_oauth_credentials():
    access_token = API_HEADERS.get("Authorization").split()[1]
    return {"access_token": access_token, "refresh_token": REFRESH_TOKEN,
            "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}


def refresh_access_token():
    global REFRESH_TOKEN
    _LOGGER.info("Attempting to refresh access token")
    if CLIENT_ID and CLIENT_SECRET and REFRESH_TOKEN:
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post('{}/oauth2/token'.format(WinkApiInterface.BASE_URL),
                                 data=json.dumps(data),
                                 headers=headers)
        response_json = response.json()
        access_token = response_json.get('access_token')
        REFRESH_TOKEN = response_json.get('refresh_token')
        set_bearer_token(access_token)
        return access_token
    return None


def get_authorization_url(client_id, redirect_uri):
    _LOGGER.debug("Client_id: " + client_id + " redirect_uri: " + redirect_uri)
    global CLIENT_ID

    CLIENT_ID = client_id
    encoded_uri = urllib.parse.quote(redirect_uri)
    return OAUTH_AUTHORIZE.format(WinkApiInterface.BASE_URL, client_id, encoded_uri)


def request_token(code, client_secret):
    _LOGGER.debug("code: " + code + " Client_secret: " + client_secret)
    data = {
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post('{}/oauth2/token'.format(WinkApiInterface.BASE_URL),
                             data=json.dumps(data),
                             headers=headers)
    _LOGGER.debug(response)
    response_json = response.json()
    access_token = response_json.get('access_token')
    refresh_token = response_json.get('refresh_token')
    return {"access_token": access_token, "refresh_token": refresh_token}


def get_user():
    url_string = "{}/users/me".format(WinkApiInterface.BASE_URL)
    arequest = requests.get(url_string, headers=API_HEADERS)
    _LOGGER.debug(arequest)
    return arequest.json()


def get_local_control_access_token(local_control_id):
    _LOGGER.debug("Local_control_id: " + local_control_id)
    if CLIENT_ID and CLIENT_SECRET and REFRESH_TOKEN:
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN,
            "scope": "local_control",
            "local_control_id": local_control_id
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post('{}/oauth2/token'.format(WinkApiInterface.BASE_URL),
                                 data=json.dumps(data),
                                 headers=headers)
        _LOGGER.debug(response)
        response_json = response.json()
        access_token = response_json.get('access_token')
        return access_token
    _LOGGER.error("Failed to get local control access, reverting to online API")
    disable_local_control()
    return None


def get_all_devices():
    return get_devices(device_types.ALL_SUPPORTED_DEVICES)


def get_light_bulbs():
    return get_devices(device_types.LIGHT_BULB)


def get_switches():
    return get_devices(device_types.BINARY_SWITCH)


def get_sensors():
    return get_devices(device_types.SENSOR_POD)


def get_locks():
    return get_devices(device_types.LOCK)


def get_eggtrays():
    return get_devices(device_types.EGGTRAY)


def get_garage_doors():
    return get_devices(device_types.GARAGE_DOOR)


def get_shades():
    return get_devices(device_types.SHADE)


def get_powerstrips():
    return get_devices(device_types.POWERSTRIP)


def get_sirens():
    return get_devices(device_types.SIREN)


def get_keys():
    return get_devices(device_types.KEY)


def get_piggy_banks():
    return get_devices(device_types.PIGGY_BANK)


def get_smoke_and_co_detectors():
    return get_devices(device_types.SMOKE_DETECTOR)


def get_thermostats():
    return get_devices(device_types.THERMOSTAT)


def get_hubs():
    hubs = get_devices(device_types.HUB)
    for hub in hubs:
        if hub.manufacturer_device_model() in SUPPORTS_LOCAL_CONTROL:
            _id = hub.local_control_id()
            token = get_local_control_access_token(_id)
            ip = hub.ip_address()
            HUBS[hub.object_id()] = {"ip": ip, "token": token, "id": _id}
    return hubs


def get_fans():
    return get_devices(device_types.FAN)


def get_door_bells():
    return get_devices(device_types.DOOR_BELL)


def get_remotes():
    return get_devices(device_types.REMOTE)


def get_sprinklers():
    return get_devices(device_types.SPRINKLER)


def get_buttons():
    return get_devices(device_types.BUTTON)


def get_gangs():
    return get_devices(device_types.GANG)


def get_cameras():
    return get_devices(device_types.CAMERA)


def get_air_conditioners():
    return get_devices(device_types.AIR_CONDITIONER)


def get_propane_tanks():
    return get_devices(device_types.PROPANE_TANK)


def get_robots():
    return get_devices(device_types.ROBOT, "robots")


def get_scenes():
    return get_devices(device_types.SCENE, "scenes")


def get_water_heaters():
    return get_devices(device_types.WATER_HEATER)


def get_light_groups():
    light_groups = []
    for group in get_devices(device_types.GROUP, "groups"):
        # Only light groups have brightness
        if group.json_state.get("reading_aggregation").get("brightness") is not None:
            light_groups.append(group)
    return light_groups


def get_binary_switch_groups():
    switch_groups = []
    for group in get_devices(device_types.GROUP, "groups"):
        # Switches don't have brightness
        if group.json_state.get("reading_aggregation").get("brightness") is None:
            switch_groups.append(group)
    return switch_groups


def get_subscription_key():
    response_dict = wink_api_fetch()
    first_device = response_dict.get('data')[0]
    return get_subscription_key_from_response_dict(first_device)


def get_subscription_key_from_response_dict(device):
    if "subscription" in device:
        return device.get("subscription").get("pubnub").get("subscribe_key")
    return None


def wink_api_fetch(end_point='wink_devices'):
    arequest_url = "{}/users/me/{}".format(WinkApiInterface.BASE_URL, end_point)
    response = requests.get(arequest_url, headers=API_HEADERS)
    _LOGGER.debug(response)
    if response.status_code == 200:
        return response.json()

    if response.status_code == 401:
        raise WinkAPIException("401 Response from Wink API.  Maybe Bearer token is expired?")
    else:
        raise WinkAPIException("Unexpected")


def get_devices(device_type, end_point="wink_devices"):
    global ALL_DEVICES, LAST_UPDATE

    if end_point == "wink_devices":
        now = time.time()
        # Only call the API once to obtain all devices
        if LAST_UPDATE is None or (now - LAST_UPDATE) > 60:
            ALL_DEVICES = wink_api_fetch(end_point)
            LAST_UPDATE = now
        return get_devices_from_response_dict(ALL_DEVICES, device_type)
    elif end_point == "robots" or end_point == "scenes" or end_point == "groups":
        json_data = wink_api_fetch(end_point)
        return get_devices_from_response_dict(json_data, device_type)


def get_devices_from_response_dict(response_dict, device_type):
    """
    :rtype: list of WinkDevice
    """
    items = response_dict.get('data')

    devices = []

    api_interface = WinkApiInterface()

    for item in items:
        if item.get("object_type") in device_type:
            _devices = build_device(item, api_interface)
            for device in _devices:
                devices.append(device)

    return devices


class WinkAPIException(Exception):
    pass
