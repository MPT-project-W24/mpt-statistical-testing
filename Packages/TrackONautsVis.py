import json
import os
from os import listdir, getcwd, chdir
from os.path import isfile, join

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from Packages import data_separation

sns.set_style("white") #set seaborn visualization style



def position_plot(data, x="X", y="Y", title="Particle Position", x_bounds=None, y_bounds=None):
    """
    function that plots scatter of particle position and colorcode based on quality
    
    INPUTs
        data: quality-sorted dataframe of the video of interest
        x: x-axis of plot; takes in "X" column from dataframe
        y: y-axis of plot; takes in "Y" column from dateframe
        x_bounds: boundary of x-axis; takes in two numbers (int or float) in the form of a list; if not specified, default is autoscale
        y_bounds: boundary of y-axis; takes in two numbers (int or float) in the form of a list; if not specified, default is autoscale

    OUTPUTs:
        scatter plot of particle position colorcoded based on quality
    """
    fig, ax = plt.subplots()
    sns.scatterplot(
                data=data,
                x="X", y="Y",
                hue="Category",
                )

    if x_bounds:
        plt.xlim(x_bounds)
    if y_bounds:
        plt.ylim(y_bounds)

    plt.title("Particle Position")
    plt.xlabel("X Position", labelpad=10)
    plt.ylabel("Y Position", labelpad=10)
    plt.show()

    return fig



def pairwise_plot(data):
    """
    function that plots all pairwise plots between each column in dataframe

    INPUTs
        data: quality-sorted dataframe of the video of interest

    OUTPUTs
        scatter plots of all pairwise plots between each column, # of total plots = (# of columns minus 1) ^2 
    """
    #fig, ax = plt.subplots()
    fig = sns.pairplot(data=data, hue="Category")
    
    plt.show()
    return fig



def pair_plot(data, feature1="", feature2=""):
    """
    function to plot scatter plot of two specified features and corresponding distribution

    INPUTs
        data: quality-sorted dataframe of the video of interest
        feature1: x-axis of plot; takes in a feature column from dataframe
        feature2: y-axis of plot; takes in another feature column from dateframe 

    OUTPUTs
        scatter plot of two specified features and their corresponding distribution colorcoded based on quality
    
    """
    #fig, ax = plt.subplots()
    fig = sns.jointplot(data=data,
                  x=feature1, y=feature2,
                  hue="Category")
    plt.show()
    return fig



def violin_plot(data, feature=""):
    """
    function to plot violin plot of specified feature and grouped by quality

    INPUTs
        data: quality-sorted dataframe of the video of interest
        feature: feature of interest

    OUTPUTs
        violin plot of specified feature grouped by feature quality
    """
    #fig, ax = plt.subplots()
    sns.violinplot(
        data=data, y=feature, hue="Category")
    
    plt.xlabel("Feature Quality", labelpad=10)
    plt.ylabel(feature, labelpad=10)
    plt.show()
    return fig