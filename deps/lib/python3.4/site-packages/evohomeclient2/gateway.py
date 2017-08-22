from .controlsystem import ControlSystem

class Gateway(object):


    def __init__(self, client, location, data=None):
        self.client = client
        self.location = location
        self._control_systems = []
        self.control_systems = {}
        if data is not None:
            self.__dict__.update(data['gatewayInfo'])

            for cs_data in data['temperatureControlSystems']:
                cs = ControlSystem(client, location, self, cs_data)
                self._control_systems.append(cs)
                self.control_systems[cs.systemId] = cs
