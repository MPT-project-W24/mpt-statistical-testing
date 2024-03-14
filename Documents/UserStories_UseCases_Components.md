# User stories, Use Cases, and Component Specification

### User stories
* Nels is a graduate student at the University of Washington who uses multiple particle tracking (MPT) to study the changes in particle diffusion in the extracellular space of brain tissue in neurodegenerative diseases. He wants to identify if there are any sources of error in his MPT data and which ones need to be reanalyzed or reprocessed in an efficient manner. He needs the data to be separated by estimated quality and assess trends and differences through visual and statistical methods, and he desires for the software to be interactive as a web app and use machine learning to flag poor quality data in the future. He is highly technically skilled with code.
* Dr. Nance is the PI of Nels's lab. She wants to be able to assist her mentees in assessing problems in their MPT data quickly. She needs to be able to run the data quickly and have a comprehendable readout that allows her to assist her mentees. She is experienced with code, but not at the same level as Nels. 
* Phil is another graduate student in the Nance Lab. He also runs MPT experiments, more on the wet side, and would like an easy way to know whether there is error in his data. He wants quality and statistical assessments similar to Nels, but in an digestable readout. He understands some simple coding, but is not as technical as Nels.
* Mies is a collaborator of the Nance Lab. They don't run MPT tests, but instead collaborate to make molecules for tracking and therapeutic applications. They want to understand what the errors might be coming from, so their lab can design better molecules. They want the data presented visually well. They are not as technically skilled with code.


### Use cases
* Separate data by estimated quality.
* Assess the statistically significant differences between the data subsets.
* Assess statistically significance within the features of MPT data subssets. 
* Find trends and differences between the data subsets through visualizations.
* Run the analysis with minimal code input by users; future use in a web app.
* Provide easily digestable readouts for users.


### Component specification 
data_separation.py
* read_feature
	* Function that reads all the feature data in the provided data path and put them into a dictionary as values, rename the .csv files and put the names to a dictionary as keys
	* Inputs
		feature_data_path: paths to where the user store the data
		feature_files: the .csv files in the data path
	* Outputs: a dictionary contains the name of each .csv file as keys and the feature data in each .csv file as values
	Connections: output given to other functions
	Side effects: none
filter_feature
Function that filter the feature data by selected feature list
Inputs
feature_data_path: paths to where the user store the data
feature_files: the .csv files in the data path
feature_list: a list contains the features we used
Outputs: a dictionary contains the name of each .csv file as keys and the filtered feature data as values
Connections: output given to other functions
Side effects: none
remove_nans_feature
Function that remove the nans in filtered feature data 
Inputs
feature_data_path: paths to where the user store the data
feature_files: the .csv files in the data path
feature_list: a list contains the features we used
Outputs: a dictionary contains the name of each .csv file as keys and the organized feature data as values
Connections: output given to other functions
Side effects: none
read_json
Function that read the quality data in the order of feature data
Inputs
feature_data_path: paths to where the user store the data
feature_files: the .csv files in the data path
feature_list: a list contains the features we used
json_data: file contains the quality data
Outputs: a dictionary contains the name as keys and the lists contained quality data as values
Connections: output given to other functions
Side effects: none
put_together
Function separate the quality data into different category, combines the organized feature data with the quality data by adding two columns named Quality and Category
Inputs
feature_data_path: paths to where the user store the data
feature_files: the .csv files in the data path
feature_list: a list contains the features we used
json_data: file contains the quality data
Outputs: a dictionary contains the name as keys and the quality data with quality and category as values
Connections: This component can separate the MPT data based on quality. Output given to other functions
Side effects: none
TrackONautsVis.py
position_plot
Function that plots scatter of particle position and color code based on quality
Inputs:
data: quality-sorted dataframe of the video of interest
x: x-axis of plot; takes in "X" column from dataframe
y: y-axis of plot; takes in "Y" column from dataframe
x_bounds: boundary of x-axis; takes two numbers (int or float) in a list; if not specified, default is autoscale
y_bounds: boundary of y-axis; takes two numbers (int or float) in a list; if not specified, default is autoscale
Outputs: scatter plot of particle position color coded based on quality
Connections: this component will read in the feature data in the form of a dataframe
Side effects: none
pairwise_plot
Function that plots all pairwise plots between each column in dataframe
Inputs: 
Data: quality-sorted dataframe of the video of interest
Outputs: scatter plots of all pairwise plots between each column, # of total plots = (# of columns minus 1)^2
Connections: this component will read in the feature data in the form of a dataframe
Side effects: none
pair_plot
Function to plot scatter plot of two specified features and corresponding distribution
Inputs:
data: quality-sorted dataframe of the video of interest
feature1: x-axis of plot; takes in a feature column from dataframe
feature2: y-axis of plot; takes in another feature column from dataframe
Outputs: scatter plot of two specified features and their corresponding distribution color coded based on quality
Connections: this component will read in the feature data in the form of a dataframe
Side effects: none
violin_plot
Function to plot violin plot of specified feature and grouped by quality
Inputs:
data: quality-sorted dataframe of the video of interest
feature: feature of interest
Outputs: violin plot of specified feature grouped by feature quality
Connections: this component will read in the feature data in the form of a dataframe
Side effects: none

video_quality_map.py
merge_data:
Function to extract quality information from Data Quality Analyzer (data_separation.py), and merge into the corresponding msd data.
Inputs:
feature_path: path to features_*.csv files
msd_path: path to msd_*.csv files
Json_path: path to json file
Outputs:
merge_df: a dictionary with keys indicating video codes; for each video code, there is a combined table of msd and feature dataset with the assigned quality for each particle trajectory.
msd_data: a dictionary of all msd data imported here, can be called if needed.
quality_data: a dictionary of all the quality data as in put_together.
Connections:
import package from data_separation
merge_df: needed for trajectory_plot & zoom_trajectory_plot
quality_data: need for distribution_by_age
Side effects: None
trajectory_plot:
Function to plot all trajectories of all particles in one video
Inputs:
merge_df: output from merge_df - a dictionary with keys indicating video codes; for each video code, there is a combined table of msd and feature dataset with the assigned quality for each particle trajectory.
vid_code: code name of the video of interest (example: “P14_40nm_s1_v3”).
save: option to save the plot to current directory; = None (by default)
Output: a plot of all trajectories of all particles of the video of interest
Connections: using merge_df from merge_data
Side effects: None
zoom_trajectory_plot:
A zoom-in function of the plot in trajectory_plot.
Inputs:
merge_df: output from merge_df - a dictionary with keys indicating video codes; for each video code, there is a combined table of msd and feature dataset with the assigned quality for each particle trajectory.
vid_code: code name of the video of interest (example: “P14_40nm_s1_v3”).
x1, x2, y1, y2: x and y bounds of the area of interest on the plot
save: option to save the plot to current directory; = None (by default)
Output: a plot with a closer look into an area of interest.
Connections: using merge_df from merge_data
Side effects: None
distribution_by_age: 
A function that takes information across all of the videos, sorted by age, and a mean quality score for each video was calculated; it generates a swarmplot among videos of different age groups.
Inputs:
feature_path: path to features_*.csv files
msd_path: path to msd_*.csv files
quality_data: a dictionary of all the quality data from merge_data
save: option to save the plot to current directory; = None (by default)
Output: A swarmplot of video quality among different age groups.
Connections: using quality_data from merge_data
Side effects: None

TrackONautsStats.py
corr_rowi_rowj
Pearson correlation between row_i and row_j
Inputs:
row_i, row_j : pd.Series
row of data from dataframe, represented as a pandas series
Outputs:
corr_ij : float
Pearson correlation of row_i to row_j
Connections: receives input data from corr_rowi_vs_all, gives output data to corr_rowi_vs_all
Side effects: ValueError if one of the rows is all zeros
corr_rowi_vs_all
Vector of Pearson correlations for each row against row_i
Inputs:
row_i : pd.Series
row of data from dataframe, represented as a pandas series
dataframe : pd.DataFrame
dataframe containing data of interest
Outputs:
corr_to_i : list
list of Pearson correlation values stored as float values
Connections: receives data from corr_rowi_rowj, receives input data from pairwise_correlation, gives output data to pairwise_correlation
Side effects: see corr_rowi_rowj
pairwise_correlation
Pairwise Pearson correlation of all rows, plus conversion back to dataframe. If issues arise, might need to transpose dataframe.
Inputs:
dataframe : pd.DataFrame
dataframe containing data of interest
Outputs:
corr_df = pd.DataFrame
pandas dataframe containing all pairwise Pearson correlation values
Connections: Can input numerical only dataframes, gives input data to corr_rowi_vs_all, receives data from corr_rowi_vs_all
Side effects: see corr_rowi_rowj
feature_descriptive_statistics	
This function pulls the descriptive statistics from given features. Input the features as a list of str. Can use "all_features" to run descriptive statistics on all features without needing to make a long list of names. Quantiles are disabled automatically. To use, make separate variables for each desired quantile and append.
Inputs:
dataframe : pd.DataFrame
Dataframe containing data of interest
features : list of str, or str
list of strings which are the features stored as column names in the data frame. Can use "all_features" to run all feature columns
Outputs:
feat_descriptive_statistics_df : pd.DataFrame
Pandas dataframe of the descriptive statistics as columns and features as rows
Connections: Can receive numerical only dataframes, output data given to multi_df_feat_descriptive_statistics, can receive inputs from multi_df_feat_descriptive_statistics
Side effects: none
multi_df_feat_descriptive_statistics
This function takes an input dictionary of dataframes and a list of features str to automatically run multiple dataframes through the feature descriptive statistics, returning a dictionary with the same keys. For running statistics on all features use "all_features".
Inputs:
dataframes : dict
dictionary of dataframes containing data of interest
features : list of str, or str
list of strings which are the features stored as column names in the data frame. Can use "all_features" to run all feature columns
Outputs:
dfs_descriptive_statistics : dict
dictionary of dataframes containing descriptive statistics of specified features. Utilizes the same keys as the input dataframe dictionary
Connections: Can receive numerical only dataframes, output data received from feature_descriptive_statistics, gives inputs to feature_descriptive_statistics
Side effects: none
feature_outliers
Rapid calculation of outliers of specified feature data within a dataframe. Has the options of STD multiplier and IQR for selecting an outlier selection parameter.
Inputs:
dataframe : pd.DataFrame
dataframe containing data of interest
features : list of str, or str
list of strings which are the features stored as column names in the data frame. Can use the "all_features" string to run all features.
outlier_method : str
either "STD multiplier" or "IQR" to specify method of determining outlier cutoff. "STD multiplier" will prompt user to enter a float value to use as a multiplier of the standard deviation.
Outputs:
feature_outliers_dict : dict
dictionary containing lists of found outliers above and below selected cutoff for specified features
Connections: Can receive numerical only dataframes
Side effects: none


