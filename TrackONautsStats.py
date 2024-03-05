import pandas as pd
import numpy as np
import scipy as sc
import sklearn as skl

# Pairwise Pearson Correlation functions
def corr_rowi_rowj(row_i, row_j):
    """Pearson correlation between row_i and row_j"""
    if row_i.any() == False or row_j.any() == False:
        raise Exception("A row is zeros and does not work with .corr")
    corr_ij = row_i.corr(row_j)
    return corr_ij
    

def corr_rowi_vs_all(row_i, dataframe):
    """Vector of Pearson correlations for each row against row_i"""
    corr_to_i = []
    for j, row_j in dataframe.iterrows():
        corr_to_i.append(corr_rowi_rowj(row_i,row_j))
    return corr_to_i
     
def pairwise_correlation(dataframe):
    """Pairwise Pearson correlation of all rows, plus conversion back to dataframe""" 
    corr_all = []
    for i, row_i in dataframe.iterrows():
        corr_all.append( corr_rowi_vs_all(row_i, dataframe) )
    corr_df = pd.DataFrame(
        np.array(corr_all), # corr_all needs to convert to Numpy array from list
        index=dataframe.index,
        columns=dataframe.index)
    return corr_df

def feature_descriptive_statistics(dataframe, features):
    """
    This function pulls the descriptive statistics from given features. Input the features as a string(s).
    Can use "all_features" to run descriptive statistics on all features without needing to make a long list of names.
    Quantiles are disabled automatically. To use, make separate variables for each desired quantile and append.
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
This function takes an input dictionary of dataframes and a list of features to automatically 
run multiple dataframes through the feature descriptive statistics, returning a dictionary with the same keys. 
For running statistics on all features use "all_features".
"""
    dfs_descriptive_statistics = {}
    for key in dataframes:
        dfs_descriptive_statistics[key] = feature_descriptive_statistics(dataframes[key],features)
    return dfs_descriptive_statistics

def feature_outliers(dataframe, features, n_by_std):

    feature_outliers_dict = {}
    for feature in features:
        feat_mean = dataframe[feature].mean()
        feat_std = dataframe[feature].std()
        outliers_above = [row_i[feature] for index, row_i in dummyFeatures_df1.iterrows() if row_i[feature] >= feat_mean+(n_by_std*feat_std)]
        outliers_below = [row_i[feature] for index, row_i in dummyFeatures_df1.iterrows() if row_i[feature] <= feat_mean-(n_by_std*feat_std)]
        feature_outliers_dict[feature+" outliers above"] = outliers_above
        feature_outliers_dict[feature+" outliers below"] = outliers_below
    return feature_outliers_dict