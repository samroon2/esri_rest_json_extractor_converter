[![Build Status](https://travis-ci.org/samroon2/esri_rest_json_extractor_converter.svg?branch=master)](https://travis-ci.org/samroon2/esri_rest_json_extractor_converter)

# esri_rest_json_extractor_converter
A library that provides a simple interface to rapidly extract features from esri rest services and easily analyze, visualize and transform/convert extracted data to common spatial data types.

# Basic Usage

# Extract and Transform Spatial Data
Package allows for quick extraction and transformation into various other useful formats for geospatial analysis:
### shapefiles (.shp)
```python
Python 3.6.7 (default, Oct 22 2018, 11:32:17)
[GCC 8.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from esrirest import *
>>> esrijson = GetESRIJSON('http://arcgis4.roktech.net/arcgis/rest/services/DaytonaBeach/TRAKiT/MapServer/10/query')
http://arcgis4.roktech.net/arcgis/rest/services/?f=pjson
>>> esrijson.get_geojson()
100%|█████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.07s/it]
>>> esrijson.geojson.to_shp('geo')
```
### json
```python
Python 3.6.7 (default, Oct 22 2018, 11:32:17)
[GCC 8.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from esrirest import *
>>> esrijson = GetESRIJSON('http://arcgis4.roktech.net/arcgis/rest/services/DaytonaBeach/TRAKiT/MapServer/10/query')
http://arcgis4.roktech.net/arcgis/rest/services/?f=pjson
>>> esrijson.get_json()
100%|█████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.07s/it]
>>> esrijson.json.to_json('geo.json')
```
### geojson
```python
Python 3.6.7 (default, Oct 22 2018, 11:32:17)
[GCC 8.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from esrirest import *
>>> esrijson = GetESRIJSON('http://arcgis4.roktech.net/arcgis/rest/services/DaytonaBeach/TRAKiT/MapServer/10/query')
http://arcgis4.roktech.net/arcgis/rest/services/?f=pjson
>>> esrijson.get_json()
100%|█████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.07s/it]
>>> esrijson.json.to_json('geo.json')
```
### geopandas dataframes
From here there are many operations that can be done!
```python
Python 3.6.7 (default, Oct 22 2018, 11:32:17)
[GCC 8.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from esrirest import *
>>> esrijson = GetESRIJSON('http://arcgis4.roktech.net/arcgis/rest/services/DaytonaBeach/TRAKiT/MapServer/10/query')
http://arcgis4.roktech.net/arcgis/rest/services/?f=pjson
>>> esrijson.get_geojson()
100%|█████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.25s/it]
>>> df = esrijson.geojson.to_gdf()
>>> df.head()
  ORDNO COMMENTS FUTURELAND  ...  SHAPE_Length     SHAPE_Area                                           geometry
0                            ...     13.307423       1.857599  POLYGON ((-81.12917483670083 29.24560927860283...
1                            ...   1016.949755   62908.334167  POLYGON ((-81.07251013086136 29.20950544605223...
2                            ...   1488.026782   92858.290556  POLYGON ((-81.05419476950398 29.22426044349914...
3                            ...   2000.288684  141830.367828  POLYGON ((-81.04787515561615 29.22411983773626...
4                            ...    404.434934    8541.190741  POLYGON ((-81.0360225313309 29.22630174617694,...

[5 rows x 16 columns]
```
### leaflet web applications
```python
Python 3.6.7 (default, Oct 22 2018, 11:32:17)
[GCC 8.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from esrirest import *
>>> esrijson = GetESRIJSON('http://arcgis4.roktech.net/arcgis/rest/services/DaytonaBeach/TRAKiT/MapServer/10/query')
http://arcgis4.roktech.net/arcgis/rest/services/?f=pjson
>>> esrijson.get_geojson()
100%|█████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.25s/it]
>>> esrijson.geojson.to_leafletmap()
'Leaflet map successfully created in /leaflet_map - follow instructions in leaflet_map/instructions.txt'
```