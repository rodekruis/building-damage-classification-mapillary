# building-damage-classification-mapillary
Building damage classification from Mapillary street-view images

## introduction
Some scripts to organize the annotation of images from Mapillary.<br/> 
Used for building damage classification after the Beirut explosions of 2020-08-04.

Workflow:
1. get a list of relevant images
2. understand how you want to label them: which building features indicate damage? (e.g. windows, walls, etc.)
3. update the config file accordingly
4. split the images in N batches
5. have X annotators label each batch using the [Oxford VGG image annotator](http://www.robots.ox.ac.uk/~vgg/software/via/via_demo.html)
6. merge N*X submissions into one, according to some logic
7. save one vector file per feature
8. merge all features into one overall damage score, save it in a vector file

The damage labels (or features) and the corresponding questions are customizable. Default labels:
* `window_damage`: are the windows damaged?
* `wall_damage`: are the walls damaged?
* `balcony_damage`: are the balconies damaged?
* `severe_structural_damage`: is the building partially or entirely collapsed?
* `other_damage`: any other damage not listed?
* `debris`: is there debris?

The merging of multiple submissions from different annotators follows this logic, in pseudo-code
``` 
for each image and feature:
  if no annotator mentions it --> no damage
  if any annotator mentions it --> possible damage
  if all annotators mention it --> confirmed damage
```
The merging of multiple features into one overall damage score follows this logic, in pseudo-code
```
 for each image:
  default --> no damage
  if any light_feature is confirmed or any medium_feature is possible --> light damage
  if any medium_feature is confirmed or any heavy_feature is possible --> moderate damage
  if any heavy_feature is confirmed --> severe damage
 ```
 where `light`, `medium` and `heavy` refer to the importance of each feature. Default importance:
```
light_features = ['other_damage', 'debris']
medium_feature = ['window_damage', 'wall_damage', 'balcony_damage']
heavy_features = ['severe_structural_damage']
```

## requirements
1. Python 3.7
2. many humans

Install needed modules with 
``` pip install -r requirements.txt```

Get humans

## usage
1. get client and access token for Mapillary API from Bitwarden, add them in ```get_mapillary_images.py```
2. get mapillary images
```
Usage: get_mapillary_images.py [OPTIONS]

Options:
  --start_time TEXT   filter by date (example: 2020-08-04)
  --bbox TEXT         filter by bounding box long_start,lat_start,long_end,lat_end (example: 35.492308,33.883913,35.547162,33.918119)
  --output_file TEXT  output file (default: images/images.geojson)
  --help              Show this message and exit.
```
3. [OPTIONAL] update `labelling_project_config.py` with chosen damage labels (features) and their importance
4. split the images into batches
```
Usage: generate_batches.py [OPTIONS]

Options:
  --batch_size INTEGER  batch size (default 100)
  --images TEXT         input images (defaut: images/images.geojson)
  --dest TEXT           output directory (default: batches)
  --help                Show this message and exit.
```
5. label the batches, get all submissions and save them as `results_batch_<batch number>_<annotator name>.json`<br/>
(example: `results_batch_12_bob.json`)
6. merge submissions and generate results: one vector layer per feature and one vector layer with the overall damage score 
```
Usage: merge_results.py [OPTIONS]

Options:
  --images TEXT       input images (defaut: images/images.geojson)
  --submissions TEXT  submissions directory (default: submissions)
  --output TEXT       output directory (default: results)
  --help              Show this message and exit.
```

