from __future__ import print_function
import requests
import json
import codecs
from .location import Location
from .base import EvohomeBase

class EvohomeClient(EvohomeBase):
    def __init__(self, username, password, debug=False):
        super(EvohomeClient, self).__init__(debug)

        self.username = username
        self.password = password

        self.access_token = None
        self.locations = []

        self._login()

    def _get_location(self, location):
        if location is None:
            return self.installation_info[0]['locationInfo']['locationId']
        else:
            return location

    def _get_single_heating_system(self):
        # This allows a shortcut for some systems
        location = None
        gateway = None
        control_system = None
        
        if len(self.locations)==1:
            location = self.locations[0]
        else:
            raise Exception("More than one location available")
            
        if len(location._gateways)==1:
            gateway = location._gateways[0]
        else:
            raise Exception("More than one gateway available")
            
        if len(gateway._control_systems)==1:
            control_system = gateway._control_systems[0]
        else:
            raise Exception("More than one control system available")
            
        return control_system
        
        
    def _login(self):
        url = 'https://tccna.honeywell.com/Auth/OAuth/Token'
        headers = {
            'Authorization':	'Basic YjAxM2FhMjYtOTcyNC00ZGJkLTg4OTctMDQ4YjlhYWRhMjQ5OnRlc3Q=',
            'Accept': 'application/json, application/xml, text/json, text/x-json, text/javascript, text/xml'

        }
        data = {
            'Content-Type':	'application/x-www-form-urlencoded; charset=utf-8',
            'Host':	'rs.alarmnet.com/',
            'Cache-Control':'no-store no-cache',
            'Pragma':	'no-cache',
            'grant_type':	'password',
            'scope':	'EMEA-V1-Basic EMEA-V1-Anonymous EMEA-V1-Get-Current-User-Account',
            'Username':	self.username,
            'Password':	self.password,
            'Connection':	'Keep-Alive'
        }
        r = requests.post(url, data=data, headers=headers)
        self.access_token = self._convert(r.text)['access_token']
        self.headers = {
            'Authorization': 'bearer ' + self.access_token,
            'applicationId': 'b013aa26-9724-4dbd-8897-048b9aada249',
            'Accept': 'application/json, application/xml, text/json, text/x-json, text/javascript, text/xml'
        }
        self.user_account()
        self.installation()


    def user_account(self):
        r = requests.get('https://tccna.honeywell.com/WebAPI/emea/api/v1/userAccount', headers=self.headers)

        self.account_info = self._convert(r.text)
        return self.account_info

    def installation(self):
        r = requests.get('https://tccna.honeywell.com/WebAPI/emea/api/v1/location/installationInfo?userId=%s&includeTemperatureControlSystems=True' % self.account_info['userId'], headers=self.headers)

        self.installation_info = self._convert(r.text)
        self.system_id = self.installation_info[0]['gateways'][0]['temperatureControlSystems'][0]['systemId']

        for loc_data in self.installation_info:
            self.locations.append(Location(self, loc_data))

        return self.installation_info

    def full_installation(self, location=None):
        location = self._get_location(location)
        r = requests.get('https://tccna.honeywell.com/WebAPI/emea/api/v1/location/%s/installationInfo?includeTemperatureControlSystems=True' % location, headers=self.headers)
        return self._convert(r.text)

    def gateway(self):
        r = requests.get('https://tccna.honeywell.com/WebAPI/emea/api/v1/gateway', headers=self.headers)
        return self._convert(r.text)

    def set_status_normal(self):
        return self._get_single_heating_system().set_status_normal()

    def set_status_custom(self, until=None):
        return self._get_single_heating_system().set_status_custom(until)

    def set_status_eco(self, until=None):
        return self._get_single_heating_system().set_status_eco(until)

    def set_status_away(self, until=None):
        return self._get_single_heating_system().set_status_away(until)

    def set_status_dayoff(self, until=None):
        return self._get_single_heating_system().set_status_dayoff(until)

    def set_status_heatingoff(self, until=None):
        return self._get_single_heating_system().set_status_heatingoff(until)

    def temperatures(self):
        return self._get_single_heating_system().temperatures()
    
    def zone_schedules_backup(self, filename):
        return self._get_single_heating_system().zone_schedules_backup(filename)

    def zone_schedules_restore(self, filename):
        return self._get_single_heating_system().zone_schedules_restore(filename)
