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

* Data Quality Analyzer
	* This software component sorts data based on estimated quality, provides some visual and statistical analysis, and flags poor data that needs revision.
	* Inputs: `.csv` MPT feature data files; `.json` Estimated data quality parameters
	* Outputs: Quality sorted data with color code: Low - red; Medium - yellow; High - green
	* Connections: Feeds quality classification to MPT Feature Data Statistical Analyzer
	* Side Effects: None
* MPT Feature Data Statistical Analyzer
	* This software component provides descriptive statistical analysis on the MPT features data.
	* Input: `.csv` MPT feature data file(s)
	* Outputs: Descriptive statistics (mean, median, etc.)
	* Connections: This component will connect to the Data Quality Analyzer to throw warnings of low quality data (optional for user). It will also pass the descriptive statistics to the MPT Feature Data Inferential Analyzer.
	* Side Effects:None
* MPT Feature Data Inferential Analyzer
	* This software component provides inferential statistical analysis on the MPT features data.
	* Inputs: `.csv` MPT feature data file(s)
	* Outputs: inferential output; p-value; regression value
	* Connections: This component takes descriptive statistics from MPR Feature Data Statistical Analyzer
	* Side Effects: None
* One line Interface
	* This software will run the data analysis in a single line
	* Inputs: `.csv` MPT feature data files; `.json` Estimated data quality parameters; desired statistics
	* Outputs: Statistical results; possible flags of data
	* Connections: This connects to and utilizes each of the analyzers
	* Side Effects: extra analysis not output

