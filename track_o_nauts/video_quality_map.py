import json
import os
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from track_o_nauts.data_separation import read_feature, put_together


def merge_data(feature_path, msd_path, json_path):
    ''' Merge Data Quality & MSD Data into ONE:
    [REQUIRED TO RUN BEFORE ADVANCING TO PLOT]

    INPUTs:
        'feature_path' - path to directory containing feature data files
        'msd_path' - path to directory containing msd files
        'json_path' - path to json file

    OUTPUTs:
        'df' - merging feature qualities & msd, excluding X & Y in feature
        'msd_data' - dict of the msd data for all videos
        'data_quality' - dict of the feature quality for all videos
    '''
    # Sort the data into categories: high, low, medium
    with open(json_path) as json_file:
        json_data = json.load(json_file)
    feature_list = [
                    'alpha',
                    'D_fit',
                    'kurtosis',
                    'asymmetry1',
                    'asymmetry2',
                    'asymmetry3',
                    'AR',
                    'elongation',
                    'boundedness',
                    'fractal_dim',
                    'trappedness',
                    'efficiency',
                    'straightness',
                    'MSD_ratio',
                    'Deff1',
                    'Deff2',
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

    feature_files = [
                    f for f in listdir(feature_path)
                    if isfile(join(feature_path, f))
                    and '.csv' in f and 'P' in f
                    ]

    # Apply put_together:
    quality_data = put_together(json_data, feature_list,
                                feature_path, feature_files)

    # Import msd file:
    msd_files = [
                f for f in listdir(msd_path)
                if isfile(join(msd_path, f))
                and '.csv' in f and 'P' in f
                ]
    msd_data = read_feature(msd_path, msd_files)

    # Extracting VIDEO CODES:

    # Create empty var
    vid_codes = []
    # Iterate over each file in feature
    for file_1 in os.listdir(feature_path):
        if file_1.endswith('.csv'):
            # Extract the tail in feature file
            feature_tail = file_1.split('_', 1)[1].split('.')[0]

            # Iterate over each file in msd
            for file_2 in os.listdir(msd_path):

                # Extract the tail in msd file
                msd_tail = file_2.split('_', 1)[1].split('.')[0]

                # If tails are the same
                if feature_tail == msd_tail:

                    # Add tail into video_codes list
                    vid_codes.append(msd_tail)

    # Merge feature quality and msd into 1 table
    # Create an empty dictionary
    merge_df = {}
    for code in vid_codes:
        merge_df[code] = pd.merge(
                                msd_data['msd_' + code],
                                quality_data['features_' + code].drop(columns=['X', 'Y']),
                                on='Track_ID', how='left'
                                )
    return merge_df, msd_data, quality_data


def trajectory_plot(merge_df, vid_code, save=None):
    '''
    Plot TRAJECTORIES of ALL PARTICLES in ONE VIDEO

    INPUTs:
        'merge_df' - merge data from previous function
        'vid_code' - code name of the video of interest (ex: 'P14_40nm_s1_v3')
        'save' (optional)
            - if None: not saving the plot as image
            - if not None (for example, 0) : saving the plot as .png image
    OUTPUT:
        A plot with all trajectories of all particles color-coded based on qualities.

    '''
    df = merge_df[vid_code]

    # Separate data based on Category
    low_y = df[df['Category'] == 'low']
    med_y = df[df['Category'] == 'medium']
    high_y = df[df['Category'] == 'high']
    null_y = df[df['Category'] is None]

    # Color coded the X Y based on quality sort
    # green-high, yellow-medium, red-low, purple-NaN

    # Plot
    plt.figure(figsize=(8, 8))

    plt.plot(low_y['X'], low_y['Y'], color='red', label='Low')
    plt.plot(med_y['X'], med_y['Y'], color='yellow', label='Medium')
    plt.plot(high_y['X'], high_y['Y'], color='green', label='High')
    plt.plot(null_y['X'], null_y['Y'], color='grey', label='Unclassified')

    plt.legend()
    plt.title('Trajectories of Particles in Video ' + vid_code)
    plt.show()

    if save is None:
        pass
    else:
        plt.savefig('trajectories_of_' + vid_code + '.png')

# Zoom into the section of interested


def zoom_trajectory_plot(merge_df, vid_code, x_1, x_2, y_1, y_2, save=None):

    '''
    Plot TRAJECTORIES of ALL PARTICLES in ONE VIDEO

    INPUTs:
        'merge_df' - merge data from previous function
        'vid_code' - code name of the video of interest (ex: 'P14_40nm_s1_v3')
        'x1,x2,y1,y2' - specify the area that you want to look at (x1<x2, y1<y2)
        'save' (optional)
                - if None: not saving the plot as image
                - if not None (for example, 0) : saving the plot as .png image
    OUTPUT:
        A plot with all trajectories of all particles color-coded based on qualities.

    '''

    df = merge_df[vid_code]

    # Separate data based on Category
    low_y = df[df['Category'] == 'low']
    med_y = df[df['Category'] == 'medium']
    high_y = df[df['Category'] == 'high']
    null_y = df[df['Category'] is None]

    # Plot
    plt.figure(figsize=(8, 8))

    plt.plot(low_y['X'], low_y['Y'], color='red', label='Low')
    plt.plot(med_y['X'], med_y['Y'], color='yellow', label='Medium')
    plt.plot(high_y['X'], high_y['Y'], color='green', label='High')
    plt.plot(null_y['X'], null_y['Y'], color='grey', label='Unclassified')

    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Zoom Trajectories of Particles in Video ' + vid_code)

    # Zoom into only an area of interested of the plot
    if x_1 < x_2 and y_1 < y_2:
        plt.xlim(x_1, x_2)
        plt.ylim(y_1, y_2)
    elif x_1 > x_2 and y_1 < y_2:
        plt.xlim(x_2, x_1)
        plt.ylim(y_1, y_2)
    elif x_1 < x_2 and y_1 > y_2:
        plt.xlim(x_1, x_2)
        plt.ylim(y_2, y_1)
    elif x_1 > x_2 and y_1 > y_2:
        plt.xlim(x_2, x_1)
        plt.ylim(y_2, y_1)

    plt.grid(True)

    plt.show()

    if save is None:
        pass
    else:
        plt.savefig('zoom_trajectories_of_' + vid_code + '.png')


def distribution_by_age(feature_path, msd_path, quality_data, save=None):
    '''
    Plot MEAN QUALITY SCORE BY AGE

    INPUTs:
        'feature_path' - path to directory containing feature data files
        'msd_path' - path to directory containing msd files
        'quality_data' - data output from the first function
        'save' (optional)
                - if None: not saving the plot as image
                - if not None (for example, 0) : saving the plot as .png image
    OUTPUT:
        A swarmplot.

    '''

    # Extracting VIDEO CODES:

    # Create empty var
    vid_codes = []
    # Iterate over each file in feature
    for file_1 in os.listdir(feature_path):
        if file_1.endswith('.csv'):
            # Extract the tail in feature file
            feature_tail = file_1.split('_', 1)[1].split('.')[0]
            # Iterate over each file in msd
            for file_2 in os.listdir(msd_path):
                # Extract the tail in msd file
                msd_tail = file_2.split('_', 1)[1].split('.')[0]
                # If tails are the same
                if feature_tail == msd_tail:
                    # Add tail into video_codes list
                    vid_codes.append(msd_tail)
    # Extract & calculate mean score of each video
    qualities = {
                'Video': [],
                'Mean Quality Score': [],
                'Quality': [],
                'Age': []
                }
    for code in vid_codes:
        quality = quality_data['features_' + code]['Quality'].mean()
        qualities['Mean Quality Score'].append(quality)
        qualities['Video'].append(code)
        qualities['Age'].append(code[:3])
        if quality <= 0.333:
            qualities['Quality'].append('low')
        elif quality > 0.667:
            qualities['Quality'].append('high')
        else:
            qualities['Quality'].append('medium')

    df_qualities = pd.DataFrame(qualities)

    # Swarmplot
    plt.figure(figsize=[8, 5])

    # Draw a categorical scatterplot to show each observation
    sns.swarmplot(data=df_qualities,
                  x="Mean Quality Score", y="Quality", hue="Age",
                  order=['high', 'medium', 'low'],
                  hue_order=np.sort(df_qualities['Age'].unique()))

    plt.title('Mean Quality Score Distribution between Different Ages')
    plt.grid(True)
    plt.show()

    if save is not None:
        plt.savefig('Quality_score_distribution_by_age.png')
