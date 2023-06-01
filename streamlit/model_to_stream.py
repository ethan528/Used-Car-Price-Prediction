import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import math
pd.set_option("display.max_columns", None)
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix,r2_score,mean_absolute_error,mean_squared_error
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
import xgboost
import joblib

df = pd.read_csv('./usedcar_total_0608.csv')

X = df[['use','nation','car_brand','car_model','mileage','year','car_type','fuel','trans','loss','flood','usage','change','insurance']] 
Y = df[['depreciation']]

encoded_X = pd.get_dummies(data = X, columns = ['nation','car_brand','car_model','car_type','fuel','trans','loss','flood','usage','insurance'])

s_scale = StandardScaler()

s_scale.fit(encoded_X)
scaled_X= s_scale.transform(encoded_X)

X_train, X_test, y_train, y_test = train_test_split(scaled_X,Y, random_state = 5, test_size = 0.25)

xgb_reg = xgboost.XGBRegressor(learning_rate = 0.5,
                               n_estimators = 200)

xgb_reg.fit(X_train, np.ravel(y_train))

# 모델명 변경해주기

xgb_reg_predict = xgb_reg.predict(X_test)

joblib.dump(xgb_reg, 'xgb_reg_0608.pkl')