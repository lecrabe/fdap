import os
import ee

import modules.image_prep as image_prep
import modules.area_stats as area_stats

dataset_id = 10

ee.Initialize()

# Import the dataset; a collection of composite granules from 2019.
oil_palm_descals_raw = ee.ImageCollection('BIOPAMA/GlobalOilPalm/v1');

# Select the classification band and mosaic all of the granules into a single image.
oil_palm_descals_mosaic = oil_palm_descals_raw.select('classification').mosaic();

# Visualisation only - not needed: create a mask to add transparency to non-oil palm plantation class pixels.
mask = oil_palm_descals_mosaic.neq(3);

mask = mask.where(mask.eq(0), 0.6); #not sure about this - from online (check)

oil_palm_descals_binary = oil_palm_descals_mosaic.lte(2) #choosing to ignore

oil_palm_descals_binary_area_hectares = area_stats.binary_to_area_hectares(oil_palm_descals_binary)

oil_palm_descals_binary_area_hectares = area_stats.set_scale_property_from_image(oil_palm_descals_binary_area_hectares,oil_palm_descals_raw.first(),0,debug=True).set("dataset_id",dataset_id)
