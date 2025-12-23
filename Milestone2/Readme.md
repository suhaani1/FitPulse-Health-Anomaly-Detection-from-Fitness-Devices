
#  FitPulse Health Anomaly Detection from Fitness Devices

##  Milestone 2: Feature Extraction and Modeling



##  Objective of Milestone 2

The objective of **Milestone 2** is to derive meaningful insights from preprocessed fitness data by extracting time-series features, modeling temporal trends, and identifying behavioral patterns.
This milestone establishes the analytical foundation required for **anomaly detection** in subsequent milestones.



##  Dataset Description

The dataset used in this milestone is the **cleaned and merged fitness dataset** generated in **Milestone 1**.

### Data Attributes:

* **participant_id** – Unique user identifier
* **timestamp** – Time index (normalized and cleaned)
* **resting_heart_rate** – Heart rate values
* **daily_steps** – Physical activity measure
* **hours_sleep** – Sleep duration

 Data is aligned to a consistent time frequency and free from missing or invalid values.


##  Steps Performed

### 1️ Feature Extraction (TSFresh)

* Converted time-series data into long format
* Automatically extracted statistical and frequency-based features using **TSFresh**
* Applied imputation to handle missing feature values
* Generated a high-dimensional feature matrix for each participant

**Extracted feature examples:**

* Mean, standard deviation, variance
* Skewness, kurtosis
* Energy and entropy measures
* Fourier and autocorrelation features



### 2️ Trend Modeling (Facebook Prophet)

* Modeled temporal trends for:

  * Resting Heart Rate
  * Daily Steps
  * Sleep Duration
* Captured:

  * Seasonal patterns
  * Long-term trends
* Forecasted future values
* Visualized results with **confidence intervals**
* Computed deviations to highlight unusual behavior patterns



### 3️ Behavioral Pattern Clustering

* Standardized extracted features
* Applied unsupervised learning techniques:

  * **KMeans** – to identify dominant behavioral groups
  * **DBSCAN** – to detect outliers and atypical behavior
* Reduced dimensionality using **PCA**
* Visualized clusters in 2D space

 Clusters help distinguish **normal vs. atypical user behavior**.



##  Tools and Libraries Used

* **Python**
* **Streamlit** – Interactive dashboard
* **Pandas & NumPy** – Data manipulation
* **TSFresh** – Time-series feature extraction
* **Facebook Prophet** – Trend and seasonality modeling
* **Scikit-learn** – Clustering & PCA
* **Matplotlib** – Visualization
  



##  Key Observations

* Clear **daily and weekly seasonality** observed in steps and heart rate
* Sleep duration shows comparatively stable trends
* Clustering reveals distinct behavioral patterns among participants
* DBSCAN successfully isolates outlier behaviors
* Feature extraction enables effective dimensionality reduction and grouping









