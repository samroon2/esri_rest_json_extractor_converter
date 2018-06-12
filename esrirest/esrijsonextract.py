import requests
from urllib.parse import urlparse
from distutils.dir_util import copy_tree
import simplejson as json
import traceback
import geopandas as gpd
import pandas as pd
from tqdm import tqdm
import fiona
import json
import os

class GetESRIJSON:

	def __init__(self, endpointurl: str):
		self.endpointurl = endpointurl
		self.version = self.getversion()
		self.objran = {}
		self.iterlist = []
		self.geojson = GEOJSON()
		self.json_data = JSONDATA()

	@staticmethod
	def endpoint_checker(url):
		'''helper method for verifying url is to esri rest services'''
		if "/arcgis/rest/services/" and "http" in url:
			return True
		return False

	def getversion(self):
		'''method for obtaining the esri version'''
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
		raise Exception(f"An Error occured retrieving vital information, the response status {str(req.status_code)} associate with {req.json()['error']['message']}")	

	def getrecordrange(self):
		'''method for determining objectID ranges'''
		if self.version >= 10.1:
			querystr = """?where=&outFields=*&returnGeometry=false&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=[{%0D%0A++++"statisticType"%3A+"count"%2C%0D%0A++++"onStatisticField"%3A+"objectid"%2C+++++"outStatisticFieldName"%3A+"oidcount"%0D%0A++}%2C{%0D%0A++++"statisticType"%3A+"min"%2C%0D%0A++++"onStatisticField"%3A+"objectid"%2C+++++"outStatisticFieldName"%3A+"oidmin"%0D%0A++}%2C{%0D%0A++++"statisticType"%3A+"max"%2C%0D%0A++++"onStatisticField"%3A+"objectid"%2C+++++"outStatisticFieldName"%3A+"oidmax"%0D%0A++}]&returnZ=false&returnM=false&returnDistinctValues=false&f=pjson"""
			req = requests.get(self.endpointurl + querystr)
			self.recordinfo = req.json()['features'][0]['attributes']
		elif self.version < 10.1:
			querystr = """?text=&geometry=&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&objectIds=&where=objectid+>+-1&time=&returnCountOnly=true&returnIdsOnly=false&returnGeometry=false&maxAllowableOffset=&outSR=&outFields=&f=pjson"""
			req = requests.get(self.endpontquerystr + qs)
			self.recordinfo = {'oidmin':0, 'oidmax':req.json()['count']}

		[self.iterlist.append([x, x+999]) for x in range(self.recordinfo['oidmin'], self.recordinfo['oidmax'], 1000)]

	def getgeojson(self):
		'''method for obtaining geojson data from rest endpoint'''
		self.getrecordrange()
		[self.geojson.setter(n, self.getdata('geojson', x)) for n, x in enumerate(tqdm(self.iterlist))]

	def getjson(self):
		'''method for obtaining json data from rest endpoint'''
		self.getrecordrange()
		[self.json_data.setter(n, self.getdata('json', x)) for n, x in enumerate(tqdm(self.iterlist))]

	def getshapefile(self, shpname: str):
		'''method to obtain data from rest endpoint and export to a .shp file.
		args: - shpname'''
		self.getgeojson()
		self.geojson.to_shp(shpname)

	def getdata(self, exportformat: str, oidrange: list):
		'''method for requesting data from endpoint'''
		querystr = f"?where=objectid+>%3D+{oidrange[0]}+AND+objectid+<%3D+{oidrange[1]}&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f={exportformat}"
		req = requests.get(self.endpointurl + querystr)
		return req.json()

class JSONDATA:
	'''class for manipulating JSON'''

	def __init__(self):
		self.json_data = {}

	def setter(self, indexnumber: int, jsondata):
		'''method to set assemble multiple json payloads into one file'''
		if indexnumber == 0:
			self.json_data = jsondata
		elif indexnumber > 0:
			try:
				if len(jsondata['features']) > 0:
					for feat in jsondata['features']:
						self.json_data['features'].append(feat)
				else:
					print(len(jsondata['features']))
			except Exception as e:
				print(e)	

	def featurecount(self):
		'''method that returns the number if features in the dataset'''
		if len(self.json_data) > 0:
			return len(self.json_data['features'])
		return 0

	def to_json(self, jsonfilename: str):
		'''method for exporting data to a .json file'''
		if self.featurecount() > 0:
			with open(jsonfilename, "w") as outfile:
				json.dump(self.json_data, outfile)
		else:
			print('No data to write to file.')

class GEOJSON(JSONDATA):
	'''class for manipulating JSON'''

	def __init__(self):
		super().__init__()

	def to_geojson(self, jsonfilename: str):
		'''method for exporting data to a .json file'''
		if self.featurecount() > 0:
			with open(jsonfilename, "w") as outfile:
				json.dump(self.json_data, outfile)
		else:
			print('No data to write to file.')

	def to_leafletmap(self):
		'''method to create a basic leafley app to visualize data'''
		if not os.path.exists('leaflet_map'):
			copy_tree(os.path.dirname(os.path.abspath(__file__)) + '/leaflet_source', './leaflet_map')
			if self.json_data['crs']['properties']['name'] != "EPSG:4326":
				self.project_espg4326()
				return 'Leaflet map successfully created in /leaflet_map - follow instructions.txt'
			self.to_geojson('./leaflet_map/layers/layer1.geojson')
			return 'Leaflet map successfully created in /leaflet_map - follow instructions.txt'
		return 'dir /leaflet_map exists, please delete or rename'

	def to_gdf(self):
		'''method that converts geojson into a geopandas dataframe.. hacky temp method due to gpd not supporting the 
		ability to read geojson straight from memory from inital look.'''
		self.to_json('temp1xyz.json')
		df = gpd.read_file('temp1xyz.json')
		os.remove('temp1xyz.json')
		return df

	def to_shp(self, shpname: str):
		'''method that converts geojson to .shp file'''
		gdf = self.to_gdf()
		gdf.to_file(driver='ESRI Shapefile', filename=shpname)

	def project_espg4326(self):
		'''method to reproject geojson for plotting in leaflet'''
		df = self.to_gdf()
		df_84 = df.to_crs({'init': 'epsg:4326'})
		df_84.to_file('./leaflet_map/layers/layer1.geojson', driver='GeoJSON')

def main():
	esrijson = GetESRIJSON('http://arcgis4.roktech.net/arcgis/rest/services/Durham/query/MapServer/86/query')
	print(esrijson.version)
	esrijson.getgeojson()
	# print(esrijson.geojson.featurecount())
	#esrijson.geojson.to_json('file1.json')
	#print(esrijson.geojson.to_shp('test1.shp'))
	print(esrijson.geojson.to_leafletmap())
	# print(esrijson.json_data.featurecount())

if __name__ == '__main__':
	main()