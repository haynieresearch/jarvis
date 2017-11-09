from pywink.devices.binary_switch import WinkBinarySwitch


class WinkSprinkler(WinkBinarySwitch):
    """
    Represents a Wink Sprinkler.
    """

    def state(self):
        return self._last_reading.get('powered', False)

    def update_state(self):
        """
        Update state with latest info from Wink API.
        """
        response = self.api_interface.get_device_state(self, type_override="sprinkler")
        return self._update_state_from_response(response)
