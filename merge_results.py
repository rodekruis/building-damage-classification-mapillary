# -*- coding: utf-8 -*-
"""
Created on 2020-08-14
@author: Jacopo Margutti (jmargutti@redcross.nl)
"""

import geopandas as gpd
import os
import re
import json
import click
from labelling_project_config import labelling_options, light_features, medium_features, heavy_features

@click.command()
@click.option('--images', default='images/images.geojson', help='input images')
@click.option('--submissions', default='submissions', help='submissions directory')
@click.option('--output', default='results', help='output directory')
def merge_results(images, submissions, output):
    """merge submissions and create various layers"""

    df_image = gpd.read_file(images)
    df_image.index = df_image['key']
    df_image = df_image.drop(columns=['key'])

    damage_features = labelling_options.keys()

    os.makedirs(submissions+'-processed', exist_ok=True)
    sub_proc_dir = submissions+'-processed'

    num_batches = len(list(set([re.findall(r".*?_(\d+)_.*", x)[0] for x in os.listdir(submissions)])))
    print('found', num_batches, 'batches')

    # loop over batches
    for batch in range(num_batches):

        # initialize geodatframe for results
        df_image_batch = df_image.copy()

        # get files and annotator names of this batch
        files = [x for x in os.listdir(submissions) if str(batch) == re.findall(r".*?_(\d+)_.*", x)[0]]
        names = list(set([x.split('.')[0].split('_')[-1] for x in files]))
        num_annotators = len(names)
        map_names_ids = {name: i for i, name in enumerate(names)}
        print('processing batch', batch, 'unique annotators', names)
        batch_keys = []

        # initialize empty columns in results geodatframe
        for i in range(num_annotators):
            for damage_feature in damage_features:
                df_image_batch[damage_feature + '_' + str(i)] = False

        # merge results from different files
        for file in files:

            name = file.split('.')[0].split('_')[-1]
            annotator_id = map_names_ids[name]

            with open(submissions+'/'+file) as json_file:
                data = json.load(json_file)

            for image in data['_via_img_metadata']:
                labels = data['_via_img_metadata'][image]['file_attributes']['damage_labels']
                for damage_feature in damage_features:
                    if damage_feature in labels.keys():
                        df_image_batch.at[image, damage_feature+'_'+str(annotator_id)] = True
            batch_keys = list(data['_via_img_metadata'])

        # keep only images in batch
        df_image_batch = df_image_batch[df_image_batch.index.isin(batch_keys)]

        # merge results from the diferrent annotators
        for damage_feature in damage_features:
            df_image_batch[damage_feature+'_merged'] = 'no damage'

        for image in df_image_batch.index:
            df = df_image_batch.loc[image].copy()
            for damage_feature in damage_features:
                labels = [damage_feature+'_'+str(i) for i in range(num_annotators)]
                values = df[labels].values
                if any(values):
                    df_image_batch.at[image, damage_feature + '_merged'] = 'possible damage'
                if all(values):
                    df_image_batch.at[image, damage_feature + '_merged'] = 'confirmed damage'

        # save processed batch results
        print('finished processing batch', batch, 'with', len(df_image_batch), 'entries')
        if len(df_image_batch) > 0:
            df_image_batch.to_file(sub_proc_dir+'/results_batch_'+str(batch)+'.geojson', driver='GeoJSON')

    # merge results from all batches
    gdf_results = gpd.GeoDataFrame()
    for file in os.listdir(sub_proc_dir):
        gdf_batch = gpd.read_file(sub_proc_dir+'/'+file)
        gdf_results = gdf_results.append(gdf_batch, ignore_index=True)
    gdf_merged = gpd.GeoDataFrame()
    gdf_merged['key'] = gdf_results['key']
    gdf_merged['geometry'] = gdf_results['geometry']
    gdf_merged['captured_at'] = gdf_results['captured_at']

    # save one layer per damage feature
    for damage_feature in damage_features:
        gdf_results_feature = gdf_results[['key', damage_feature+'_merged', 'geometry', 'captured_at']]
        gdf_results_feature = gdf_results_feature.rename(columns={damage_feature+'_merged': damage_feature})
        gdf_results_feature.to_file(output+'/results_'+damage_feature+'.geojson', driver='GeoJSON')
        gdf_merged[damage_feature] = gdf_results_feature[damage_feature]

    # merge damage features in one layer, save it
    gdf_merged['damage'] = "no damage"
    for ix, row in gdf_merged.iterrows():
        if any(['confirmed damage' in row[x] for x in light_features]) or any(['possible damage' in row[x] for x in medium_features]):
            gdf_merged.at[ix, 'damage'] = "light damage"
        if any(['confirmed damage' in row[x] for x in medium_features]) or any(['possible damage' in row[x] for x in heavy_features]):
            gdf_merged.at[ix, 'damage'] = "moderate damage"
        if any(['confirmed damage' in row[x] for x in heavy_features]):
            gdf_merged.at[ix, 'damage'] = "severe damage"

    gdf_merged = gdf_merged.drop(columns=light_features+medium_features+heavy_features)
    gdf_merged = gdf_merged[['key', 'damage', 'geometry', 'captured_at']]
    gdf_merged.to_file(output+'/results_merged.geojson', driver='GeoJSON')


if __name__ == "__main__":
    merge_results()