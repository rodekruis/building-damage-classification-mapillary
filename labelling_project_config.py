# -*- coding: utf-8 -*-
"""
Created on 2020-08-14
@author: Jacopo Margutti (jmargutti@redcross.nl)

CONFIGURATION FILE FOR LABELLING PROJECT
see readme at https://github.com/rodekruis/building-damage-classification-mapillary
"""

# labelling options (features and questions)
labelling_options = {"window_damage": "Are the windows damaged?",
                     "wall_damage": "Are the walls damaged?",
                     "balcony_damage": "Are the balconies damaged?",
                     "severe_structural_damage": "Is the building partially collapsed?",
                     "other_damage": "Any other damage not listed?",
                     "debris": "Is there debris?"}

# feature importance (for merging)
light_features = ['other_damage', 'debris']
medium_features = ['window_damage', 'wall_damage', 'balcony_damage']
heavy_features = ['severe_structural_damage']

