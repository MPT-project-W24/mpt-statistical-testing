# Track_o_Nauts
Hello! Welcome to our software engineering project Track-o-Nauts. Within this repository we have created software for visualization and statisical testing to improve multiple particle tracking data quality and experimental design.

### Dependencies
The Track-o-Nauts Python Packages run in Python environments, and require Pandas, Numpy, SciPy, Seaborn, and Matplotlib. These packages were developed using up-to-date versions of Python=3.11, Pandas, Numpy=1.23.3, SciPy, Seaborn, and Matplotlib as of March 13, 2024.

### Packages
* data_separation.py - contains functions to separate MTP data based on quality value and catagory. Functions include reading MPT feature and quality data, organizing MPT feature data and combining quality values with MPT feature data. 
* video_quality_map.py - contains a function to merge the quality data with the msd data; using the output of that, there are plot functions that plot trajectory map of all particles in one chosen video and its zoom version into an area of interest, including color codes based on the quality of each particle; and a function that plot the distribution of quality among different age groups and videos.
* TrackONautsVis.py file - contains functions to plot features of the video of interest. Functions include particle position plot, pairwise plot for all features, pairwise plot for two specified features, and violin plot of a specified feature distribution.
* TrackONautsStats.py - contains functions to rapidly run statistical methods on dataframes. V1.0 contains Pearson pairwise correlation, descriptive statistics, and outlier identification

### How to use
Functions from the .py files can be imported and utilized in Jupyter notebooks and Python scripts. Example use cases are available in the 'Notebooks' directory.
