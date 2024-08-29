# ML-ClassificationCustomer-Churn-Prediction


# Problem Statement
- Developed a predictive model to forecast customer churn for a telecom company using customer data. The objective was to accurately identify customers at risk of leaving, enabling the company to concentrate its retention strategies on high-risk customers and avoid wasting efforts on those less likely to churn.

# Dataset
- Source: Telco Customer Churn Dataset
- Details: Contains information on customer demographics, account information, and usage patterns.

# Data Preprocessing
- Handling Missing Values: Replaced empty values in TotalCharges with NaN, then dropped rows with missing values.
- Data Type Conversion: Converted TotalCharges to float after cleaning.
- Duplicate Removal: Identified and removed duplicate rows.
- Feature Engineering: Dropped non-predictive columns (e.g., customerID), and encoded categorical features using one-hot encoding.
# Exploratory Data Analysis (EDA)
- Numeric Features: Analyzed the distribution and outliers for tenure, MonthlyCharges, and TotalCharges.
- Categorical Features: Examined the distribution and relationships of categorical variables with churn status.
- Imbalance Detection: Identified class imbalance with 73.51% non-churn and 26.49% churn, impacting model performance.
# Model Building
- Models Evaluated: Logistic Regression, K-Nearest Neighbors, Support Vector Machine, Decision Tree, Random Forest, Gradient Boosting, AdaBoost, and XGBoost.
- Best Model: Random Forest Classifier achieved the highest accuracy (0.79) and a strong ROC AUC score of 0.83. It demonstrated effective performance in distinguishing between churners and non-churners.
# Model Tuning
- Hyperparameter Optimization: Conducted grid search for hyperparameter tuning, resulting in an optimized Random Forest model.
- Feature Selection: Utilized Recursive Feature Elimination (RFE) to select the most relevant features, leading to enhanced model performance with 25 features.
- Performance Metrics
    - Accuracy: 0.79
    - Precision for Churners: 0.54
    - Recall for Churners: 0.62
    - Mean Cross-Validation Score: 0.85
# Conclusion
-The Random Forest model, after tuning and feature selection, provided a robust solution for predicting customer churn, offering a good balance between precision and recall. This model supports targeted retention strategies by identifying at-risk customers effectively.

# Model Deployment
- Saved Model: The final model was saved using joblib for future use.
