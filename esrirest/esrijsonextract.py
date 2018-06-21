import requests
from urllib.parse import urlparse
from distutils.dir_util import copy_tree
from .jsonclasses import JSONDATA, GEOJSON
import geopandas as gpd
import pandas as pd
from tqdm import tqdm
import fiona
import json
import os


class GetESRIJSON:
    '''Class for handling requests to extract and transform geospatial data extracted from ESRI REST services.

    :param endpointurl: The endpoint url of where the data lies, eg: http://somedomain.com/arcgis/rest/services/Someservice/query/MapServer/86/query
    :type endpointurl: str
    '''

    def __init__(self, endpointurl: str):
        self.endpointurl = endpointurl
        self.version = self.get_version()
        self.objran = {}
        self.iterlist = []
        self.geojson = GEOJSON()
        self.json_data = JSONDATA()

    @staticmethod
    def endpoint_checker(url):
        '''Helper method for verifying url is to esri rest services.

        :param url: URL of ESRI REST endpoint.
        :type url: str
        :returns:  Bool - whether the url is valid or not.
        :rtype: bool
        '''
        if "/arcgis/rest/services/" and "http" in url:
            return True
        return False

    def get_version(self):
        '''Method for obtaining the esri version.

        :returns: The ESRI version being used.
        :rtype: str
        :raises: Exception
        '''
        if not self.endpoint_checker(self.endpointurl):
            raise Exception("Please use a valid ESRI REST url")

        parsedurl = urlparse(self.endpointurl)
        print(f"{parsedurl.scheme}://{parsedurl.netloc}/arcgis/rest/services/?f=pjson")
        req = requests.get(f"{parsedurl.scheme}://{parsedurl.netloc}/arcgis/rest/services/?f=pjson")

        if req.status_code == 200:
            try:
                return req.json()['currentVersion']
            except KeyError:
                try:
                    req = requests.get(self.endpointurl.split('services/')[0] + 'services/?f=pjson')
                    return req.json()['currentVersion']
                except Exception as e:
                    raise e
        raise Exception(f"An Error occurred retrieving vital information, the response status {str(req.status_code)} associate with {req.json()['error']['message']}")  

    def get_recordrange(self):
        '''Method for determining objectID ranges.
        '''
        if self.version >= 10.1:
            querystr = """?where=&outFields=*&returnGeometry=false&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=[{%0D%0A++++"statisticType"%3A+"count"%2C%0D%0A++++"onStatisticField"%3A+"objectid"%2C+++++"outStatisticFieldName"%3A+"oidcount"%0D%0A++}%2C{%0D%0A++++"statisticType"%3A+"min"%2C%0D%0A++++"onStatisticField"%3A+"objectid"%2C+++++"outStatisticFieldName"%3A+"oidmin"%0D%0A++}%2C{%0D%0A++++"statisticType"%3A+"max"%2C%0D%0A++++"onStatisticField"%3A+"objectid"%2C+++++"outStatisticFieldName"%3A+"oidmax"%0D%0A++}]&returnZ=false&returnM=false&returnDistinctValues=false&f=pjson"""
            req = requests.get(self.endpointurl + querystr)
            self.recordinfo = req.json()['features'][0]['attributes']

        elif self.version < 10.1:
            querystr = """?text=&geometry=&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&objectIds=&where=objectid+>+-1&time=&returnCountOnly=true&returnIdsOnly=false&returnGeometry=false&maxAllowableOffset=&outSR=&outFields=&f=pjson"""
            req = requests.get(self.endpontquerystr + qs)
            self.recordinfo = {'oidmin':0, 'oidmax':req.json()['count']}

        [self.iterlist.append([x, x+999]) for x in range(self.recordinfo['oidmin'], self.recordinfo['oidmax'], 1000)]

    def get_geojson(self):
        '''Method for obtaining geojson data from rest endpoint.
        '''
        self.get_recordrange()
        [self.geojson.setter(n, self.get_data('geojson', x)) for n, x in enumerate(tqdm(self.iterlist))]

    def get_json(self):
        '''Method for obtaining json data from rest endpoint.
        '''
        self.get_recordrange()
        [self.json_data.setter(n, self.get_data('json', x)) for n, x in enumerate(tqdm(self.iterlist))]

    def get_shapefile(self, shpname: str):
        '''Method to obtain data from rest endpoint and export to a .shp file.

        :param shpname: Name of the output shapefile, eg: somefile.shp
        :type shpname: str
        '''
        self.get_geojson()
        self.geojson.to_shp(shpname)

    def get_data(self, exportformat: str, oidrange: list):
        '''Method for requesting data from endpoint.

        :param exportformat: geojson or json.
        :type exportformat: str
        :param oidrange: List containing [minid, maxid]
        :type oidrange: list
        '''
        querystr = f"?where=objectid+>%3D+{oidrange[0]}+AND+objectid+<%3D+{oidrange[1]}&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f={exportformat}"
        req = requests.get(self.endpointurl + querystr)
        return req.json()