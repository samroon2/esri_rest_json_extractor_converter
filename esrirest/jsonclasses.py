from distutils.dir_util import copy_tree
import geopandas as gpd
import fiona
import json
import os


class JSONDATA:
    '''Class for manipulating JSON.
    '''

    def __init__(self):
        self.json_data = {}

    def setter(self, indexnumber: int, jsondata: dict):
        '''Method to set assemble multiple json payloads into one file.

        :param indexnumber: Index of oidrange. If 0 then it will provide all spatial and schema info.
        :type indexnumber: int
        :param jsondata: JSON data extracted from the REST service API.
        :type jsondata: dict
        '''
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
        '''Method that returns the number if features in the dataset.'''
        if len(self.json_data) > 0:
            return len(self.json_data['features'])
        return 0

    def to_json(self, jsonfilename: str):
        '''Method for exporting data to a esri .json file.

        :param jsonfilename: The name of the json file to be exported. eg: somefile.json 
        :type jsonfilename: str
        '''
        if self.featurecount() > 0:
            with open(jsonfilename, "w") as outfile:
                json.dump(self.json_data, outfile)
        else:
            print('No data to write to file.')

class GEOJSON(JSONDATA):
    '''Class for manipulating GEOJSON
    '''

    def __init__(self):
        super().__init__()

    def to_geojson(self, jsonfilename: str):
        '''Method for exporting data to a .geojson file.

        :param jsonfilename: The name of the json file to be exported. eg: somefile.geojson
        :type jsonfilename: str
        '''
        if self.featurecount() > 0:
            with open(jsonfilename, "w") as outfile:
                json.dump(self.json_data, outfile)
        else:
            print('No data to write to file.')

    def to_leafletmap(self):
        '''Method to create a basic leaflet app to visualize data.
        '''
        if not os.path.exists('leaflet_map'):
            copy_tree(os.path.dirname(os.path.abspath(__file__)) + '/leaflet_source', './leaflet_map')
            if self.json_data['crs']['properties']['name'] != "EPSG:4326":
                self.project_espg4326()
                return 'Leaflet map successfully created in /leaflet_map - follow instructions.txt'
            self.to_geojson('./leaflet_map/layers/layer1.geojson')
            return 'Leaflet map successfully created in /leaflet_map - follow instructions in leaflet_map/instructions.txt'
        return 'dir /leaflet_map exists, please delete or rename'

    def to_gdf(self):
        '''Method that converts geojson into a geopandas dataframe.. hacky temp method due to gpd not supporting the 
        ability to read geojson straight from memory from inital look.'''
        self.to_json('temp1xyz.json')
        df = gpd.read_file('temp1xyz.json')
        os.remove('temp1xyz.json')
        return df

    def to_shp(self, shpname: str):
        '''Method that converts geojson to .shp file.

        :param shpname: The name of the shapefile to be exported. eg: somefile.shp
        :type shpname: str
        '''
        gdf = self.to_gdf()
        gdf.to_file(driver='ESRI Shapefile', filename=shpname)

    def project_espg4326(self):
        '''Method to reproject geojson for plotting in leaflet.
        '''
        df = self.to_gdf()
        df_84 = df.to_crs({'init': 'epsg:4326'})
        df_84.to_file('./leaflet_map/layers/layer1.geojson', driver='GeoJSON')