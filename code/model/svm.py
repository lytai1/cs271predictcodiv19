import pandas as pd
from sklearn.model_selection import RandomizedSearchCV, cross_val_score, train_test_split
from sklearn import svm
from sklearn import metrics
from matplotlib import pyplot as plt
from sklearn.svm import SVR


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
target = list(df['outbreak'].map({True:1, False:0}))
print(len(features), "Features: ", features)
print(len(data), 'Data: ', data)
print(len(target), 'Target: ', target)

X_train, X_test, y_train, y_test = train_test_split(data, target, test_size = 0.2)

# # use this to find the optimal parameters for SVR
# c = [0.01, 0.1, 1]
# gamma = [0.01, 0.1, 1]
# shrinking = [True, False]
# degree = [3, 4, 5, 6, 7]

# svm_grid = {'C': c, 'gamma' : gamma, 'shrinking' : shrinking, 'degree': degree}

# svm1 = svm.SVC(kernel='linear')
# svm_search = RandomizedSearchCV(svm1, svm_grid, scoring='neg_mean_squared_error', cv=3, return_train_score=True, n_jobs=-1, n_iter=30, verbose=1)
# svm_search.fit(X_train, y_train)

# print(svm_search.best_params_)
# #{'shrinking': False, 'gamma': 0.01, 'degree': 6, 'C': 1}

clf = svm.SVC(kernel='linear', shrinking=False, gamma=0.01, degree=6, C=1)
# clf.fit(X_train, y_train)
# y_pred = clf.predict(X_test)
# print("Accuracy: ", metrics.accuracy_score(y_test, y_pred))

scores = cross_val_score(clf, data, target, cv=5)
print(scores)

#f_importances(clf.coef_, features)
# f_importances(abs(clf.coef_[0]), features)