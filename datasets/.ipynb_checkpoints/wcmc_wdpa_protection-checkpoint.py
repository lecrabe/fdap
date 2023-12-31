import os
import ee

import modules.image_prep as image_prep
import modules.area_stats as area_stats
import modules.WDPA_prep as WDPA_prep

from datasets.template_images import template_image_1

ee.Initialize()

dataset_id = 13

wdpa_pnt = ee.FeatureCollection("WCMC/WDPA/current/points");

wdpa_poly = ee.FeatureCollection("WCMC/WDPA/current/polygons");

#apply filters and merge polygon with buffered points  
wdpa_filt = WDPA_prep.filterWDPA(wdpa_poly) ##.merge(WDPA_prep.filterWDPA(wdpa_pnt).filter(ee.Filter.gt('REP_AREA', 0)).map(WDPA_prep.bufferByArea));
#turn into image (no crs etc set currently)
wdpa_overlap = wdpa_filt.reduceToImage(['STATUS_YR'],'min');  #make into raster - remove mask if want 0s

#make binary
wdpa_binary = wdpa_overlap.lt(2070).unmask()


#reproject based on gfc data (approx 30m res which should be easily)
crs_template = template_image_1.select(0).projection().crs().getInfo()

wdpa_binary_reproj = wdpa_binary.reproject(
  crs= crs_template,
  scale= area_stats.get_scale_from_image(template_image_1),
).int8()

protected_areas_WDPA_area_hectares = area_stats.binary_to_area_hectares(wdpa_binary_reproj)

protected_areas_WDPA_area_hectares = area_stats.set_scale_property_from_image(protected_areas_WDPA_area_hectares,template_image_1,0,debug=True).set("dataset_id",dataset_id)
