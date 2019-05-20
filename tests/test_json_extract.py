import unittest
import json
import base64
import os, sys

testdir = os.path.dirname(__file__)
srcdir = '../'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from esrirest.json_extract import GetESRIJSON

esrijson = GetESRIJSON('http://arcgis4.roktech.net/arcgis/rest/services/DaytonaBeach/TRAKiT/MapServer/10/query')

class BasicTests(unittest.TestCase):

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
        esrijson = GetESRIJSON('http://arcgis4.roktech.net/arcgis/rest/services/DaytonaBeach/TRAKiT/MapServer/10/query')
        esrijson.get_json()
        assert esrijson.json_data.feature_count() > 0

    def test_getgeojson(self):
        esrijson = GetESRIJSON('http://arcgis4.roktech.net/arcgis/rest/services/DaytonaBeach/TRAKiT/MapServer/10/query')
        esrijson.get_geojson()
        assert esrijson.geojson.feature_count() > 0

    def test_getshapefile(self):
        esrijson = GetESRIJSON('http://arcgis4.roktech.net/arcgis/rest/services/DaytonaBeach/TRAKiT/MapServer/10/query')
        esrijson.get_shapefile('tests_1.shp')
        assert os.path.exists('tests_1.shp')

if __name__ == "__main__":
    unittest.main()   