# Hospital Patient Record Analysis

A Big Data project that ingests, cleans, processes, and analyzes real
New York State hospital inpatient discharge records using **Hadoop HDFS**
for distributed storage and **PySpark** for data processing and analysis.

The project explores patterns in patient demographics, admission types,
hospital distribution, illness severity, mortality risk, length of stay,
and hospital charges.

**Team:** Adhithya Rajesh · Anannya AK · Anuvarnna A · Mayooka K

**Guide:** Ms. Jithika M

---

## Architecture

```text
Raw CSV
(NY SPARCS Hospital Inpatient Discharge, 2010)
                │
                ▼
          HDFS Storage
                │
                ▼
       PySpark Data Cleaning
                │
                ▼
      Cleaned Data in HDFS
                │
                ▼
        PySpark Analysis
                │
                ▼
         Visualization
                │
                ▼
             Report
Tech Stack
Layer	Technology
Distributed Storage	Hadoop HDFS 3.3.6
Data Processing	Apache PySpark 3.5.1
Programming Language	Python
Visualization	Matplotlib
Development Environment	Visual Studio Code
Operating System	Windows
Dataset
Source

New York State Statewide Planning and Research Cooperative System
(SPARCS) — Hospital Inpatient Discharge Data, 2010

The dataset contains real, de-identified hospital inpatient discharge
records from hospitals in New York State.

The dataset was used to demonstrate the application of Big Data
technologies for healthcare data processing and analysis.

Dataset Fields Used

The following 14 fields were selected for the project:

Health Service Area
Hospital County
Facility Name
Age Group
Gender
Race
Length of Stay
Type of Admission
Patient Disposition
CCS Diagnosis Description
APR Severity of Illness Description
APR Risk of Mortality
Total Charges
Total Costs
Project Objectives

The main objectives of this project are:

To understand distributed data storage using Hadoop HDFS.
To process healthcare data using Apache PySpark.
To clean and prepare raw hospital records for analysis.
To perform data aggregation and statistical analysis.
To identify patterns in patient demographics and hospital admissions.
To analyze illness severity and risk of mortality.
To examine hospital length of stay and total charges.
To visualize important findings from the processed dataset.
Project Workflow
1. Data Ingestion

The raw hospital discharge dataset is uploaded to Hadoop HDFS.

Raw CSV → HDFS

The raw dataset is stored at:

/healthcare_project/raw/hospital_discharge_sample.csv

HDFS provides the distributed storage layer for the project.

2. Data Cleaning

The raw dataset is loaded from HDFS using PySpark.

The cleaning process includes:

Selecting the required columns.
Converting Length of Stay into numeric format.
Converting Total Charges into numeric format.
Converting Total Costs into numeric format.
Removing rows with missing required values.
Removing invalid Length of Stay values.
Removing duplicate records.
Saving the cleaned dataset back to HDFS.
Raw Data
    ↓
Column Selection
    ↓
Data Type Conversion
    ↓
Missing Value Removal
    ↓
Invalid Value Removal
    ↓
Duplicate Removal
    ↓
Cleaned Data
3. Data Analysis

The cleaned dataset is processed using PySpark to perform different
aggregations and calculations.

The analysis includes:

Patient distribution by age group.
Patient distribution by gender.
Top 10 hospitals by patient count.
Average length of stay.
Average total charges.
Patient distribution by type of admission.
Patient distribution by risk of mortality.
Patient distribution by severity of illness.
4. Data Visualization

The analysis results are visualized using Matplotlib.

The project includes charts for:

Age Group Distribution
Gender Distribution
Admission Type
Risk of Mortality
Top 10 Hospitals by Patient Count

The generated charts are stored in:

outputs/charts/
Dataset Statistics

The project processed 150,406 hospital records.

Processing Stage	Number of Records
Original Records	150,406
Cleaned Records	147,650
Records Removed	2,756
Final Columns	14

The cleaned dataset contains 147,650 records after applying the
cleaning operations.

The cleaned data is stored in HDFS at:

/healthcare_project/cleaned
Analysis Results
1. Patients by Age Group
Age Group	Patient Count
70 or Older	41,670
50 to 69	38,833
30 to 49	31,318
0 to 17	19,940
18 to 29	15,889

The 70 or Older age group contains the highest number of patient
records in the cleaned dataset.

2. Patients by Gender
Gender	Patient Count
Female	83,021
Male	64,628
Unknown	1

The cleaned dataset contains more female records than male records.

3. Top 10 Hospitals by Patient Count
Hospital	Patient Count
Mount Sinai Hospital	3,349
North Shore University Hospital	3,017
New York Presbyterian Hospital - Columbia Presbyterian Center	2,909
New York Presbyterian Hospital - New York Weill Cornell Center	2,646
Beth Israel Medical Center/Petrie Campus	2,595
Montefiore Medical Center - Henry & Lucy Moses Div	2,591
Strong Memorial Hospital	2,241
Long Island Jewish Medical Center	2,219
New York Methodist Hospital	2,132
Winthrop-University Hospital	2,052
4. Average Length of Stay

The average length of stay calculated from the cleaned dataset is:

5.55 days

5. Average Total Charges

The average total charges calculated from the cleaned dataset are:

$29,965

6. Patients by Type of Admission
Type of Admission	Patient Count
Emergency	93,337
Elective	29,394
Urgent	12,994
Newborn	11,617
Not Available	259
Trauma	49

Emergency is the largest admission category in the cleaned dataset.

7. Patients by Risk of Mortality
Risk of Mortality	Patient Count
Minor	91,447
Moderate	32,015
Major	17,009
Extreme	7,169
Unknown	10
8. Patients by Severity of Illness
Severity of Illness	Patient Count
Moderate	55,210
Minor	52,950
Major	30,462
Extreme	9,018
Unknown	10
Visualizations

The project generates five main visualizations.

Age Group Distribution

Displays the number of patient records across different age groups.

Gender Distribution

Shows the distribution of patient records by gender.

Admission Type

Displays the number of patients across different admission categories.

Risk of Mortality

Shows the distribution of patients across the different APR risk of
mortality categories.

Top 10 Hospitals

Displays the hospitals with the highest number of patient records in the
cleaned dataset.

All visualization files are stored in:

outputs/charts/
Project Structure
healthcare-bigdata-analysis/
│
├── data/
│   └── raw/
│       └── hospital_discharge_sample.csv
│
├── outputs/
│   └── charts/
│       ├── age_group_distribution.py
│       ├── age_group_distribution.png
│       ├── gender_distribution.py
│       ├── gender_distribution.png
│       ├── admission_type.py
│       ├── admission_type.png
│       ├── mortality_risk.py
│       ├── mortality_risk.png
│       ├── top_10_hospitals.py
│       └── top_10_hospitals.png
│
├── report/
│
├── src/
│   ├── data_cleaning.py
│   └── analysis.py
│
├── test_read_hdfs.py
├── test_spark.py
├── requirements.txt
├── README.md
└── venv/
Setup & Reproduction
Prerequisites

The following software is required:

Python
Java
Hadoop 3.3.6
Apache PySpark 3.5.1
Matplotlib
Visual Studio Code
1. Start Hadoop

Start the Hadoop HDFS and YARN services:

start-dfs.cmd
start-yarn.cmd
2. Create HDFS Directory

Create the project directory in HDFS:

hdfs dfs -mkdir -p /healthcare_project/raw
3. Upload the Dataset

Place the dataset inside the project's raw data folder:

data/raw/

Then upload it to HDFS:

hdfs dfs -put data/raw/hospital_discharge_sample.csv /healthcare_project/raw/
4. Install Python Dependencies

Install the required Python packages:

pip install -r requirements.txt
5. Run Data Cleaning

Run the PySpark data cleaning program:

python src/data_cleaning.py

The cleaned data will be stored in:

/healthcare_project/cleaned
6. Run Data Analysis

Run the PySpark analysis program:

python src/analysis.py

The analysis results will be displayed in the terminal.

7. Generate Visualizations

The visualization scripts are located in:

outputs/charts/

Run the required Python scripts to generate the chart images.

HDFS Storage

Hadoop HDFS is used as the distributed storage layer of the project.

Raw Dataset
/healthcare_project/raw/hospital_discharge_sample.csv
Cleaned Dataset
/healthcare_project/cleaned
Key Observations

The analysis of the cleaned dataset produced the following observations:

The 70 or Older age group contains the highest number of patient
records.
Emergency admissions represent the largest admission category.
The dataset contains more female records than male records.
Minor is the most common APR risk of mortality category.
Moderate is the most common APR severity of illness category.
The average length of stay is approximately 5.55 days.
The average total charges are approximately $29,965.
The patient records are distributed across multiple hospitals,
counties, age groups, admission types, and illness categories.
Future Improvements

The project can be extended in several ways:

Scale the project to a multi-node Hadoop cluster.
Add more advanced PySpark analysis.
Include hospital discharge data from additional years.
Perform year-wise trend analysis.
Add more healthcare-related visualizations.
Build an interactive dashboard using Power BI or Streamlit.
Explore machine learning techniques for predicting hospital-related
outcomes.
Conclusion

This project demonstrates a Big Data workflow for processing and analyzing
hospital inpatient discharge records using Hadoop HDFS and
Apache PySpark.

The pipeline successfully performed data ingestion, data cleaning,
large-scale analysis, and visualization.

A total of 150,406 hospital records were processed, resulting in
147,650 cleaned records after applying the data cleaning operations.

The project provides practical experience in distributed storage,
data cleaning, PySpark-based processing, statistical analysis, and
data visualization using a real-world healthcare dataset.

Team

Adhithya Rajesh
Anannya AK
Anuvarnna A
Mayooka K

Project Guide: Ms. Jithika M

Project Status

Completed

The project includes:

Data ingestion into HDFS
Data cleaning using PySpark
Data analysis using PySpark
Data visualization using Matplotlib
Project documentation