def video_quality_map(feature_path, msd_path, json_path, vid_code):
    ''' Plot trajectories of particles in 1 video:
    INPUTs:
        'feature_path' - path to directory containing feature data files
        'msd_path' - path to directory containing msd files
        'json_path' - path to json file
        'vid_code' - code name of the video of interest (ex: 'P14_40nm_s1_v3')
    '''
    
    from data_separation import read_feature, filter_feature, remove_nans_feature, put_together    
    from os import listdir, getcwd, chdir
    from os.path import isfile, join
    import json
    import pandas as pd
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
    data_quality = put_together(json_data,feature_list,feature_path,feature_files)
    feature1 = data_quality['features_' + vid_code]

    # Import msd file:
    msd_files = [f for f in listdir(msd_path) if isfile(join(msd_path, f)) and '.csv' in f and 'P' in f]
    msd_data = read_feature(msd_path, msd_files)
    msd1 = msd_data['msd_' + vid_code]

    # Color coded the X Y based on quality sort
    # green-high, yellow-medium, red-low, purple-NaN
    
    # Merge feature quality and msd into 1 table
    feature2 = feature1[['Track_ID','Category']]
    df = pd.merge(msd1, feature2, on='Track_ID', how='left')

    # Separate data based on Category
    low_Y = df[df['Category'] == 'low']
    med_Y = df[df['Category'] == 'medium']
    high_Y = df[df['Category'] == 'high']
    null_Y = df[df['Category'] == None]
    
    # Plot
    import matplotlib.pyplot as plt
    plt.figure(figsize = (10,10))
        
    plt.plot(low_Y['X'], low_Y['Y'], color='red', label='Low')
    plt.plot(med_Y['X'], med_Y['Y'], color='yellow', label='Medium')
    plt.plot(high_Y['X'], high_Y['Y'], color='green', label='High')
    plt.plot(null_Y['X'], null_Y['Y'], color='grey', label='Unclassified')
    
    plt.legend()
    plt.title('Trajectories of Particles in Video ' + vid_code)
    plt.show()
