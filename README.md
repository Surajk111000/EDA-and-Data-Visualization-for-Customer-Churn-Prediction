# EDA-and-Data-Visualization-for-Customer-Churn-Prediction
Exploratory Data Analysis (EDA) and Data Visualization for Customer Churn Prediction

In this project, I conducted an Exploratory Data Analysis (EDA) on client and price data using Python and the Pandas library. The primary goal was to gain insights into the dataset and identify patterns that could contribute to customer churn prediction.

Steps and Highlights:

Data Loading and Initial Examination:

Loaded the client data from "client_data.csv" and the price data from "price_data.csv".
Displayed the first 3 rows of each dataset using head() to get a glimpse of the data.
Used info() to analyze the data types and missing values in both datasets.
Employed describe() to generate basic statistics like mean, standard deviation, etc. for numeric columns.
Data Visualization and Insights:

Defined a function plot_stacked_bars() to plot stacked bar charts for visualizing categorical data distribution.
Utilized the function to visualize the distribution of sales channels and contract types.
Created histograms and box plots to visualize and compare various consumption metrics.
Visualized the distribution of forecasted values related to energy consumption and pricing.
Examined margin data using box plots to understand gross and net margins.
Plotted distributions of power capacity (pow_max) and product-related metrics.
Data Transformation and Feature Engineering:

Converted date columns to datetime format for further analysis.
Computed mean values for energy prices over different time periods (yearly, 6 months, 3 months) using the price data.
Combined the computed price features with client data to create a comprehensive analysis dataset.
Calculated correlation coefficients to understand relationships between variables.
Correlation Analysis:

Calculated the correlation matrix of the combined dataset.
Utilized a heatmap to visualize the correlation coefficients and identify potential dependencies.
Data Consolidation and Export:

Merged the cleaned and analyzed data from both datasets into a single dataframe.
Exported the consolidated and enriched dataset as "clean_data_after_eda.csv" for further modeling and analysis.
Outcome:
This EDA process helped uncover patterns, correlations, and potential factors contributing to customer churn. By visualizing and analyzing various features, the project provided valuable insights for building predictive models to identify customers at risk of churning.

Please note that the actual insights and conclusions from the data analysis would depend on the content of the datasets and the specific findings from the EDA process.





