class WinkDevice(object):
    """
    This is a generic Wink device, all other object inherit from this.
    """

    def __init__(self, device_state_as_json, api_interface):
        """
        :type api_interface pywink.api.WinkApiInterface:
        :return:
        """
        self.api_interface = api_interface
        self.json_state = device_state_as_json
        self.pubnub_key = None
        self.pubnub_channel = None
        self.obj_id = self.json_state.get('object_id')
        self.obj_type = self.json_state.get('object_type')
        subscription = self.json_state.get('subscription')
        if subscription != {} and subscription is not None:
            pubnub = subscription.get('pubnub')
            self.pubnub_key = pubnub.get('subscribe_key')
            self.pubnub_channel = pubnub.get('channel')

    def name(self):
        return self.json_state.get('name')

    def set_name(self, name):
        response = self.api_interface.set_device_state(self, {
            "name": name
        })
        self._update_state_from_response(response)

    def state(self):
        raise NotImplementedError("Must implement state")

    def object_id(self):
        return self.obj_id

    def object_type(self):
        return self.obj_type

    def hub_id(self):
        return self.json_state.get('hub_id')

    def local_id(self):
        # Devices with a "gang" controlling them (Ceiling fans and their associated light)
        # must be controlled by the gang's local control ID.
        # These devices local control ID is in the following format (gang_id.their_id)
        # Stripping the trailing ID so the first ID is always used.
        _local_id = self.json_state.get('local_id')
        if _local_id is not None:
            _local_id = _local_id.split(".")[0]
        return _local_id

    @property
    def _last_reading(self):
        return self.json_state.get('last_reading') or {}

    def available(self):
        return self._last_reading.get('connection', False)

    def battery_level(self):
        if not self._last_reading.get('external_power'):
            try:
                _battery = self._last_reading.get('battery')
                _battery = float(_battery)
                return _battery
            except TypeError:
                return None
        else:
            return None

    def manufacturer_device_model(self):
        return self.json_state.get('manufacturer_device_model')

    def manufacturer_device_id(self):
        return self.json_state.get('manufacturer_device_id')

    def device_manufacturer(self):
        return self.json_state.get('device_manufacturer')

    def model_name(self):
        return self.json_state.get('model_name')

    def remove_device(self):
        return self.api_interface.remove_device(self)

    def _update_state_from_response(self, response_json):
        """
        :param response_json: the json obj returned from query
        :return:
        """
        _response_json = response_json.get('data')
        if _response_json is not None:
            self.json_state = _response_json
            return True
        return False

    def update_state(self):
        """ Update state with latest info from Wink API. """
        response = self.api_interface.get_device_state(self)
        return self._update_state_from_response(response)

    def pubnub_update(self, json_response):
        if json_response is not None:
            self.json_state = json_response
        else:
            self.update_state()
