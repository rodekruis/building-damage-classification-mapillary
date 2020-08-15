# building-damage-classification-mapillary
Building damage classification from Mapillary street-view images

## requirements
1. Python 3.7
2. many humans

Install needed modules with 
``` pip install -r requirements.txt```

Get humans from Jonath or Koos

## set-up
1. get client and access token for Mapillary API from Bitwarden
2. add them in ```get_mapillary_images.py```
3. get mapillary images
```
Usage: get_mapillary_images.py [OPTIONS]

Options:
  --start_time TEXT   filter by date
  --bbox TEXT         filter by bounding box [long_start, lat_start, long_end,
                      lat_end]

  --output_file TEXT  output file
  --help              Show this message and exit.
```
4. divide images in batches

