import pandas as pd
import numpy as np
import scipy as sp

# pairwise Pearson correlation functions
def corr_rowi_rowj(row_i, row_j):
    """
    Pearson correlation between row_i and row_j

    Args: 
        row_i, row_j : pd.Series
            row of data from dataframe, represented as a pandas series

    Output: 
        corr_ij : float
            Pearson correlation of row_i to row_j
    """
    if row_i.any() == False or row_j.any() == False:
        raise Exception("A row is all zeros and does not work with .corr")
    corr_ij = row_i.corr(row_j)
    return corr_ij
    

def corr_rowi_vs_all(row_i, dataframe):
    """
    Vector of Pearson correlations for each row against row_i

    Args: 
        row_i : pd.Series
            row of data from dataframe, represented as a pandas series
        dataframe : pd.DataFrame
            dataframe containing data of interest
    
    Output:
        corr_to_i : list
            list of Pearson correlation values stored as float values
    """
    corr_to_i = []
    for j, row_j in dataframe.iterrows():
        corr_to_i.append(corr_rowi_rowj(row_i,row_j))
    return corr_to_i
     
def pairwise_correlation(dataframe):
    """
    Pairwise Pearson correlation of all rows, plus conversion back to dataframe.
    If issues arise, might need to transpose dataframe.

    Args: 
        dataframe : pd.DataFrame
            dataframe containing data of interest
    
    Output: 
        corr_df = pd.DataFrame
            pandas dataframe containing all pairwise Pearson correlation values
    """ 
    corr_all = []
    for i, row_i in dataframe.iterrows():
        corr_all.append( corr_rowi_vs_all(row_i, dataframe) )
    corr_df = pd.DataFrame(
        np.array(corr_all), # corr_all needs to convert to Numpy array from list
        index=dataframe.index,
        columns=dataframe.index)
    return corr_df

# Dataframe descriptive statistics functions
f feature_descriptive_statistics(dataframe, features):
    """
    This function pulls the descriptive statistics from given features. Input the features as a list of str.
    Can use "all_features" to run descriptive statistics on all features without needing to make a long list of names.
    Quantiles are disabled automatically. To use, make separate variables for each desired quantile and append.


    Args:
        dataframe : pd.DataFrame
            dataframe containing data of interest
        features : list of str, or str
            list of strings which are the features stored as column names in the data frame.
            can use "all_features" to run all feature columns
    
    Output: 
        feat_descriptive_statistics_df : pd.DataFrame
            Pandas dataframe of the descriptive statistics as columns and features as rows
    """
    feat_descriptive_statistics = []
    if features == "all_features":
        features = dataframe.columns.tolist()
        # need to add method to remove Unnamed:0 and ID
        for feature in features:
            feat_stats = []
            feat_mean = dataframe[feature].mean();feat_stats.append(feat_mean)
            feat_median = dataframe[feature].median();feat_stats.append(feat_median)
            feat_max = dataframe[feature].max();feat_stats.append(feat_max)
            feat_min = dataframe[feature].min();feat_stats.append(feat_min)
            #feat_quantile1, feat_quantile2 = dataframe[feature].quantile([0.25, 0.75])
            #feat_stats.append(feat_quantile1,feat_quantile2)
            feat_var = dataframe[feature].var();feat_stats.append(feat_var)
            feat_std = dataframe[feature].std();feat_stats.append(feat_std)
            feat_descriptive_statistics.append(feat_stats)
    else:
        for feature in features:
            feat_stats = []
            feat_mean = dataframe[feature].mean();feat_stats.append(feat_mean)
            feat_median = dataframe[feature].median();feat_stats.append(feat_median)
            feat_max = dataframe[feature].max();feat_stats.append(feat_max)
            feat_min = dataframe[feature].min();feat_stats.append(feat_min)
            #feat_quantiles = dataframe[feature].quantile([0.25, 0.75])
            #feat_stats.append(feat_quantiles)
            feat_var = dataframe[feature].var();feat_stats.append(feat_var)
            feat_std = dataframe[feature].std();feat_stats.append(feat_std)
            feat_descriptive_statistics.append(feat_stats)
    stat_names = ["mean", "median", "maximum", "minimum",
                  "variance", "standard deviation"] 
    feat_descriptive_statistics_df = pd.DataFrame(
        np.array(feat_descriptive_statistics),
        index=features,
        columns=stat_names)
    return feat_descriptive_statistics_df

def multi_df_feat_descriptive_statistics(dataframes, features):
    """
    This function takes an input dictionary of dataframes and 
    a list of features str to automatically run multiple dataframes through
    the feature descriptive statistics, returning a dictionary with the same keys. 
    For running statistics on all features use "all_features".

    Args:
        dataframes : dict
            dictionary of dataframes containing data of interest
        features : list of str, or str
            list of strings which are the features stored as column names in the data frame.
            can use "all_features" to run all feature columns

    Output: 
        dfs_descriptive_statistics : dict
            dictionary of dataframes containing descriptive statistics of specified features
            utilizes the same keys as the input dataframe dictionary
    """
    dfs_descriptive_statistics = {}
    for key in dataframes:
        dfs_descriptive_statistics[key] = feature_descriptive_statistics(dataframes[key],features)
    return dfs_descriptive_statistics

# Feature Outliers function
def feature_outliers(dataframe, features, outlier_method):
    """
    Rapid calculation the outliers of specified feature data within a dataframe.
    Has the options of STD multiplier and IQR for selecting an outlier selection parameter.

    Args:
        dataframe : pd.DataFrame
            dataframe containing data of interest
        features : list of str, or str
            list of strings which are the features stored as column names in the data frame.
            Can use "all_features" string to run all features.
        outlier_method : str
            either "STD multiplier" or "IQR" to specify method of determining outlier cutoff.
            "STD multiplier" will prompt user to enter a float value to use as a multiplier
            of the standard deviation.

    Output:
        feature_outliers_dict : dict
            dictionary containing lists of found outliers above and below selected cutoff for
            specified features
    """
    if features == "all_features":
        features = dataframe.columns.tolist()
        if outlier_method == "STD multiplier":
            n_by_std = float(input("Enter the multiplier you want to use:"))
            feature_outliers_dict = {}
            for feature in features:
                feat_mean = dataframe[feature].mean()
                feat_std = dataframe[feature].std()
                outliers_above = [row_i[feature] for index, row_i in dataframe.iterrows() if row_i[feature] >= feat_mean+(n_by_std*feat_std)]
                outliers_below = [row_i[feature] for index, row_i in dataframe.iterrows() if row_i[feature] <= feat_mean-(n_by_std*feat_std)]
                feature_outliers_dict[feature+" outliers above"] = outliers_above
                feature_outliers_dict[feature+" outliers below"] = outliers_below
    
        elif outlier_method == "IQR":
            feature_outliers_dict = {}
            for feature in features:
                feat_iqr = sp.stats.iqr(dataframe[feature])
                feat_median = dataframe[feature].median()
                outliers_above = [row_i[feature] for index, row_i in dataframe.iterrows() if row_i[feature] >= feat_median+(1.5*feat_iqr)]
                outliers_below = [row_i[feature] for index, row_i in dataframe.iterrows() if row_i[feature] <= feat_median-(1.5*feat_iqr)]
                feature_outliers_dict[feature+" outliers above"] = outliers_above
                feature_outliers_dict[feature+" outliers below"] = outliers_below
    
    else:
        if outlier_method == "STD multiplier":
            n_by_std = float(input("Enter the multiplier you want to use:"))
            feature_outliers_dict = {}
            for feature in features:
                feat_mean = dataframe[feature].mean()
                feat_std = dataframe[feature].std()
                outliers_above = [row_i[feature] for index, row_i in dataframe.iterrows() if row_i[feature] >= feat_mean+(n_by_std*feat_std)]
                outliers_below = [row_i[feature] for index, row_i in dataframe.iterrows() if row_i[feature] <= feat_mean-(n_by_std*feat_std)]
                feature_outliers_dict[feature+" outliers above"] = outliers_above
                feature_outliers_dict[feature+" outliers below"] = outliers_below
    
        elif outlier_method == "IQR":
            feature_outliers_dict = {}
            for feature in features:
                feat_iqr = sp.stats.iqr(dataframe[feature])
                feat_median = dataframe[feature].median()
                outliers_above = [row_i[feature] for index, row_i in dataframe.iterrows() if row_i[feature] >= feat_median+(1.5*feat_iqr)]
                outliers_below = [row_i[feature] for index, row_i in dataframe.iterrows() if row_i[feature] <= feat_median-(1.5*feat_iqr)]
                feature_outliers_dict[feature+" outliers above"] = outliers_above
                feature_outliers_dict[feature+" outliers below"] = outliers_below
    return feature_outliers_dict

# clustering function(s)
def feature_clustering(dataframe, features):
    """
    Simple clustering method to provide a tool in determining whether
    certain features have high contribution to data quality.

    To be implemented in V2. Planning to use scipy k means, or 
    sci-kit learn NearestNeighbors or DBSCAN
    """