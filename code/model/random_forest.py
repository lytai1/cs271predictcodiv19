import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import plot_roc_curve, roc_auc_score, roc_curve
from matplotlib import pyplot as plt
import seaborn as sns


df = pd.read_csv('../../processed_data/ZZ_final_processed_data_no_nan.csv')
print(df)

features = list(df.drop(['outbreak','daily cases mean','daily cases max'], axis = 1).columns[1:])
labels = ['outbreak', 'non-outbreak']
data = df[df.drop(['outbreak','daily cases mean','daily cases max'], axis = 1).columns[1:]].values.tolist()
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

# Add labels to graph
plt.xlabel('Feature Importance Score by Random Forest')
plt.ylabel('Features')
plt.legend()
plt.show()

# Predict probabilities for the test data.
probs = clf.predict_proba(data)
# Keep Probabilities of the positive class only.
probs = probs[:, 1]
# Compute the AUC Score.
auc = roc_auc_score(target, probs)
print('AUC: %.2f' % auc)

# fpr, tpr, thresholds = roc_curve(y_test, probs)
plot_roc_curve(clf, data, target)
plt.show()