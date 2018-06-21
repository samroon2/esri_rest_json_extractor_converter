import unittest
import json
import base64
from esrirest import *
 
 
esrijson = GetESRIJSON('http://arcgis4.roktech.net/arcgis/rest/services/Durham/query/MapServer/86/query')

class BasicTests(unittest.TestCase):
 
###############
#### tests ####
###############

    def test_endpointcheck(self):
        valid = esrijson.endpoint_checker(esrijson.endpointurl)
        assert isinstance(valid, bool)

    def test_versionchecker(self):
    	version = esrijson.get_version()
    	assert isinstance(version, float)


if __name__ == "__main__":
    unittest.main()   
