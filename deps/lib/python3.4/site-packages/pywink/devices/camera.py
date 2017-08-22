from pywink.devices.base import WinkDevice


class WinkCanaryCamera(WinkDevice):
    """
    Represents a Wink Canary camera.

    The Canary camera has three modes "home", "away", or "night" these avaible modes
    are not listed in the device's JSON.
    """

    def state(self):
        return self.mode()

    def mode(self):
        return self._last_reading.get('mode')

    def private(self):
        return self._last_reading.get('private')

    def set_mode(self, mode):
        """
        :param mode:  a str, one of [home, away, night]
        :return: nothing
        """
        values = {"desired_state": {"mode": mode}}
        response = self.api_interface.set_device_state(self, values)
        self._update_state_from_response(response)

    def set_privacy(self, state):
        """
        :param state: True or False
        :return: nothing
        """
        values = {"desired_state": {"private": state}}
        response = self.api_interface.set_device_state(self, values)
        self._update_state_from_response(response)
