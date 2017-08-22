import json
import codecs
import logging
logging.basicConfig()
requests_log = logging.getLogger("requests.packages.urllib3")

try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client

class EvohomeClientInvalidPostData(Exception):
    pass

class EvohomeBase(object):
    def __init__(self, debug=False):
        self.reader = codecs.getdecoder("utf-8")
        
        if debug:
            http_client.HTTPConnection.debuglevel = 1
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True
        else:
            http_client.HTTPConnection.debuglevel = 0
            logging.getLogger().setLevel(logging.INFO)
            requests_log.setLevel(logging.INFO)
            requests_log.propagate = False
    
    def _convert(self, object):
        return json.loads(object)
