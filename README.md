# Life Expectancy Analysis Dashboard

An end-to-end data analytics project exploring the socio-economic and health factors influencing life expectancy across countries and over time.

The project combines data cleaning, exploratory data analysis, statistical analysis, and interactive dashboarding using Streamlit.

## Problem Statement

Life expectancy is one of the most important indicators of population health and overall development.
Understanding the factors that influence life expectancy can help policymakers and organizations improve overall population health and development.
This project analyzes global life expectancy trends and identifies the socio-economic and health-related factors most strongly associated with it.

## Objectives

- Explore relationships between socio-economic variables.
- Analyze the relationship between life expectancy and socio-economic, health, and nutrition-related factors.
- Identify key drivers of life expectancy.
- Analyze global life expectancy trends over time.
- Compare life expectancy across regions and countries.
- Build an interactive Streamlit dashboard for data exploration.

## Tools & Technologies

- Python
- Pandas
- TheFuzz 
- Scikit-learn
- Plotly
- Streamlit

## Data Cleaning & Preprocessing

The dataset required extensive preprocessing due to missing values, inconsistent formatting, and the absence of regional classification data.

Several preprocessing and data quality improvement steps were performed to prepare the dataset for analysis:

- Fixed inconsistencies in string columns and standardized categorical values.
  
- Handled missing values using multiple approaches:
  - Country-level mean/median imputation for country-specific patterns.
  - KNN Imputer for correlated socio-economic and health-related features.
  - A custom user-defined function to impute missing year values based on detected sequential patterns within the data.

- Added a new "Continent" feature using the United Nations M49 Standard Country or Area Codes table:
  - Applied fuzzy matching techniques using the "thefuzz" library to standardize country names across datasets.
  - Merged continent information into the original dataset for regional analysis.

- Identified unrealistic values (e.g., invalid BMI entries) through data validation checks.

- Fixed inconsistent data types to ensure compatibility across analysis and visualization workflows.

## Key Analysis

### 1. Correlation Analysis
Identified income composition of resources, schooling, adult mortality, and thinness as key factors associated with life expectancy.

### 2. Time Series Analysis
Observed a global increase in life expectancy over time, which aligned with increase in schooling and income composition of resources, and decrease in thinness and adult mortality.

### 3. Regional Analysis
Europe showed the highest average life expectancy, while Africa had the lowest, highlighting major regional disparities.
Japan recorded the highest life expectancy among countries in the dataset, supported by a consistent increase in schooling, income composition of resources, GDP, and healthcare expenditure, along with lower adult mortality rates.

## Key Insights

- Income composition of resources emerged as a primary driver of life expectancy.
- Higher levels of schooling and more effective resource allocation were strongly associated with better population outcomes.
- Schooling and income composition of resources showed a strong positive relationship, suggesting that improvements in education and resource distribution may reinforce one another.
- Significant regional inequalities in life expectancy persist across countries and are strongly associated with disparities in schooling and income composition of resources.

## Live Dashboard

The interactive Streamlit dashboard can be accessed here:
https://life-expectancy-data-analysis-duy94ctrtj2sfyzyxxkawb.streamlit.app/

## Future Improvements

- Integrate country-level map visualizations.
- Include additional healthcare and economic features.
- Add predictive machine learning models.

## Author

Mostafa El-Deeb  
Data Analyst | Pharmacist | Healthcare Background
