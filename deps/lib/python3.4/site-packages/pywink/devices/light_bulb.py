from pywink.devices.base import WinkDevice


class WinkLightBulb(WinkDevice):
    """
    Represents a Wink light bulb.
    """

    def state(self):
        return self._last_reading.get('powered', False)

    def brightness(self):
        return self._last_reading.get('brightness')

    def color_model(self):
        return self._last_reading.get('color_model')

    def color_xy(self):
        """
        XY colour value: [float, float] or None
        :rtype: list float
        """
        color_x = self._last_reading.get('color_x')
        color_y = self._last_reading.get('color_y')
        if color_x is not None and color_y is not None:
            return [float(color_x), float(color_y)]
        return None

    def color_temperature_kelvin(self):
        """
        Color temperature, in degrees Kelvin.
        Eg: "Daylight" light bulbs are 4600K
        :rtype: int
        """
        return self._last_reading.get('color_temperature')

    def color_hue(self):
        """
        Color hue from 0 to 1.0
        """
        return self._last_reading.get('hue')

    def color_saturation(self):
        """
        Color saturation from 0 to 1.0
        :return:
        """
        return self._last_reading.get('saturation')

    def update_state(self):
        """ Update state with latest info from Wink API. """
        response = self.api_interface.local_get_state(self)
        return self._update_state_from_response(response)

    def set_state(self, state, brightness=None,
                  color_kelvin=None, color_xy=None,
                  color_hue_saturation=None):
        """
        :param state:   a boolean of true (on) or false ('off')
        :param brightness: a float from 0 to 1 to set the brightness of
         this bulb
        :param color_kelvin: an integer greater than 0 which is a color in
         degrees Kelvin
        :param color_xy: a pair of floats in a list which specify the desired
        CIE 1931 x,y color coordinates
        :param color_hue_saturation: a pair of floats in a list which specify
        the desired hue and saturation in that order.  Brightness can be
        supplied via the brightness param
        :return: nothing
        """
        desired_state = {"powered": state}

        color_state = self._format_color_data(color_hue_saturation, color_kelvin, color_xy)
        if color_state is not None:
            desired_state.update(color_state)

        if brightness is not None:
            desired_state.update({'brightness': brightness})

        response = self.api_interface.local_set_state(self, {
            "desired_state": desired_state
        })
        self._update_state_from_response(response)

    def _format_color_data(self, color_hue_saturation, color_kelvin, color_xy):
        if color_hue_saturation is None and color_kelvin is None and color_xy is None:
            return None

        if color_hue_saturation is None and color_kelvin is not None and self.supports_temperature():
            return _format_temperature(color_kelvin)

        if self.supports_hue_saturation():
            hsv = _get_color_as_hue_saturation_brightness(color_hue_saturation)
            if hsv is not None:
                return _format_hue_saturation(hsv)

        if self.supports_xy_color():
            if color_xy is not None:
                return _format_xy(color_xy)

        return {}

    def supports_hue_saturation(self):
        capabilities = self.json_state.get('capabilities', {})
        cap_fields = capabilities.get('fields', [])
        for field in cap_fields:
            _field = field.get('field')
            if _field == 'color_model':
                choices = field.get('choices')
                if "hsb" in choices:
                    return True
        return False

    def supports_xy_color(self):
        capabilities = self.json_state.get('capabilities', {})
        cap_fields = capabilities.get('fields', [])
        for field in cap_fields:
            _field = field.get('field')
            if _field == 'color_model':
                choices = field.get('choices')
                if "xy" in choices:
                    return True
        return False

    def supports_temperature(self):
        capabilities = self.json_state.get('capabilities', {})
        cap_fields = capabilities.get('fields', [])
        for field in cap_fields:
            _field = field.get('field')
            if _field == 'color_model':
                choices = field.get('choices')
                if "color_temperature" in choices:
                    return True
        return False


def _format_temperature(kelvin):
    return {
        "color_model": "color_temperature",
        "color_temperature": kelvin,
    }


def _format_hue_saturation(hue_saturation):
    hsv_iter = iter(hue_saturation)
    return {
        "color_model": "hsb",
        "hue": next(hsv_iter),
        "saturation": next(hsv_iter),
    }


def _format_xy(xy):
    color_xy_iter = iter(xy)
    return {
        "color_model": "xy",
        "color_x": next(color_xy_iter),
        "color_y": next(color_xy_iter)
    }


def _get_color_as_hue_saturation_brightness(hue_sat):
    if hue_sat:
        color_hs_iter = iter(hue_sat)
        return next(color_hs_iter), next(color_hs_iter), 1
