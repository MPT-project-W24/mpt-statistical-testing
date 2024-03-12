import unittest
from unittest import TestCase
from Packages.data_separation import read_feature, filter_feature, remove_nans_feature, read_json,  put_together
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import listdir, getcwd, chdir
from os.path import isfile, join
import json
import os


class TestSeparation(unittest.TestCase):
    def test_read_feature_test1(self):
        test_feature_data = read_feature(feature_data_path, feature_files)
        for key, value in test_feature_data.items():
            self.assertIsInstance(value, pd.DataFrame, "Value is not a dataframe")        
    def test_read_feature_test2(self):
        test_feature_data = read_feature(feature_data_path, feature_files)
        num_of_keys = len(test_feature_data.keys())
        self.assertEqual(num_of_keys, 75, "Number of keys does not match")     
    def test_read_feature_test3(self):
        with self.assertRaises(TypeError):
            read_feature()
            
    def test_filter_feature_test1(self):
        with self.assertRaises(TypeError):
            filter_feature()
    def test_filter_feature_test2(self):
        test_filter_feature = filter_feature(feature_list, feature_data_path, feature_files)
        num_of_keys_filtered = len(test_filter_feature.keys())
        self.assertEqual(num_of_keys_filtered, 75, "Number of keys does not match") 
    def test_filter_feature_test3(self):
        test_filter_feature = filter_feature(feature_list, feature_data_path, feature_files)
        for key, value in test_filter_feature.items():
            self.assertEqual(value.shape[1] , 36, "Number of columns does not match")
            
    def test_remove_nans_test1(self):
        with self.assertRaises(TypeError):
            remove_nans_feature()
    def test_remove_nans_test2(self):
        test_remove_nans = remove_nans_feature(feature_list, feature_data_path, feature_files)
        num_of_keys_removed = len(test_remove_nans.keys())
        self.assertEqual(num_of_keys_removed, 75, "Number of keys does not match") 
    def test_remove_nans_test3(self):
        test_remove_nans = remove_nans_feature(feature_list, feature_data_path, feature_files)
        for key, value in test_remove_nans.items():
            self.assertEqual(value.shape[1] , 36, "Number of columns does not match")
            
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
            self.assertEqual(value.shape[1] , 38, "Number of columns does not match")
    def test_put_together_test3(self):
        test_put_together = put_together(json_data, feature_list, feature_data_path, feature_files)
        for key, value in test_put_together.items():
            self.assertIn('Quality', value.columns, 'Dataframe has a column named Quality')
            self.assertIn('Category', value.columns, 'Dataframe has a column named Category')
                
    
        
            
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
