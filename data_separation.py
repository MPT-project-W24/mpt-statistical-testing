
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import listdir, getcwd, chdir
from os.path import isfile, join
import json
import os

def read_feature(feature_data_path, feature_files):
    '''
    Read feature data using original feature_data_path and selected feature_files. 
    rename each file using the names in feature_files without .csv
    put file name and feature data in a dictionary named "feature_data"
    '''
    
    feature_data = {}
    for item in feature_files:
        file_path = os.path.join(feature_data_path, item)
        #rename
        file_name = os.path.splitext(item)[0]
        df = pd.read_csv(file_path)
        feature_data[file_name] = df
    return feature_data


def filter_feature(feature_list, feature_data_path, feature_files):
    '''
    Filtered feature data by selected list
    put filtered feature data into a dictionary named "feature_data_filtered"
    '''
    
    feature_data = read_feature(feature_data_path, feature_files)
    feature_data_filtered = {}
    for key in feature_data:
        feature_data_filtered[key] = feature_data[key][feature_list + ['Track_ID', 'X', 'Y', 'frames']]
    return feature_data_filtered


def remove_nans_feature(feature_list, feature_data_path, feature_files):
    '''
    Remove nans in filtered feature data
    put nans removed feature data into a dictionary named "feature_data_removed_nans"
    '''
    
    feature_data_filtered = filter_feature(feature_list, feature_data_path, feature_files)
    feature_data_removed_nans = {}
    for key in feature_data_filtered:
        feature_data_removed_nans[key] = feature_data_filtered[key][~feature_data_filtered[key][list(set(feature_list) - set(['Deff2', 'Mean Deff2']))].isin([np.nan, np.inf, -np.inf]).any(1)]
        feature_data_removed_nans[key] = feature_data_removed_nans[key].reset_index(drop=True)
    return feature_data_removed_nans


def read_json(json_data, feature_list, feature_data_path, feature_files):
    '''
    Read json data in the order of feature_data_removed_nans
    put json data into a dictionary named "json_data_new"
    '''
    
    feature_data_removed_nans = remove_nans_feature(feature_list, feature_data_path, feature_files)
    quality_data = {}
    for key in feature_data_removed_nans:
        quality_data[key] = json_data['/'+ key + '.csv']
    return quality_data

def put_together(json_data, feature_list, feature_data_path, feature_files):
    '''
    Combine removed nans data and quality data together
    seperate the quality data in removed nans data using "catagory"
    put combined data into a dictionary named "quality_feature"
    
    In the quality_feature, (-0.001, 0.333] is low, (0.333, 0.667] is medium, and (0.667, 1.0] is high
    '''
    feature_data_removed_nans = remove_nans_feature(feature_list, feature_data_path, feature_files)
    quality_data = read_json(json_data, feature_list, feature_data_path, feature_files)
    category_labels = ['low', 'medium', 'high']
    
    quality_feature = {}
    
    for key in feature_data_removed_nans:
        feature_data_removed_nans[key]['Quality'] = quality_data[key]
        feature_data_removed_nans[key]['Category'] = pd.cut(feature_data_removed_nans[key]['Quality'], bins=3, labels=category_labels)
        quality_feature[key] = feature_data_removed_nans[key]
    return quality_feature


