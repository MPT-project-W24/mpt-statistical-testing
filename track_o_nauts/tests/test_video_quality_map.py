import unittest
from unittest.mock import patch

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from track_o_nauts.video_quality_map import merge_data, trajectory_plot, zoom_trajectory_plot, distruibution_by_age
import random
import track_o_nauts

class TestPlotFunctions(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(track_o_nauts.__path__[0], "test_data")
        self.feature_path = os.path.join(file_path, "feature_data")
        self.msd_path = os.path.join(file_path, "msd_data")
        self.json_path = os.path.join(file_path, "json_file/15_models_10_percent.json")
        vid_codes = []
        for f1 in os.listdir(self.feature_path):
            if f1.endswith('.csv'):
                # Extract the tail in feature file
                feature_tail = f1.split('_',1)[1].split('.')[0]
                
                # Iterate over each file in msd
                for f2 in os.listdir(self.msd_path):
                    
                    # Extract the tail in msd file
                    msd_tail = f2.split('_',1)[1].split('.')[0]
            
                    # If tails are the same
                    if feature_tail == msd_tail:
            
                        # Add tail into video_codes list
                        vid_codes.append(msd_tail)
        self.codes = vid_codes
        self.merge_df,_,_ = merge_data(self.feature_path, self.msd_path, self.json_path)
   
    def test_basic_functionality(self):
            [df, msd_data, quality_data] = merge_data(self.feature_path, self.msd_path, self.json_path)
            self.assertIsInstance(df, dict)
            self.assertIsInstance(msd_data, dict)
            self.assertIsInstance(quality_data, dict)

    def test_input_validation(self):
        # Test with invalid paths
        with self.assertRaises(Exception):
            merge_data("invalid/path", self.msd_path, self.json_path)
            merge_data(self.feature_path, "invalid/path", self.json_path)
            merge_data(self.feature_path, self.msd_path, "invalid/path")


    def test_data_integrity(self):
        df, _, _ = merge_data(self.feature_path, self.msd_path, self.json_path)
        # Number of columns = 45
        for key in df.keys():
            self.assertEqual(df[key].shape[1], 45)

    def test_expected_columns(self):
        df, _, _ = merge_data(self.feature_path, self.msd_path, self.json_path)
        expected_columns = ['Unnamed: 0', 'Frame', 'Gauss', 'MSDs', 'Mean_Intensity', 'Quality_x',
                            'SN_Ratio', 'Track_ID', 'X', 'Y', 'alpha', 'D_fit', 'kurtosis',
                            'asymmetry1', 'asymmetry2', 'asymmetry3', 'AR', 'elongation',
                            'boundedness', 'fractal_dim', 'trappedness', 'efficiency',
                            'straightness', 'MSD_ratio', 'Deff1', 'Deff2', 'Mean alpha',
                            'Mean D_fit', 'Mean kurtosis', 'Mean asymmetry1', 'Mean asymmetry2',
                            'Mean asymmetry3', 'Mean AR', 'Mean elongation', 'Mean boundedness',
                            'Mean fractal_dim', 'Mean trappedness', 'Mean efficiency',
                            'Mean straightness', 'Mean MSD_ratio', 'Mean Deff1', 'Mean Deff2',
                            'frames', 'Quality_y', 'Category']  # List of expected columns
        for key in df.keys():    
            self.assertCountEqual(list(df[key].columns), expected_columns)

    
            
    def test_trajectory_plot(self):
        vid_code = random.choice(self.codes)

        with patch("video_quality_map.plt.show") as show_patch, \
            patch("video_quality_map.plt.title") as title_patch, \
            patch("video_quality_map.plt.legend") as legend_patch:

            trajectory_plot(self.merge_df, vid_code)
            # Test if the plot is called
            assert show_patch.called

            # Test if it is the right title
            title_patch.assert_called_once_with('Trajectories of Particles in Video ' + vid_code)        

            # Test if legend is called
            legend_patch.assert_called_once()


    def test_zoom_trajectory_plot(self):
        vid_code = random.choice(self.codes)
        
        df = self.merge_df[vid_code]
        x1 = random.randint(0, int(max(df['X'].dropna(), default = 0)))
        x2 = random.randint(0, int(max(df['X'].dropna(), default = 0)))
        y1 = random.randint(0, int(max(df['Y'].dropna(), default = 0)))
        y2 = random.randint(0, int(max(df['Y'].dropna(), default = 0)))

        with patch("video_quality_map.plt.show") as show_patch, \
            patch("video_quality_map.plt.title") as title_patch, \
            patch("video_quality_map.plt.legend") as legend_patch:

            zoom_trajectory_plot(self.merge_df, vid_code, x1, x2, y1, y2)
            # Test if the plot is called
            assert show_patch.called

            # Test if it is the right title
            title_patch.assert_called_once_with('Zoom Trajectories of Particles in Video ' + vid_code)        

            # Test if legend is called
            legend_patch.assert_called_once()

    def test_distruibution_by_age(self):
        _, _, quality_data = merge_data(self.feature_path, self.msd_path, self.json_path)
        
        with patch("video_quality_map.plt.show") as show_patch, \
            patch("video_quality_map.plt.title") as title_patch, \
            patch("video_quality_map.plt.grid") as grid_patch:

            distruibution_by_age(self.feature_path, self.msd_path, quality_data)
            # Test if the plot is called
            assert show_patch.called

            # Test if it is the right title
            title_patch.assert_called_once_with('Mean Quality Score Distribution between Different Ages')      

            # Test if legend is called
            grid_patch.assert_called_once_with(True)
            

if __name__ == '__main__':
    unittest.main()
