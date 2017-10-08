"""
Build Wink devices.
"""

from pywink.devices import types as device_types
from pywink.devices.sensor import WinkSensor
from pywink.devices.light_bulb import WinkLightBulb
from pywink.devices.binary_switch import WinkBinarySwitch
from pywink.devices.lock import WinkLock
from pywink.devices.eggtray import WinkEggtray
from pywink.devices.garage_door import WinkGarageDoor
from pywink.devices.shade import WinkShade
from pywink.devices.siren import WinkSiren
from pywink.devices.key import WinkKey
from pywink.devices.thermostat import WinkThermostat
from pywink.devices.fan import WinkFan
from pywink.devices.remote import WinkRemote
from pywink.devices.hub import WinkHub
from pywink.devices.powerstrip import WinkPowerStrip, WinkPowerStripOutlet
from pywink.devices.piggy_bank import WinkPorkfolioBalanceSensor, WinkPorkfolioNose
from pywink.devices.sprinkler import WinkSprinkler
from pywink.devices.button import WinkButton
from pywink.devices.gang import WinkGang
from pywink.devices.smoke_detector import WinkSmokeDetector, WinkSmokeSeverity, WinkCoDetector, WinkCoSeverity
from pywink.devices.camera import WinkCanaryCamera
from pywink.devices.air_conditioner import WinkAirConditioner
from pywink.devices.propane_tank import WinkPropaneTank
from pywink.devices.robot import WinkRobot
from pywink.devices.scene import WinkScene
from pywink.devices.light_group import WinkLightGroup
from pywink.devices.binary_switch_group import WinkBinarySwitchGroup
from pywink.devices.water_heater import WinkWaterHeater


# pylint: disable=too-many-branches, too-many-statements
def build_device(device_state_as_json, api_interface):
    # This is used to determine what type of object to create
    object_type = device_state_as_json.get("object_type")
    new_objects = []

    if object_type == device_types.LIGHT_BULB:
        new_objects.append(WinkLightBulb(device_state_as_json, api_interface))
    elif object_type == device_types.BINARY_SWITCH:
        # Skip relay switches that aren't controlling a load. The binary_switch can't be used.
        if device_state_as_json.get("last_reading").get("powering_mode") is not None:
            mode = device_state_as_json["last_reading"]["powering_mode"]
            if mode == "dumb":
                new_objects.append(WinkBinarySwitch(device_state_as_json, api_interface))
        else:
            new_objects.append(WinkBinarySwitch(device_state_as_json, api_interface))
    elif object_type == device_types.LOCK:
        new_objects.append(WinkLock(device_state_as_json, api_interface))
    elif object_type == device_types.EGGTRAY:
        new_objects.append(WinkEggtray(device_state_as_json, api_interface))
    elif object_type == device_types.GARAGE_DOOR:
        new_objects.append(WinkGarageDoor(device_state_as_json, api_interface))
    elif object_type == device_types.SHADE:
        new_objects.append(WinkShade(device_state_as_json, api_interface))
    elif object_type == device_types.SIREN:
        new_objects.append(WinkSiren(device_state_as_json, api_interface))
    elif object_type == device_types.KEY:
        new_objects.append(WinkKey(device_state_as_json, api_interface))
    elif object_type == device_types.THERMOSTAT:
        new_objects.append(WinkThermostat(device_state_as_json, api_interface))
    elif object_type == device_types.FAN:
        new_objects.append(WinkFan(device_state_as_json, api_interface))
    elif object_type == device_types.REMOTE:
        # The lutron Pico remote doesn't follow the API spec and
        # provides no benefit as a device in this library.
        if device_state_as_json.get("model_name") != "Pico":
            new_objects.append(WinkRemote(device_state_as_json, api_interface))
    elif object_type == device_types.HUB:
        new_objects.append(WinkHub(device_state_as_json, api_interface))
    elif object_type == device_types.SENSOR_POD:
        new_objects.extend(__get_subsensors_from_device(device_state_as_json, api_interface))
    elif object_type == device_types.POWERSTRIP:
        new_objects.extend(__get_outlets_from_powerstrip(device_state_as_json, api_interface))
        new_objects.append(WinkPowerStrip(device_state_as_json, api_interface))
    elif object_type == device_types.PIGGY_BANK:
        new_objects.extend(__get_devices_from_piggy_bank(device_state_as_json, api_interface))
    elif object_type == device_types.DOOR_BELL:
        new_objects.extend(__get_subsensors_from_device(device_state_as_json, api_interface))
    elif object_type == device_types.SPRINKLER:
        new_objects.append(WinkSprinkler(device_state_as_json, api_interface))
    elif object_type == device_types.BUTTON:
        new_objects.append(WinkButton(device_state_as_json, api_interface))
    elif object_type == device_types.GANG:
        new_objects.append(WinkGang(device_state_as_json, api_interface))
    elif object_type == device_types.SMOKE_DETECTOR:
        new_objects.extend(__get_sensors_from_smoke_detector(device_state_as_json, api_interface))
    elif object_type == device_types.CAMERA:
        if device_state_as_json.get("device_manufacturer") == "canary":
            new_objects.append(WinkCanaryCamera(device_state_as_json, api_interface))
        elif device_state_as_json.get("device_manufacturer") == "dropcam":
            new_objects.extend(__get_subsensors_from_device(device_state_as_json, api_interface))
    elif object_type == device_types.AIR_CONDITIONER:
        new_objects.append(WinkAirConditioner(device_state_as_json, api_interface))
    elif object_type == device_types.PROPANE_TANK:
        new_objects.append(WinkPropaneTank(device_state_as_json, api_interface))
    elif object_type == device_types.ROBOT:
        new_objects.append(WinkRobot(device_state_as_json, api_interface))
    elif object_type == device_types.SCENE:
        new_objects.append(WinkScene(device_state_as_json, api_interface))
    elif object_type == device_types.GROUP:
        # This will skip auto created groups that Wink creates as well has empty groups
        if device_state_as_json.get("name")[0] not in [".", "@"] and device_state_as_json.get("members"):
            # This is a group of swithces
            if device_state_as_json.get("reading_aggregation").get("brightness") is None:
                new_objects.append(WinkBinarySwitchGroup(device_state_as_json, api_interface))
            # This is a group of lights
            else:
                new_objects.append(WinkLightGroup(device_state_as_json, api_interface))
    elif object_type == device_types.WATER_HEATER:
        new_objects.append(WinkWaterHeater(device_state_as_json, api_interface))

    return new_objects


def __get_subsensors_from_device(item, api_interface):
    sensor_types = item.get('capabilities', {}).get('fields', [])
    sensor_types.extend(item.get('capabilities', {}).get('sensor_types', []))

    # These are attributes of the sensor, not the main sensor to track.
    ignored_sensors = ["battery", "powered", "connection", "tamper_detected",
                       "external_power"]

    subsensors = []

    for sensor_type in sensor_types:
        if sensor_type.get("field") in ignored_sensors:
            continue
        else:
            subsensors.append(WinkSensor(item, api_interface, sensor_type))

    return subsensors


def __get_outlets_from_powerstrip(item, api_interface):
    _outlets = []
    outlets = item['outlets']
    for outlet in outlets:
        if 'subscription' in item:
            outlet['subscription'] = item['subscription']
        outlet['last_reading']['connection'] = item['last_reading']['connection']
        _outlets.append(WinkPowerStripOutlet(outlet, api_interface))
    return _outlets


def __get_devices_from_piggy_bank(item, api_interface):
    subdevices = []
    subdevices.append(WinkPorkfolioBalanceSensor(item, api_interface))
    subdevices.append(WinkPorkfolioNose(item, api_interface))
    return subdevices


def __get_sensors_from_smoke_detector(item, api_interface):
    sensors = []
    sensors.append(WinkSmokeDetector(item, api_interface))
    sensors.append(WinkCoDetector(item, api_interface))
    if item.get("manufacturer_device_model") == "nest":
        sensors.append(WinkSmokeSeverity(item, api_interface))
        sensors.append(WinkCoSeverity(item, api_interface))
    return sensors
