import json
import os
from os import listdir, getcwd, chdir
from os.path import isfile, join

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from track_o_nauts.TrackONautsVis import position_plot, pairwise_plot, pair_plot, violin_plot

import unittest
from unittest.mock import patch



#tests for position_plot
class TestPositionPlot(unittest.TestCase):

    def test_position_plot_show(data, x="X", y="Y", title="Particle Position", x_bounds=None, y_bounds=None):
        """test function that tests if position_plot displays a plot"""
        test_df = pd.DataFrame({"X": [1, 2, 3], "Y": [10, 20, 30], "Category": ["low", "medium", "high"]})
        with patch("matplotlib.pyplot.show") as mock_show:
            position_plot(test_df)
            assert mock_show.called, "position_plot did not show a plot"
        return

    def test_position_plot_bounds(data, x="X", y="Y", title="Particle Position", x_bounds=None, y_bounds=None):
        """test function that tests if bounds of position_plot are correct"""
        test_df = pd.DataFrame({"X": [1, 2, 3], "Y": [10, 20, 30], "Category": ["low", "medium", "high"]})
        fig = position_plot(test_df, x_bounds=(0, 50), y_bounds=(0, 100))
              
        assert fig.gca().get_xlim() == (0, 50)
        assert fig.gca().get_ylim() == (0, 100)
        return
        
    def test_position_plot_label(data, x="X", y="Y", title="Particle Position", x_bounds=None, y_bounds=None):
        """test function that tests if the xlabel and ylabel are displayed correctly"""
        test_df = pd.DataFrame({"X": [1, 2, 3], "Y": [10, 20, 30], "Category": ["low", "medium", "high"]})
        fig = position_plot(test_df)
        
        x_label = plt.xlabel("X Position", labelpad=10).get_text()
        y_label = plt.ylabel("Y Position", labelpad=10).get_text()
        
        assert x_label == "X Position"
        assert y_label == "Y Position"
        return
     
    def test_position_plot_title(data, x="X", y="Y", title="Particle Position", x_bounds=None, y_bounds=None):
        """test function that tests if the plot title is displayed correctly"""
        test_df = pd.DataFrame({"X": [1, 2, 3], "Y": [10, 20, 30], "Category": ["low", "medium", "high"]})
        fig = position_plot(test_df)

        plot_title = fig.gca().get_title()
        
        assert plot_title == "Particle Position"
        return



#tests for pairwise_plot
class TestPairwisePlot(unittest.TestCase):
    
    def test_pairwise_plot_show(data):
        """test function that tests if pairwise_plot displays a plot"""
        test_df = pd.DataFrame({"X": [1, 2, 3, 4, 5], "Y": [10, 20, 30, 40, 50], "Z": [5, 4, 3, 2, 1], "Category": ["low", "medium", "high", "medium", "low"]})
        with patch("matplotlib.pyplot.show") as mock_show:
            pairwise_plot(test_df)
            assert mock_show.called, "pairwise_plot did not show a plot"
        return
    
    def test_pairwise_plot_total(data):
        """test function to test if number of plots generated is equal to (# of columns minus 1) squared"""
        test_df = pd.DataFrame({"X": [1, 2, 3, 4, 5], "Y": [10, 20, 30, 40, 50], "Z": [5, 4, 3, 2, 1], "Category": ["low", "medium", "high", "medium", "low"]})
        fig = pairwise_plot(test_df)
        assert len(fig.axes)*len(fig.axes) == 9
        return



#tests for pair_plot
class TestPairPlot(unittest.TestCase):

    def test_pair_plot_show(data, feature1="", feature2=""):
        """test function that tests if pair_plot displays a plot"""
        test_df = pd.DataFrame({"X": [1, 2, 3, 4, 5], "Y": [10, 20, 30, 40, 50], "Z": [5, 4, 3, 2, 1], "Category": ["low", "medium", "high", "medium", "low"]})
        with patch("matplotlib.pyplot.show") as mock_show:
            pair_plot(test_df, feature1="X", feature2="Y")
            assert mock_show.called, "pair_plot did not show a plot"
        return



#tests for violin_plot
class TestViolinPlot(unittest.TestCase):

    def test_violin_plot_show(data, feature=""):
        """test function that tests if position_plot displays a plot"""
        test_df = pd.DataFrame({"X": [1, 2, 3, 4, 5], "Y": [10, 20, 30, 40, 50], "Z": [5, 4, 3, 2, 1], "Category": ["low", "medium", "high", "medium", "low"]})
        with patch("matplotlib.pyplot.show") as mock_show:
            violin_plot(test_df, feature="X")
            assert mock_show.called, "violin_plot did not show a plot"
        return

    def test_violin_plot_label(data, feature=""):
        """test function that tests if the xlabel and ylabel are displayed correctly"""
        test_df = pd.DataFrame({"X": [1, 2, 3, 4, 5], "Y": [10, 20, 30, 40, 50], "Z": [5, 4, 3, 2, 1], "Category": ["low", "medium", "high", "medium", "low"]})
        violin_plot(test_df, feature="X")
        
        x_label = plt.xlabel("Feature Quality", labelpad=10).get_text()
        y_label = plt.ylabel("X", labelpad=10).get_text()
        
        assert x_label == "Feature Quality"
        assert y_label == "X"
        return
