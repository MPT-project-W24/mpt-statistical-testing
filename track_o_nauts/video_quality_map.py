from track_o_nauts.data_separation import read_feature, filter_feature, remove_nans_feature, put_together    
import os
from os import listdir, getcwd, chdir
from os.path import isfile, join
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def merge_data(feature_path, msd_path, json_path):
    ''' Merge Data Quality & MSD Data into ONE:
    [REQUIRED TO RUN BEFORE ADVANCING TO PLOT]
    
    INPUTs:
        'feature_path' - path to directory containing feature data files
        'msd_path' - path to directory containing msd files
        'json_path' - path to json file

    OUTPUTs:
        'df' - the merge data containing both feature qualities and msd, excluding out X & Y values in feature files.
        'msd_data' - dictonary of the msd data for all videos (input for other functions)
        'data_quality' - dictonary of the feature data for all videos (input for other functions)
    '''
    # Sort the data into categories: high, low, medium
    
    with open(json_path) as json_file:
        json_data = json.load(json_file)
    
    feature_list = [
    'alpha', # Fitted anomalous diffusion alpha exponenet
    'D_fit', # Fitted anomalous diffusion coefficient
    'kurtosis', # Kurtosis of track
    'asymmetry1', # Asymmetry of trajecory (0 for circular symmetric, 1 for linear)
    'asymmetry2', # Ratio of the smaller to larger principal radius of gyration
    'asymmetry3', # An asymmetric feature that accnts for non-cylindrically symmetric pt distributions
    'AR', # Aspect ratio of long and short side of trajectory's minimum bounding rectangle
    'elongation', # Est. of amount of extension of trajectory from centroid
    'boundedness', # How much a particle with Deff is restricted by a circular confinement of radius r
    'fractal_dim', # Measure of how complicated a self similar figure is
    'trappedness', # Probability that a particle with Deff is trapped in a region
    'efficiency', # Ratio of squared net displacement to the sum of squared step lengths
    'straightness', # Ratio of net displacement to the sum of squared step lengths
    'MSD_ratio', # MSD ratio of the track
#     'frames', # Number of frames the track spans
    'Deff1', # Effective diffusion coefficient at 0.33 s
    'Deff2', # Effective diffusion coefficient at 3.3 s
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

    feature_files = [f for f in listdir(feature_path) if isfile(join(feature_path, f)) and '.csv' in f and 'P' in f]

    # Apply put_together:
    quality_data = put_together(json_data,feature_list,feature_path,feature_files)

    # Import msd file:
    msd_files = [f for f in listdir(msd_path) if isfile(join(msd_path, f)) and '.csv' in f and 'P' in f]
    msd_data = read_feature(msd_path, msd_files)
   
    # Extracting VIDEO CODES:
    
    # Create empty var
    vid_codes = []
    # Iterate over each file in feature
    for f1 in os.listdir(feature_path):
        
        # Extract the tail in feature file
        feature_tail = f1.split('_',1)[1].split('.')[0]
        
        # Iterate over each file in msd
        for f2 in os.listdir(msd_path):
            
            # Extract the tail in msd file
            msd_tail = f2.split('_',1)[1].split('.')[0]
    
            # If tails are the same
            if feature_tail == msd_tail:
    
                # Add tail into video_codes list
                vid_codes.append(msd_tail)
    
    # Merge feature quality and msd into 1 table
    # Create an empty dictionary
    df = {}
    for code in vid_codes:
        df[code] = pd.merge(msd_data['msd_' + code], quality_data['features_' + code].drop(columns=['X','Y']), on='Track_ID', how='left')                        
    return df, msd_data, quality_data


def trajectory_plot(merge_df, vid_code, save = None):
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
    low_Y = df[df['Category'] == 'low']
    med_Y = df[df['Category'] == 'medium']
    high_Y = df[df['Category'] == 'high']
    null_Y = df[df['Category'] == None]

    # Color coded the X Y based on quality sort
    # green-high, yellow-medium, red-low, purple-NaN

    # Plot
    plt.figure(figsize = (8,8))
        
    plt.plot(low_Y['X'], low_Y['Y'], color='red', label='Low')
    plt.plot(med_Y['X'], med_Y['Y'], color='yellow', label='Medium')
    plt.plot(high_Y['X'], high_Y['Y'], color='green', label='High')
    plt.plot(null_Y['X'], null_Y['Y'], color='grey', label='Unclassified')
    
    plt.legend()
    plt.title('Trajectories of Particles in Video ' + vid_code)
    plt.show()

    if save != None:
        plt.savefig('trajectories_of_' + vid_code + '.png')



# Zoom into the section of interested

def zoom_trajectory_plot(merge_df, vid_code, x1, x2, y1, y2, save = None):

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
    low_Y = df[df['Category'] == 'low']
    med_Y = df[df['Category'] == 'medium']
    high_Y = df[df['Category'] == 'high']
    null_Y = df[df['Category'] == None]

    # Plot
    plt.figure(figsize = (8,8))
        
    plt.plot(low_Y['X'], low_Y['Y'], color='red', label='Low')
    plt.plot(med_Y['X'], med_Y['Y'], color='yellow', label='Medium')
    plt.plot(high_Y['X'], high_Y['Y'], color='green', label='High')
    plt.plot(null_Y['X'], null_Y['Y'], color='grey', label='Unclassified')
    
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Zoom Trajectories of Particles in Video ' + vid_code)
    
    # Zoom into only an area of interested of the plot
    if x1 < x2 and y1 < y2:
        plt.xlim(x1, x2)
        plt.ylim(y1, y2)
    elif x1 > x2 and y1 < y2:
        plt.xlim(x2, x1)
        plt.ylim(y1, y2)
    elif x1 < x2 and y1 > y2:
        plt.xlim(x1, x2)
        plt.ylim(y2, y1)
    elif x1 > x2 and y1 > y2:
        plt.xlim(x2, x1)
        plt.ylim(y2, y1)
        
    plt.grid(True)
    
    plt.show()

    if save != None:
        plt.savefig('zoom_trajectories_of_' + vid_code + '.png')



def distruibution_by_age(feature_path, msd_path, quality_data, save = None):
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
    for f1 in os.listdir(feature_path):
        
        # Extract the tail in feature file
        feature_tail = f1.split('_',1)[1].split('.')[0]
        
        # Iterate over each file in msd
        for f2 in os.listdir(msd_path):
            
            # Extract the tail in msd file
            msd_tail = f2.split('_',1)[1].split('.')[0]
    
            # If tails are the same
            if feature_tail == msd_tail:
    
                # Add tail into video_codes list
                vid_codes.append(msd_tail)



    # Extract & calculate mean score of each video
    qualities = {'Video': [],
                'Mean Quality Score': [],
                'Quality': [],
                'Age': []}
    for i,code in enumerate(vid_codes):
        quality = quality_data['features_' + code]['Quality'].mean()
        qualities['Mean Quality Score'].append(quality)
        qualities['Video'].append(code)
        qualities['Age'].append(code[:3])
        if quality <= 0.333:
            # (-0.001, 0.333] is low, (0.333, 0.667] is medium, and (0.667, 1.0] is high
            qualities['Quality'].append('low')
        elif quality > 0.667:
            qualities['Quality'].append('high')
        else:
            qualities['Quality'].append('medium')
    
    df_qualities = pd.DataFrame(qualities)

    #-- Swarmplot --
    plt.figure(figsize = [8,5])
    
    # Draw a categorical scatterplot to show each observation
    sns.swarmplot(data=df_qualities,
                  x="Mean Quality Score", y="Quality", hue="Age",
                  order = ['high', 'medium','low'],
                  hue_order = np.sort(df_qualities['Age'].unique()))
    
    plt.title('Mean Quality Score Distribution between Different Ages')
    plt.grid(True)
    plt.show()

    if save != None:
        plt.savefig('Quality_score_distribution_by_age.png')
