import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, cross_val_score, train_test_split
from sklearn import svm
from sklearn import metrics
from matplotlib import pyplot as plt
from sklearn.svm import SVR
from sklearn.metrics import roc_auc_score, roc_curve
import numpy as np
import seaborn as sns


df = pd.read_csv('../../processed_data/ZZ_final_processed_data_no_nan.csv')
print(df)

# TO_DO: 12 features, put outbreak 2nd column
features = list(df.drop(['outbreak','daily cases mean','daily cases max'], axis = 1).columns[1:])             # to fix [2:]
labels = ['outbreak', 'non-outbreak']
data = df[df.drop(['outbreak','daily cases mean','daily cases max'], axis = 1).columns[1:]].values.tolist()   # to fix [2:]
#target = list(df['outbreak'])
target = list(df['outbreak'].map({True:1, False:0}))
print(len(features), "Features: ", features)
print(len(data), 'Data: ', data)
print(len(target), 'Target: ', target)

X_train, X_test, y_train, y_test = train_test_split(data, target, test_size = 0.2)
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print("Accuracy: ", metrics.accuracy_score(y_test, y_pred))

feature_imp = pd.Series(clf.feature_importances_,index=features).sort_values(ascending=True)
#print(feature_imp)

# Creating a bar plot
sns.barplot(x=feature_imp, y=feature_imp.index)

# Add labels to your graph
plt.xlabel('Feature Importance Score by Random Forest')
plt.ylabel('Features')
plt.legend()
plt.show()
