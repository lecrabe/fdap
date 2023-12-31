import os
import ee

import modules.image_prep as image_prep
import modules.area_stats as area_stats

dataset_id = 2

ee.Initialize()

esri_lulc10 = ee.ImageCollection(
    "projects/sat-io/open-datasets/landcover/ESRI_Global-LULC_10m_TS");

esri_lulc10_2020 = esri_lulc10.filterDate('2020-01-01','2020-12-31').map(
    lambda image:
    image.remap([1,2,4,5,7,8,9,10,11],
                [1,2,3,4,5,6,7,8,9])).mosaic()

esri_trees_2020 = esri_lulc10_2020.eq(2) #get trees    NB check flooded veg class

esri_trees_2020_area_hectares = area_stats.binary_to_area_hectares(
    esri_trees_2020)

esri_trees_2020_area_hectares = area_stats.set_scale_property_from_image(
    esri_trees_2020_area_hectares,esri_lulc10.first(),0,debug=True).set("dataset_id",dataset_id)

