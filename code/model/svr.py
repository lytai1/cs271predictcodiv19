from datetime import timedelta
import datetime
import pandas as pd
import numpy as np
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.svm import SVR
from matplotlib import pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error


start = datetime.date(2020,1,22)
end = datetime.date(2020,3,15)
path = "../../raw_data/COVID-19-master/COVID-19-master/csse_covid_19_data/csse_covid_19_daily_reports/"

def pull_data(start, end, path, col):
    day_count = (end - start).days +1
    worldcases = list()

    for single_date in (start + timedelta(n) for n in range(day_count)):
        date = single_date.strftime("%m-%d-%Y")
        filepath = path + date + ".csv"
        df = pd.read_csv(filepath)
        df.fillna(0, inplace=True)
        df = df[col]
        worldcases.append(df.sum())
        
    return np.array([i for i in range(day_count)]).reshape(-1, 1), np.array(worldcases).reshape(-1, 1)

def main():
    date_from, confirm = pull_data(start, end, path, "Confirmed")
    X_train_confirmed, X_test_confirmed, y_train_confirmed, y_test_confirmed = train_test_split(date_from, confirm, test_size=0.07, shuffle=False)

    # # use this to find the optimal parameters for SVR
    # kernel = ['poly', 'sigmoid', 'rbf']
    # c = [0.01, 0.1, 1, 10]
    # gamma = [0.01, 0.1, 1]
    # epsilon = [0.01, 0.1, 1]
    # shrinking = [True, False]
    # # svm_grid = {'C': c, 'gamma' : gamma, 'epsilon': epsilon, 'shrinking' : shrinking}
    # svm_grid = {'kernel': kernel, 'C': c, 'gamma' : gamma, 'epsilon': epsilon, 'shrinking' : shrinking}

    # svm = SVR()
    # # svm = SVR(kernel='rbf')
    # svm_search = RandomizedSearchCV(svm, svm_grid, scoring='neg_mean_squared_error', cv=3, return_train_score=True, n_jobs=-1, n_iter=40, verbose=1)
    # svm_search.fit(X_train_confirmed, y_train_confirmed)

    # print(svm_search.best_params_)
    # #{'shrinking': True, 'kernel': 'poly', 'gamma': 0.01, 'epsilon': 0.01, 'C': 10}
    # #{'shrinking': False, 'gamma': 0.01, 'epsilon': 0.1, 'C': 10} # with rbf

    svm_confirmed = SVR(shrinking=True, kernel='poly', gamma=0.01, epsilon=0.01, C=10)
    # svm_confirmed = SVR(shrinking=False, kernel='rbf', gamma=0.01, epsilon=0.1, C=10)
    svm_confirmed.fit(X_train_confirmed, y_train_confirmed)
    days_in_future = 10
    day_count = (end - start).days +1
    future_forcast = np.array([i for i in range(day_count + days_in_future)]).reshape(-1, 1)
    svm_pred = svm_confirmed.predict(future_forcast)
    print(svm_pred)

    # check against testing data
    svm_test_pred = svm_confirmed.predict(X_test_confirmed)
    plt.plot(y_test_confirmed)
    plt.plot(svm_test_pred)
    plt.legend(['Confirmed Cases', 'SVM predictions'])
    print('MAE:', mean_absolute_error(svm_test_pred, y_test_confirmed))
    print('MSE:',mean_squared_error(svm_test_pred, y_test_confirmed))

    
    actual_date, actual_confirm =  pull_data(start, end + timedelta(days=days_in_future), path, "Confirmed")
    plt.figure(figsize=(20, 12))
    plt.plot(actual_date, actual_confirm)
    plt.plot(future_forcast, svm_pred, linestyle='dashed', color='purple')
    plt.title('Number of Coronavirus Cases Over Time', size=30)
    plt.xlabel('Days Since 1/22/2020', size=30)
    plt.ylabel('Number of Cases', size=30)
    plt.legend(['Confirmed Cases', 'SVM predictions'])
    plt.xticks(size=15)
    plt.yticks(size=15)
    plt.show()

main()