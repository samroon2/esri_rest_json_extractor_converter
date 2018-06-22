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

    def test_rangecheck(self):
    	esrijson.get_recordrange()
    	assert isinstance(esrijson.recordinfo, dict)
    	self.assertNotEqual(len(esrijson.recordinfo), 0)

    def test_getjson(self):
    	esrijson.get_json()
    	assert esrijson.json_data.feature_count() > 0

if __name__ == "__main__":
    unittest.main()   
