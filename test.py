
# from datetime import datetime
# str1 ='2017-05-01 00:00:00'
# str2 = '5/1/2017  1:00:00 AM'
# str2 = datetime.strptime(str2, "%m/%d/%Y %I:%M:%S %p").strftime("%Y-%m-%d %H:%M:%S")
# print(str2)
# print(datetime.strptime(str2, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d'))
# print(datetime.strptime(str1, '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S'))
#
# a = '20160228'
# date = datetime.strptime(a, '%Y%m%d').strftime('%m%d%Y')
# print(date)
#
# file = open("testfile.txt", "w")
#
# file.write("Hello World")
# file.write("This is ournewtextfile")
# file.write(" and this is anotherline.")
# file.write("Why? Becausewecan.")
#
# file.close()

import pandas as pd
import numpy as np
from numba.parfor import prange
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
df= pd.read_csv('C:\\Users\\chai_\\Google Drive\\1_2560 (1)\\DeepLearning\\output\\PrevTest.csv',dtype={'Date':str,'Lat':float,'Long':float,'IR8':float,'IR13':float,'IR15':float,'Rain':float},
                usecols=['Lat','Long','IR8','IR13','IR15','IR8-IR13','IR8-IR15','IR13-IR15','Rain'])
df = df[['Lat','Long','IR8','IR13','IR15','IR8-IR13','IR8-IR15','IR13-IR15','Rain']]
print(df)
x = df[['Lat','Long','IR8','IR13','IR15','IR8-IR13','IR8-IR15','IR13-IR15']]


y = np.asarray(df['Rain'], dtype="|S6")

# print(x['Lat'].dtype)
# print(x['Long'].dtype)
# print(x['IR13'].dtype)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
model = MLPClassifier(activation='logistic', solver='adam', alpha=1e-5, learning_rate='adaptive',max_iter=10000)
# print(model)
# print('XTest:',X_test)
# print(y_test)

model.fit(X_train,y_train)
y_predict = model.predict(X_test)
accuracy = accuracy_score(y_test, y_predict)
print(accuracy)
