# -*- coding: utf-8 -*-
"""
Created on 2020-08-14
@author: Jacopo Margutti (jmargutti@redcross.nl)
"""

import geopandas as gpd
from tqdm import tqdm
import click
import json
import copy


def chunks(lst, n):
    """yield successive n-sized chunks from list"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


@click.command()
@click.option('--batch_size', default=100, help='batch size')
@click.option('--images', default='images/images.geojson', help='input file (images)')
@click.option('--dest', default='batches', help='output directory')
def generate_batches(batch_size, images, dest):
    """
    split images into batches and prepare one project per batch for Oxford VGG image annotator
    http://www.robots.ox.ac.uk/~vgg/software/via/via_demo.html
    """

    # get images
    df_image = gpd.read_file(images)
    keys = list(set(df_image['key'].tolist()))
    print('preparing batches from', len(keys), 'images')

    # prepare project template
    with open('labelling_project_template.json') as json_file:
        data = json.load(json_file)
        img_metadata = data['_via_img_metadata']
    img_metadata_template = data['_via_img_metadata']['image-id']
    data['_via_img_metadata'].pop('image-id')
    data['_via_attributes']['file'].pop('image_url')

    # split image ids (keys) into batches
    keys_batches = list(chunks(keys, batch_size))

    # loop over batches and generate projects
    for batch_number, batch in tqdm(enumerate(keys_batches)):
        data_batch = copy.deepcopy(data)
        data_batch['_via_attributes']['file']['location_url'] = {"type": "text",
                                                                 "description": "",
                                                                 "default_value": ""}
        # loop over images in batch
        for image_key in batch:
            # add image url and id
            image_url = "https://images.mapillary.com/"+image_key+"/thumb-2048.jpg"
            img_metadata = copy.deepcopy(img_metadata_template)
            img_metadata['filename'] = image_url
            # add googlemaps url with location
            img_geo = df_image[df_image['key'] == image_key].geometry.values[0]
            x, y = img_geo.x, img_geo.y
            image_url = 'https://www.google.com/maps/search/?api=1&query='+str(y)+','+str(x)
            img_metadata['file_attributes']['location_url'] = image_url
            # update batch project
            data_batch['_via_img_metadata'][image_key] = img_metadata

        data_batch['_via_image_id_list'] = batch

        # save batch
        with open(dest+'/labelling_project_batch_{}.json'.format(batch_number), 'w') as outfile:
            json.dump(data_batch, outfile)


if __name__ == "__main__":
    generate_batches()