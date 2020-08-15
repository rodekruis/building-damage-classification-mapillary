import geopandas as gpd
from tqdm import tqdm
import pandas as pd
import os
import json
import copy
import random

df_image = gpd.read_file('images_smallest.geojson')
df_image['captured_at'] = pd.to_datetime(df_image['captured_at'])
df_image = df_image[df_image['captured_at'] > '2020-08-04']
# df_image.to_file('data/images.geojson', driver='GeoJSON')

# damage_classes = ['window_damage', 'wall_damage', 'balcony_damage', 'severe_structural_damage', 'other_damage', 'debris']
#
# df_image.index = df_image['key']
# df_image = df_image.drop(columns=['key'])
#
# for batch in range(15):
#
#     df_image_batch = df_image.copy()
#
#     # find unique annotators
#     if batch == 1:
#         files = [x for x in os.listdir('results') if 'batch_' + str(batch) + '_' in x.lower()]
#     else:
#         files = [x for x in os.listdir('results') if 'batch_'+str(batch) in x.lower()]
#     names = list(set([x.split('.')[0].split('_')[-1] for x in files]))
#     num_annotators = len(names)
#     map_names_ids = {name: i for i, name in enumerate(names)}
#     print('batch', batch, 'unique annotators', names)
#     print(map_names_ids)
#     batch_keys = []
#
#     for i in range(num_annotators):
#         for damage_class in damage_classes:
#             df_image_batch[damage_class + '_' + str(i)] = False
#
#     for file in files:
#
#         name = file.split('.')[0].split('_')[-1]
#         annotator_id = map_names_ids[name]
#
#         with open('results/'+file) as json_file:
#             data = json.load(json_file)
#
#         for image in data['_via_img_metadata']:
#             labels = data['_via_img_metadata'][image]['file_attributes']['damage_labels']
#             for damage_class in damage_classes:
#                 if damage_class in labels.keys():
#                     df_image_batch.at[image, damage_class+'_'+str(annotator_id)] = True
#         batch_keys = list(data['_via_img_metadata'])
#
#     # filter only batch images
#     df_image_batch = df_image_batch[df_image_batch.index.isin(batch_keys)]
#
#     # merge
#     for damage_class in damage_classes:
#         df_image_batch[damage_class+'_merged'] = 'no damage'
#
#     for image in df_image_batch.index:
#         df = df_image_batch.loc[image].copy()
#         for damage_class in damage_classes:
#             labels = [damage_class+'_'+str(i) for i in range(num_annotators)]
#             values = df[labels].values
#             # values = [bool(random.getrandbits(1)) for x in values]
#             if any(values):
#                 df_image_batch.at[image, damage_class + '_merged'] = 'possible damage'
#             if all(values):
#                 df_image_batch.at[image, damage_class + '_merged'] = 'confirmed damage'
#
#     # save
#     print('finished processing batch', batch, len(df_image_batch))
#     if len(df_image_batch) > 0:
#         df_image_batch.to_file('results_processed/results_batch_'+str(batch)+'.geojson', driver='GeoJSON')
#
# # merge results from all batches
# gdf_results = gpd.GeoDataFrame()
# for file in os.listdir('results_processed'):
#     gdf_batch = gpd.read_file('results_processed/'+file)
#     gdf_results = gdf_results.append(gdf_batch, ignore_index=True)
#
# # save one layer per damage class
# gdf_merged = gpd.GeoDataFrame()
# gdf_merged['key'] = gdf_results['key']
# gdf_merged['geometry'] = gdf_results['geometry']
# gdf_merged['captured_at'] = gdf_results['captured_at']
# for damage_class in damage_classes:
#     gdf_results_class = gdf_results[['key', damage_class+'_merged', 'geometry', 'captured_at']]
#     gdf_results_class = gdf_results_class.rename(columns={damage_class+'_merged': damage_class})
#     gdf_results_class.to_file('results_delivery/results_'+damage_class+'.geojson', driver='GeoJSON')
#     gdf_merged[damage_class] = gdf_results_class[damage_class]
#
# damage_classes = ['window_damage', 'wall_damage', 'balcony_damage', 'severe_structural_damage', 'other_damage', 'debris']
#
# # create merged layer
# gdf_merged['damage'] = "no damage"
# light_stuff = ['other_damage', 'debris']
# medium_stuff = ['window_damage', 'wall_damage', 'balcony_damage']
# heavy_stuff = ['severe_structural_damage']
#
# for ix, row in gdf_merged.iterrows():
#     # print(row)
#     if any(['confirmed damage' in row[x] for x in light_stuff]) or any(['possible damage' in row[x] for x in medium_stuff]):
#         gdf_merged.at[ix, 'damage'] = "light damage"
#     if any(['confirmed damage' in row[x] for x in medium_stuff]) or any(['possible damage' in row[x] for x in heavy_stuff]):
#         gdf_merged.at[ix, 'damage'] = "moderate damage"
#     if any(['confirmed damage' in row[x] for x in heavy_stuff]):
#         gdf_merged.at[ix, 'damage'] = "severe damage"
#     # print('RESULTS', gdf_merged.loc[ix, 'damage'])
#
# gdf_merged = gdf_merged.drop(columns=light_stuff+medium_stuff+heavy_stuff)
# gdf_merged = gdf_merged[['key', 'damage', 'geometry', 'captured_at']]
# gdf_merged.to_file('results_delivery/results_merged.geojson', driver='GeoJSON')


