# -*- coding: utf-8 -*-
"""Customer Churn Prediction Using Random Forest.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/100Uqxig8g4PDu0eUc8PY_wSgtfu6er-M
"""



"""# Project Title :
# **Telco Customer Chrun Prediction**

# Problem Statment:

Create a predictive model to forecast customer churn for a telecom company using customer data. The goal is to accurately identify customers at risk of leaving, so the company can focus its retention strategies on those who need it most, while avoiding wasted efforts on customers who are unlikely to churn.
"""

# URL for dataset : https://drive.google.com/file/d/1dht-fUhzmbrwNE0xpjVRfOzHiFTnRUIy/view?usp=drive_link

"""# Load Dataset"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

from google.colab import drive
drive.mount('/content/drive/')

train_data = pd.read_csv(r"/content/drive/MyDrive/csv_files/ML PR CLF/Telco-Customer-Churn.csv")
train_data.head()

"""# Data Overview"""

train_data.shape

train_data.size

train_data.info()

# here in dataset "TotalCharges" datatype is Wrong
# train_data["TotalCharges"] = train_data["TotalCharges"].astype("float") when there are empty value in so conversion not happen.
# error = ValueError: could not convert string to float: ' '
# so do this step during handling null value

train_data.describe()

"""Observation:
The 25th, 50th, and 75th percentiles for "SeniorCitizen" are all 0, showing that at least 75% of the values are 0. This confirms that "SeniorCitizen" is a binary categorical variable, with most entries being 0 ("not a senior citizen").
"""

train_data["SeniorCitizen"].plot(kind="hist")

"""result: This histogram, along with the descriptive statistics, will confirm that "SeniorCitizen" is a categorical variable."""

# Check for missing value
train_data.isnull().sum()

train_data[train_data["TotalCharges"]==' ']

"""Observation : There '  ' empty value in TotalCharegs.There are less no. of value so remove empty value."""

train_data["TotalCharges"] = train_data["TotalCharges"].replace(" ", np.nan)

train_data["TotalCharges"].isnull().sum()

# drop null value
train_data.dropna(inplace=True)

# recheck
train_data["TotalCharges"].isnull().sum()

# convert Datatype of "TotalCharges"
train_data["TotalCharges"] = train_data["TotalCharges"].astype("float64")

# Drop the 'customerID' column as it is not useful for prediction
train_data.drop("customerID", axis=1, inplace=True)

# Check and print the number of duplicate rows in the datase
print(f"Number of duplicate rows in train_data: {train_data.duplicated().sum()}")
print("Removing duplicate rows...")
train_data.drop_duplicates(inplace=True,keep = "first")
print(f"Number of duplicate rows after removal:{train_data.duplicated().sum()} ")

# Numeric value EDA

numeric_column = [col for col in train_data.columns if train_data[col].dtype != "O"]
numeric_column

numeric_col = ['tenure', 'MonthlyCharges','TotalCharges']

# Check the distribution of numeric_col
plt.figure(figsize=(15, 10))

for i, col in enumerate(numeric_col):
    # Histogram
    plt.subplot(len(numeric_col), 2, 2*i+1)
    sns.histplot(train_data[col], kde=True)
    plt.xlabel(col)
    plt.ylabel(f"Skewness {train_data[col].skew():.4f}")
    plt.title(f"Distribution of {col}")

    # Box plot
    plt.subplot(len(numeric_col), 2, 2*i+2)
    sns.boxplot(x=train_data[col])
    plt.xlabel(col)
    plt.title(f"Box plot of {col}")

plt.tight_layout()

"""Observation:
Here’s how you can combine the statements for each column:

**Tenure**:
- The distribution is right-skewed, indicating that a majority of customers have been with the company for a shorter duration.
-The box plot shows outliers on the higher end, suggesting that some customers have been with the company for significantly longer periods.

**Monthly Charges**:
- The distribution is relatively normal with a slight left skew.
- The box plot reveals a wider interquartile range, indicating a more varied distribution of monthly charges among customers.

**Total Charges**:
- The distribution is strongly right-skewed, suggesting that a large proportion of customers have lower total charges.
- The box plot shows outliers on the higher end, indicating that a few customers have incurred significantly higher total charges.
"""

# Univarite analysis for numericla columns
numeric_col = ['tenure', 'MonthlyCharges','TotalCharges']

# scatter plot tenure vs MonthlyCharges
plt.figure(figsize=(12,4))
plt.subplot(1,3,1)
sns.scatterplot(data=train_data,
                x="tenure",
                y="MonthlyCharges",
                hue ="Churn")
plt.title("tenure vs MonthlyCharges")

plt.subplot(1,3,2)
sns.scatterplot(data=train_data,
                x="tenure",
                y="TotalCharges",
                hue ="Churn")
plt.title("tenure vs TotalCharges")

plt.subplot(1,3,3)
sns.scatterplot(data=train_data,
                x="MonthlyCharges",
                y="TotalCharges",
                hue ="Churn")
plt.title("MonthlyCharges vs TotalCharges")
plt.tight_layout()

"""Observation:

**Tenure vs. Monthly Charges:**

- There isn’t a clear straight-line relationship between tenure and monthly charges.
- Customers who leave (churn) tend to have shorter tenures and higher monthly charges.


**Tenure vs. Total Charges:**

- There is a clear upward trend: the longer a customer stays, the higher their total charges.
- Churn is more common among customers with lower total charges.


**Monthly Charges vs. Total Charges:**

- There is a strong upward trend: higher monthly charges lead to higher total charges.
- Customers who churn are more often those with lower monthly and total charges.
"""

sns.heatmap(train_data[['tenure', 'MonthlyCharges', 'TotalCharges']].corr(),annot= True)

corr_matrics = train_data[['tenure', 'MonthlyCharges', 'TotalCharges']].corr()
print(corr_matrics)

"""Observation:

TotalCharges and MonthlyCharges have a strong positive correlation of 0.83, indicating that customers with higher monthly charges tend to have higher total charges.
"""

# univariate Analysis of Categorical variable

Categorical_col = [col for col in train_data.columns if train_data[col].dtype == 'O']
Categorical_col

categorical_features = [
    'gender', 'Partner', 'Dependents', 'PhoneService',
    'MultipleLines', 'InternetService', 'OnlineSecurity',
    'OnlineBackup', 'DeviceProtection', 'TechSupport',
    'StreamingTV', 'StreamingMovies', 'Contract',
    'PaperlessBilling', 'PaymentMethod'
]

# Distribution of categorical columns
plt.figure(figsize=(15, 20))

for i, feature in enumerate(categorical_features):
    plt.subplot(5, 3, i+1)
    sns.countplot(x=feature, data=train_data)
    plt.title(f'Count Plot for {feature}')
    plt.xticks(rotation=20)
    plt.tight_layout()

categorical_features = [
    'gender', 'Partner', 'Dependents', 'PhoneService',
    'MultipleLines', 'InternetService', 'OnlineSecurity',
    'OnlineBackup', 'DeviceProtection', 'TechSupport',
    'StreamingTV', 'StreamingMovies', 'Contract',
    'PaperlessBilling', 'PaymentMethod'
]
plt.figure(figsize=(15, 20))

for i, feature in enumerate(categorical_features, 1):
    plt.subplot(5, 3, i)

    crosstab = pd.crosstab(train_data[feature], train_data['Churn'])

    crosstab.plot(kind='bar', stacked=True, ax=plt.gca())  # Use `plt.gca()` to get the current subplot
    plt.title(f'Stacked Bar Plot for {feature}')
    plt.xlabel(feature)
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()

"""## Check whether a dataset is Balanced or Imbalanced ?"""

# final in Eda let's check there in data is Imbalance or not in Target Variable -->> "Chrun"
print(train_data["Churn"].value_counts())

labels = train_data["Churn"].value_counts().index
values = train_data["Churn"].value_counts().values

plt.figure(figsize=(8, 8))
plt.pie(values, labels=labels, autopct='%1.2f%%', startangle=90,
        wedgeprops={'edgecolor': 'black', 'linewidth': 1})

plt.title('Distribution of Churn Status', fontsize=16)
plt.show()

"""Observation:

The pie chart and the value counts clearly indicate that the dataset is imbalanced. The majority of instances belong to the "No" class (73.51%), while only 26.49% belong to the "Yes" class. This imbalance can potentially affect the model's performance, as it may be biased towards the majority class.
"""

train_data.info()

# Checking for Unique Values and Potential Nulls in Categorical Features
categorical_features = [
    'gender', 'Partner', 'Dependents', 'PhoneService',
    'MultipleLines', 'InternetService', 'OnlineSecurity',
    'OnlineBackup', 'DeviceProtection', 'TechSupport',
    'StreamingTV', 'StreamingMovies', 'Contract',
    'PaperlessBilling', 'PaymentMethod'
]

for faeture in categorical_features:
  print(f"{faeture} : {train_data[faeture].unique()}")

train_data.shape

"""# Model Preprocessing steps"""

x =  train_data.drop("Churn",axis =1)
y = train_data["Churn"]

columns_to_scale = ['MonthlyCharges', 'TotalCharges', 'tenure']

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
x[columns_to_scale] = scaler.fit_transform(x[columns_to_scale])

# encode the target varibale
y = y.map({"No":0,"Yes":1})
y.head()

# encode categorical feature
categorical_features = [
    'gender', 'Partner', 'Dependents', 'PhoneService',
    'MultipleLines', 'InternetService', 'OnlineSecurity',
    'OnlineBackup', 'DeviceProtection', 'TechSupport',
    'StreamingTV', 'StreamingMovies', 'Contract',
    'PaperlessBilling', 'PaymentMethod'
]

from sklearn.preprocessing import OneHotEncoder
OHE = OneHotEncoder(sparse = False,drop = 'first')
ohe_x = OHE.fit_transform(x[categorical_features])  # numpy array
ohe_x_df = pd.DataFrame(ohe_x,columns = OHE.get_feature_names_out()) # convert to dataframe # columns get by using ohe.get_feature_names_out() method
ohe_x_df.head()

x = x.drop(categorical_features,axis=1)
x.head()

# lets's concatenate the "x" and "ohe_x_df"
X = pd.concat([x,ohe_x_df],axis=1)
X.head()

X.isnull().sum()

print(x.shape)
print(ohe_x_df.shape)

print(x.index)
print(ohe_x_df.index)

# reset the index of "x" dataframe
x.reset_index(drop=True, inplace=True)
print(x.index)

"""null value issue solve let's concatenate and Recheck"""

X = pd.concat([x,ohe_x_df],axis=1)
X.head()

# recheck if there wasnull value
X.isnull().sum()

""" Issue solve"""



"""# train and test split"""

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

x_train.shape

y_train.shape

"""## Handling Imbalanced Dataset Using SMOTE

**Need :**

Balancing the target class is crucial because the dataset is imbalanced, with 73.51% of instances in the "No" class and only 26.49% in the "Yes" class. This imbalance can lead to a model that is biased towards predicting the majority class, potentially reducing its effectiveness in accurately identifying at-risk customers.
"""

from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state = 42)
x_train_res , y_train_res = smote.fit_resample(x_train,y_train)

x_train_res.shape

y_train_res.shape

# Import necessary libraries
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix , roc_curve, auc

classification_models = {
    "Logistic Regression": LogisticRegression(),
    "K-Nearest Neighbors": KNeighborsClassifier(),
    "Support Vector Machine": SVC(probability=True),
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(),
    "Gradient Boosting": GradientBoostingClassifier(),
    "XGBoost": XGBClassifier(),
    "AdaBoost": AdaBoostClassifier()
}

for model_name, model in classification_models.items():
  model = model
  model.fit(x_train_res,y_train_res)
  y_pred = model.predict(x_test)

  print(f"{model_name}")
  print(f"Accuracy Score :{accuracy_score(y_test,y_pred)}")
  print(f"classification_report :\n {classification_report(y_test,y_pred)}")
  print(f"confusion matrix : \n {confusion_matrix(y_test,y_pred)}")
  print("*"*60)

"""**Obseravtion :**
- Random Forest is the best model for predicting customer churn because it has the highest accuracy at 0.79, outperforming all other models.

- It also provides a good balance between precision (0.53) and recall (0.62), effectively identifying churners while avoiding too many false positives.
- Additionally, its consistent performance is reflected in a solid F1-score of 0.57 for churners, making it a reliable choice overall.
"""

# roc auc curve
rf = RandomForestClassifier()
rf.fit(x_train_res,y_train_res)

y_pred = rf.predict(x_test)
y_prob = rf.predict_proba(x_test)[:,1]

fpr, tpr, _ = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, color='red', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC)')
plt.legend(loc='lower right')
plt.show()

"""Observation:
The Random Forest model achieves a robust ROC AUC score of 0.83, indicating strong performance in distinguishing between churners and non-churners.
"""

from sklearn.model_selection import GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['auto', 'sqrt', 'log2']
}

grid_search = GridSearchCV(
    estimator = rf,
    param_grid = param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    verbose=2)

grid_search.fit(x_train_res,y_train_res)

best_params =  grid_search.best_params_
best_model  =  grid_search.best_estimator_

print(f"Best Parameters: {best_params}")
print(f"Best Model: {best_model}")

y_pred = best_model.predict(x_test)
print(f"Best Model Accuracy: {accuracy_score(y_test, y_pred)}")

from sklearn.model_selection import cross_val_score
cv_score = cross_val_score(best_model,x_train_res,y_train_res,cv=5)
print(f"Cross Validation Score : {cv_score}")
print(f"Mean Cross Validation Score : {cv_score.mean()}")

from sklearn.feature_selection import RFE
rfe = RFE(best_model,n_features_to_select=25)
rfe.fit(x_train_res,y_train_res)

selected_features = x_train_res.columns[rfe.support_]
print(f"Selected Features : {selected_features}")

x_train_selected = x_train_res[selected_features]
x_test_selected = x_test[selected_features]


best_model.fit(x_train_selected, y_train_res)


y_pred = best_model.predict(x_test_selected)

print(f"Accuracy Score: {accuracy_score(y_test, y_pred)}")
print(f"Classification Report:\n{classification_report(y_test, y_pred)}")
print(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")

cv_scores = cross_val_score(best_model, x_train_selected, y_train_res, cv=5)
print(f"Cross-Validation Scores: {cv_scores}")
print(f"Mean Cross-Validation Score: {cv_scores.mean()}")

"""Obseravtion:

With 25 features, the Random Forest model achieved an accuracy score of 0.79, demonstrating strong overall performance. The precision for identifying churners is 0.54, while recall is 0.62, indicating the model effectively balances identifying churners and minimizing false positives. The mean cross-validation score of 0.85 reflects robust and consistent performance across different data splits. Overall, the model's solid accuracy and stability with 25 features make it a reliable tool for predicting customer churn and optimizing retention strategies.

"""

from joblib import dump, load

# Save the best model
dump(best_model, 'best_model.joblib')

