from .gateway import Gateway
from .base import EvohomeBase
import requests

class Location(EvohomeBase):

    def __init__(self, client, data=None):
        super(Location, self).__init__()
        self.client = client
        self._gateways = []
        self.gateways = {}
        if data is not None:
            self.__dict__.update(data['locationInfo'])

            for gw_data in data['gateways']:
                gateway = Gateway(client, self, gw_data)
                self._gateways.append(gateway)
                self.gateways[gateway.gatewayId] = gateway
            self.status()

    def status(self):
        r = requests.get('https://tccna.honeywell.com/WebAPI/emea/api/v1/location/%s/status?includeTemperatureControlSystems=True' % self.locationId, headers=self.client.headers)
        data = self.client._convert(r.text)

        # Now feed into other elements
        for gw in data['gateways']:
            gateway = self.gateways[gw['gatewayId']]

            for sys in gw["temperatureControlSystems"]:
                system = gateway.control_systems[sys['systemId']]

                system.__dict__.update({'systemModeStatus': sys['systemModeStatus'], 'activeFaults': sys['activeFaults']})

                if 'dhw' in sys:
                    system.hotwater.__dict__.update(sys['dhw'])

                for z in sys["zones"]:
                    zone = system.zones[z['name']]
                    zone.__dict__.update(z)

        return data
