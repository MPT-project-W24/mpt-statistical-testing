import unittest
# from unittest import TestCase
import track_o_nauts
from track_o_nauts.data_separation import read_feature, filter_feature, remove_nans_feature, read_json,  put_together
import pandas as pd
# import numpy as np
# from os import listdir, getcwd, chdir
from os import listdir
from os.path import isfile, join
import json
import os

feature_list = [
    'alpha',  # Fitted anomalous diffusion alpha exponenet
    'D_fit',  # Fitted anomalous diffusion coefficient
    'kurtosis',  # Kurtosis of track
    'asymmetry1',  # Asymmetry of trajecory (0 for circular symmetric, 1 for linear)
    'asymmetry2',  # Ratio of the smaller to larger principal radius of gyration
    'asymmetry3',  # An asymmetric feature that accnts for non-cylindrically symmetric pt distributions
    'AR',  # Aspect ratio of long and short side of trajectory's minimum bounding rectangle
    'elongation',  # Est. of amount of extension of trajectory from centroid
    'boundedness',  # How much a particle with Deff is restricted by a circular confinement of radius r
    'fractal_dim',  # Measure of how complicated a self similar figure is
    'trappedness',  # Probability that a particle with Deff is trapped in a region
    'efficiency',  # Ratio of squared net displacement to the sum of squared step lengths
    'straightness',  # Ratio of net displacement to the sum of squared step lengths
    'MSD_ratio',  # MSD ratio of the track, 'frames', Number of frames the track spans
    'Deff1',  # Effective diffusion coefficient at 0.33 s
    'Deff2',  # Effective diffusion coefficient at 3.3 s
    'Mean alpha',
    'Mean D_fit',
    'Mean kurtosis',
    'Mean asymmetry1',
    'Mean asymmetry2',
    'Mean asymmetry3',
    'Mean AR',
    'Mean elongation',
    'Mean boundedness',
    'Mean fractal_dim',
    'Mean trappedness',
    'Mean efficiency',
    'Mean straightness',
    'Mean MSD_ratio',
    'Mean Deff1',
    'Mean Deff2',
    ]
file_path = os.path.join(track_o_nauts.__path__[0], 'test_data')
feature_data_path = os.path.join(file_path, 'feature_data')
feature_files = [f for f in listdir(feature_data_path) if isfile(join(feature_data_path, f)) and '.csv' in f and 'P' in f]
json_filepath = os.path.join(file_path, 'json_file/15_models_10_percent.json')
f1 = open(json_filepath, 'r')
json_data = json.load(f1)
f1.close()


class TestSeparation(unittest.TestCase):
    def test_read_feature_test1(self):
        test_feature_data = read_feature(feature_data_path, feature_files)
        for key, value in test_feature_data.items():
            self.assertIsInstance(value, pd.DataFrame, "Value is not a dataframe")

    def test_read_feature_test2(self):
        test_feature_data = read_feature(feature_data_path, feature_files)
        num_of_keys = len(test_feature_data.keys())
        self.assertEqual(num_of_keys, 5, "Number of keys does not match")

    def test_read_feature_test3(self):
        with self.assertRaises(TypeError):
            read_feature()

    def test_filter_feature_test1(self):
        with self.assertRaises(TypeError):
            filter_feature()

    def test_filter_feature_test2(self):
        test_filter_feature = filter_feature(feature_list, feature_data_path, feature_files)
        num_of_keys_filtered = len(test_filter_feature.keys())
        self.assertEqual(num_of_keys_filtered, 5, "Number of keys does not match")

    def test_filter_feature_test3(self):
        test_filter_feature = filter_feature(feature_list, feature_data_path, feature_files)
        for key, value in test_filter_feature.items():
            self.assertEqual(value.shape[1], 36, "Number of columns does not match")

    def test_remove_nans_test1(self):
        with self.assertRaises(TypeError):
            remove_nans_feature()

    def test_remove_nans_test2(self):
        test_remove_nans = remove_nans_feature(feature_list, feature_data_path, feature_files)
        num_of_keys_removed = len(test_remove_nans.keys())
        self.assertEqual(num_of_keys_removed, 5, "Number of keys does not match")

    def test_remove_nans_test3(self):
        test_remove_nans = remove_nans_feature(feature_list, feature_data_path, feature_files)
        for key, value in test_remove_nans.items():
            self.assertEqual(value.shape[1], 36, "Number of columns does not match")

    def test_read_json_test1(self):
        test_json = read_json(json_data, feature_list, feature_data_path, feature_files)
        self.assertIsInstance(test_json, dict, "read_json is not a dictionary")

    def test_read_json_test2(self):
        test_json = read_json(json_data, feature_list, feature_data_path, feature_files)
        for key, value in test_json.items():
            self.assertIsInstance(value, list, "Value is not a list")

    def test_read_json_test3(self):
        test_json = read_json(json_data, feature_list, feature_data_path, feature_files)
        for key, value in test_json.items():
            for element in value:
                self.assertLessEqual(element, 1, 'element in the list is less or equal than 1')

    def test_put_together_test1(self):
        test_put_together = put_together(json_data, feature_list, feature_data_path, feature_files)
        for key, value in test_put_together.items():
            self.assertIsInstance(value, pd.DataFrame, "Value is not a dataframe")

    def test_put_together_test2(self):
        test_put_together = put_together(json_data, feature_list, feature_data_path, feature_files)
        for key, value in test_put_together.items():
            self.assertEqual(value.shape[1], 38, "Number of columns does not match")

    def test_put_together_test3(self):
        test_put_together = put_together(json_data, feature_list, feature_data_path, feature_files)
        for key, value in test_put_together.items():
            self.assertIn('Quality', value.columns, 'Dataframe has a column named Quality')
            self.assertIn('Category', value.columns, 'Dataframe has a column named Category')


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
