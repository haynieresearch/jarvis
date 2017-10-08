from pywink.devices.base import WinkDevice


# pylint: disable=too-many-public-methods
class WinkThermostat(WinkDevice):
    """
    Represents a Wink thermostat.
    """

    def state(self):
        return self.current_hvac_mode()

    def fan_modes(self):
        capabilities = self.json_state.get('capabilities', {})
        cap_fields = capabilities.get('fields', [])
        fan_modes = None
        for field in cap_fields:
            _field = field.get('field')
            if _field == 'fan_mode':
                fan_modes = field.get('choices')
        return fan_modes

    def hvac_modes(self):
        capabilities = self.json_state.get('capabilities', {})
        cap_fields = capabilities.get('fields', [])
        hvac_modes = None
        for field in cap_fields:
            _field = field.get('field')
            if _field == 'mode':
                hvac_modes = field.get('choices')
        return hvac_modes

    def away(self):
        return self._last_reading.get('users_away', False)

    def current_hvac_mode(self):
        return self._last_reading.get('mode', None)

    def current_fan_mode(self):
        return self._last_reading.get('fan_mode', None)

    def current_units(self):
        return self._last_reading.get('units', None)

    def current_temperature(self):
        return self._last_reading.get('temperature', None)

    def current_external_temperature(self):
        return self._last_reading.get('external_temperature', None)

    def current_smart_temperature(self):
        return self._last_reading.get('smart_temperature', None)

    def current_humidity(self):
        return self._last_reading.get('humidity', None)

    def current_max_set_point(self):
        return self._last_reading.get('max_set_point', None)

    def current_min_set_point(self):
        return self._last_reading.get('min_set_point', None)

    def current_humidifier_mode(self):
        return self._last_reading.get('humidifier_mode', None)

    def current_dehumidifier_mode(self):
        return self._last_reading.get('dehumidifier_mode', None)

    def current_humidifier_set_point(self):
        return self._last_reading.get('humidifier_set_point', None)

    def current_dehumidifier_set_point(self):
        return self._last_reading.get('dehumidifier_set_point', None)

    def min_min_set_point(self):
        return self._last_reading.get('min_min_set_point', None)

    def max_min_set_point(self):
        return self._last_reading.get('max_min_set_point', None)

    def min_max_set_point(self):
        return self._last_reading.get('min_max_set_point', None)

    def max_max_set_point(self):
        return self._last_reading.get('max_max_set_point', None)

    def eco_target(self):
        return self._last_reading.get('eco_target', None)

    def occupied(self):
        return self._last_reading.get('occupied', None)

    def deadband(self):
        return self._last_reading.get('deadband', None)

    def fan_on(self):
        if self.has_fan():
            return self._last_reading.get('fan_active', False)
        return False

    def has_fan(self):
        cap_fields = self.json_state.get('capabilities').get('fields')
        for field in cap_fields:
            if field.get('field') == "fan_mode":
                return True
        return self._last_reading.get('has_fan', False)

    def is_on(self):
        return self._last_reading.get('powered', False)

    def set_fan_mode(self, mode):
        """
        :param mode: a string one of ["on", "auto"]
        :return: nothing
        """
        desired_state = {"fan_mode": mode}

        response = self.api_interface.set_device_state(self, {
            "desired_state": desired_state
        })

        self._update_state_from_response(response)

    def set_away(self, away=True):
        """
        :param away: a boolean of true (away) or false ('home')
        :return nothing
        """
        desired_state = {"users_away": away}

        response = self.api_interface.set_device_state(self, {
            "desired_state": desired_state
        })

        self._update_state_from_response(response)

    def set_operation_mode(self, mode):
        """
        :param mode: a string one of ["cool_only", "heat_only", "auto", "aux", "off"]
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

    def set_temperature(self, min_set_point=None, max_set_point=None):
        """
        :param temperature: a float for the temperature value in celsius
        :return: nothing
        """
        desired_state = {}

        if min_set_point:
            desired_state['min_set_point'] = min_set_point
        if max_set_point:
            desired_state['max_set_point'] = max_set_point

        response = self.api_interface.set_device_state(self, {
            "desired_state": desired_state
        })

        self._update_state_from_response(response)
