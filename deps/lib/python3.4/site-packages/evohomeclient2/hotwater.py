import requests
import json

from .zone import ZoneBase

class HotWater(ZoneBase):

    def __init__(self, client, data=None):
        super(HotWater, self).__init__()
        self.client = client
        self.zone_type = 'domesticHotWater'
        if data is not None:
            self.__dict__.update(data)
            self.zoneId = self.dhwId

    def _set_dhw(self, data):
        headers = dict(self.client.headers)
        headers['Content-Type'] = 'application/json'
        url = 'https://tccna.honeywell.com/WebAPI/emea/api/v1/domesticHotWater/%s/state' % self.dhwId

        response = requests.put(url, data=json.dumps(data), headers=headers)


    def set_dhw_on(self, until=None):
        if until is None:
            data = {"State":1,"Mode":1,"UntilTime":None}
        else:
            data = {"State":1,"Mode":2,"UntilTime":until.strftime('%Y-%m-%dT%H:%M:%SZ')}
        self._set_dhw(data)

    def set_dhw_off(self, until=None):
        if until is None:
            data = {"State":0,"Mode":1,"UntilTime":None}
        else:
            data = {"State":0,"Mode":2,"UntilTime":until.strftime('%Y-%m-%dT%H:%M:%SZ')}
        self._set_dhw(data)

    def set_dhw_auto(self):
        data =  {"State":0,"Mode":0,"UntilTime":None}
        self._set_dhw(data)
