import unittest
import json
import base64
from esrirest import *
import os.path 
 
esrijson = GetESRIJSON('http://arcgis4.roktech.net/arcgis/rest/services/Durham/query/MapServer/86/query')

class BasicTests(unittest.TestCase):
 
###############
#### tests ####
###############

    def test_setter(self):
        jsonn = JSONDATA()
        jsonn.setter(0, {'features':[{1:'test'}]})
        assert isinstance(jsonn.json_data, dict)
        jsonn.setter(1, {'features':[{2:'test2'}]})
        assert len(jsonn.json_data['features']) == 2

    def test_featurecount(self):
        jsonn = JSONDATA()
        jsonn.setter(0, {'features':[{1:'test'}]})
        jsonn.setter(1, {'features':[{2:'test2'}]})
        assert jsonn.feature_count() > 1

if __name__ == "__main__":
    unittest.main()   
