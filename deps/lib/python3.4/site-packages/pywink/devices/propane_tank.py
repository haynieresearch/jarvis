from pywink.devices.base import WinkDevice


class WinkPropaneTank(WinkDevice):
    """
    Represents a Wink refuel.
    """

    def __init__(self, device_state_as_json, api_interface):
        super(WinkPropaneTank, self).__init__(device_state_as_json, api_interface)
        self._capability = None
        self._unit = None

    def capability(self):
        # Propane tanks have no capability.
        return self._capability

    def unit(self):
        return self._unit

    def state(self):
        return self._last_reading.get("remaining")

    def tare(self):
        return self.json_state.get("tare")

    def set_tare(self, tare):
        """
        :param tare: weight of tank as printed on can
        :return: nothing
        tare is not set in desired state, but on the main device.
        """
        response = self.api_interface.set_device_state(self, {"tare": tare})
        self._update_state_from_response(response)
