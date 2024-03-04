import json
import os
from os import listdir, getcwd, chdir
from os.path import isfile, join

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import data_separation

def position_plot(data, x="X", y="Y"):
    """function to plot scatter of particle position and colorcode based on quality"""
    sns.relplot(
                data=data,
                x="X", y="Y",
                hue="Category")
    plt.xlabel("X Position", labelpad=10)
    plt.ylabel("Y Position", labelpad=10)
    plt.show()
    return

def zoom_position_plot(data, x="X", y="Y", x_bounds=None, y_bounds=None):
    """function to plot scatter of particle position,
    colorcode based on quality,
    and zoom in to area of interest with x and y bound inputs"""
    sns.relplot(
                data=data,
                x="X", y="Y",
                hue="Category")
    
    if x_bounds:
        plt.xlim(x_bounds)
    if y_bounds:
        plt.ylim(y_bounds)
    
    plt.xlabel("X Position", labelpad=10)
    plt.ylabel("Y Position", labelpad=10)
    plt.show()
    return

def pairwise_plot(data):
    """plot all pairwise plots between each column"""
    sns.pairplot(data=features_df, hue="Category")
    plt.show()
    return

def pair_plot(data, x, y):
    """function to plot scatter plot of two specified features and corresponding distribution"""
    sns.jointplot(
    data=data,
    x=x, y=y,
    hue="Category")
    return

def violin_plot(data, x):
    """function to plot violin plot of specified column"""
    sns.violinplot(
        data=data, y=x, hue="Category")
    
    plt.xlabel("Data Quality", labelpad=10)
    plt.ylabel(x, labelpad=10)
    plt.show()
    return