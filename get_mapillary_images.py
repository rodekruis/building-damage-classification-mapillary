# -*- coding: utf-8 -*-
"""
Created on 2020-08-14
@author: Jacopo Margutti (jmargutti@redcross.nl)
"""

import json, requests
from time import sleep
import click

client = '<client-id>'
access_token = '<access-token>'

@click.command()
@click.option('--start_time', default='', help='filter by date')
@click.option('--bbox', default='', help='filter by bounding box with format long_start,lat_start,long_end,lat_end')
@click.option('--output_file', default='images/images.geojson', help='output file')
def get_mapillary_images(start_time, bbox, output_file):
    """
    get image ids and urls from Mapillary, save them as geojson
    """

    # initialize output file
    output = {"type": "FeatureCollection", "features": []}

    # call API
    url = 'https://a.mapillary.com/v3/images?client_id={}&per_page=100'.format(client)
    if start_time != '':
        url += '&start_time='+start_time
    if bbox != '':
        url += '&bbox={}'.format(bbox)
    print(url)
    r = requests.get(url, headers={'Authorization': 'Bearer {}'.format(access_token)})
    data = r.json()
    data_length = len(data['features'])
    for f in data['features']:
        output['features'].append(f)
    print("Total images: {}".format(len(output['features'])))
    retry_max_attempts = 10
    count_attempts = 0

    # loop over all result pages
    while data_length == 100:
        if 'next' in r.links.keys():
            print('opening next page')
            link = r.links['next']['url']
            r = requests.get(link, headers={'Authorization': 'Bearer {}'.format(access_token)})
            try:
                data = r.json()
            except:
                print('simplejson.errors.JSONDecodeError')
                data_length = 100
                continue
            if 'features' in data:
                for f in data['features']:
                    output['features'].append(f)
            else:
                print('ERROR: no images in data')
                print(data)
            print("Total images: {}".format(len(output['features'])))
            data_length = len(data['features'])
            count_attempts = 0
            sleep(1)
        elif count_attempts > retry_max_attempts:
            print('too many failed attempts, interrupting')
            data_length = 0
        else:
            print('no next page, retrying')
            count_attempts += 1
            sleep(5)
            r = requests.get(link, headers={'Authorization': 'Bearer {}'.format(access_token)})
            data_length = 100

    # save results
    with open(output_file, 'w') as outfile:
        print("finished, saving results to", output_file)
        json.dump(output, outfile)


if __name__ == "__main__":
    get_mapillary_images()
