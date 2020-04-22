import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics
from matplotlib import pyplot as plt


def f_importances(coef, features, top=-1):
    imp = coef
    imp, features = zip(*sorted(zip(imp, features)))
    if top == -1:
        top = len(features)

    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), features[::-1][0:top])
    plt.show()


df = pd.read_csv('../../processed_data/ZZ_final_processed_data_no_nan.csv', index_col=0)
print(df)

# TO_DO: 12 features, put outbreak 2nd column
features = list(df.drop(['outbreak'], axis = 1).columns[1:])             # to fix [2:]
labels = ['outbreak', 'non-outbreak']
data = df[df.drop(['outbreak'], axis = 1).columns[1:]].values.tolist()   # to fix [2:]
target = list(df['outbreak'])
print(len(features), "Features: ", features)
print(len(data), 'Data: ', data)
print(len(target), 'Target: ', target)

X_train, X_test, y_train, y_test = train_test_split(data, target, test_size = 0.8)
clf = svm.SVC(kernel='linear')
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print("Accuracy: ", metrics.accuracy_score(y_test, y_pred))

#f_importances(clf.coef_, features)
f_importances(abs(clf.coef_[0]), features)