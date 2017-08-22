from pywink.devices.binary_switch import WinkBinarySwitch


class WinkButton(WinkBinarySwitch):
    """
    Represents a Wink relay button.
    """

    def state(self):
        return bool(self.long_pressed() or self.pressed())

    def long_pressed(self):
        return self._last_reading.get('long_pressed') or False

    def pressed(self):
        return self._last_reading.get('pressed') or False

    def update_state(self):
        """
        Update state with latest info from Wink API.
        """
        response = self.api_interface.get_device_state(self, type_override="button")
        return self._update_state_from_response(response)
