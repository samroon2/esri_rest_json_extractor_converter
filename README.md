# esri_rest_json_extractor_converter
A library to extract features from esri rest services and easily convert extracted data to common spatial data types.<br />
Project allows for simple extraction, transformation and visualization of spatial data.

# Basic Usage

# Extract and Transform Spatial Data
Package allows for quick extraction and transformation into various other useful formats for geospatial analysis;
- Shapefiles (.shp)
- .json
- .geojson
- geopandas dataframes
- leaflet web application

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