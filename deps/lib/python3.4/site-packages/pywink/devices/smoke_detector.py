from pywink.devices.sensor import WinkDevice


class WinkBaseSmokeDetector(WinkDevice):
    """Represents a base smoke detector sensor."""

    def __init__(self, device_state_as_json, api_interface, unit_type, capability):
        super(WinkBaseSmokeDetector, self).__init__(device_state_as_json, api_interface)
        self._unit = None
        self._unit_type = unit_type
        self._capability = capability

    def unit(self):
        return self._unit

    def unit_type(self):
        return self._unit_type

    def capability(self):
        return self._capability

    def name(self):
        return self.json_state.get("name") + " " + self.capability()

    def state(self):
        return self._last_reading.get(self.capability())

    def test_activated(self):
        return self._last_reading.get("test_activated")


class WinkSmokeDetector(WinkBaseSmokeDetector):
    """
    Represents a Wink Smoke detector.
    """

    def __init__(self, device_state_as_json, api_interface):
        capability = "smoke_detected"
        unit_type = "boolean"
        super(WinkSmokeDetector, self).__init__(device_state_as_json, api_interface, unit_type, capability)


class WinkSmokeSeverity(WinkBaseSmokeDetector):
    """
    Represents a Wink/Nest Smoke severity sensor.
    """

    def __init__(self, device_state_as_json, api_interface):
        capability = "smoke_severity"
        super(WinkSmokeSeverity, self).__init__(device_state_as_json, api_interface, None, capability)


class WinkCoDetector(WinkBaseSmokeDetector):
    """
    Represents a Wink CO detector.
    """

    def __init__(self, device_state_as_json, api_interface):
        capability = "co_detected"
        unit_type = "boolean"
        super(WinkCoDetector, self).__init__(device_state_as_json, api_interface, unit_type, capability)


class WinkCoSeverity(WinkBaseSmokeDetector):
    """
    Represents a Wink/Nest CO severity sensor.
    """

    def __init__(self, device_state_as_json, api_interface):
        capability = "co_severity"
        super(WinkCoSeverity, self).__init__(device_state_as_json, api_interface, None, capability)
