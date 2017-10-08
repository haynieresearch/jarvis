from pywink.devices.base import WinkDevice


# pylint: disable=too-many-public-methods
class WinkWaterHeater(WinkDevice):
    """
    Represents a Wink water heater.
    """

    def state(self):
        return self.current_mode()

    def modes(self):
        return self._last_reading.get('modes_allowed')

    def current_mode(self):
        return self._last_reading.get('mode')

    def current_set_point(self):
        return self._last_reading.get('set_point')

    def max_set_point(self):
        return self._last_reading.get('max_set_point_allowed')

    def min_set_point(self):
        return self._last_reading.get('min_set_point_allowed')

    def is_on(self):
        return self._last_reading.get('powered', False)

    def vacation_mode_enabled(self):
        return self._last_reading.get('vacation_mode', False)

    def rheem_type(self):
        return self._last_reading.get('rheem_type')

    def set_operation_mode(self, mode):
        """
        :param mode: a string one of self.modes()
        :return: nothing
        """
        if mode == "off":
            desired_state = {"powered": False}
        else:
            desired_state = {"powered": True, "mode": mode}

        response = self.api_interface.set_device_state(self, {
            "desired_state": desired_state
        })

        self._update_state_from_response(response)

    def set_temperature(self, set_point):
        """
        :param temperature: a float for the temperature value in celsius
        :return: nothing
        """
        response = self.api_interface.set_device_state(self, {
            "desired_state": {'set_point': set_point}
        })

        self._update_state_from_response(response)

    def set_vacation_mode(self, state):
        """
        :param state: a boolean of ture (on) or false ('off')
        :return: nothing
        """
        values = {"desired_state": {"vacation_mode": state}}
        response = self.api_interface.local_set_state(self, values)
        self._update_state_from_response(response)
