import numpy
import pandas
import datetime
import platform
from sklearn import linear_model
import sklearn.metrics as sm
from sklearn.ensemble import AdaBoostRegressor
import os
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor

def LinearBoot(dataTrain,dataTest,TestCol,outputpath):
    modelName = 'LinearRegression'
    s = datetime.datetime.now()

    X_train = dataTrain.drop('Rain', axis=1)
    y_train = dataTrain['Rain']  # .loc[dataTrain['Rain'] >= 0, 'Rain']

    X_test = dataTest.drop('Rain', axis=1)
    y_test = dataTest['Rain']  # .loc[dataTest['Rain'] >= 0, 'Rain']

    X_train_Nodate = X_train[TestCol]
    X_test_Nodeate = X_test[TestCol]


    # Create the linear regressor model
    linear_regressor = AdaBoostRegressor(linear_model.LinearRegression(n_jobs=-1),n_estimators=300)

    # Train the model using the training sets
    linear_regressor.fit(X_train_Nodate, y_train)

    # Predict the output
    y_pred = linear_regressor.predict(X_test_Nodeate)

    # Measure performance
    print("Linear Regressor performance:")
    MAE = round(sm.mean_absolute_error(y_test, y_pred), 2)
    MSE = round(sm.mean_squared_error(y_test, y_pred), 2)
    MedienAE = round(sm.median_absolute_error(y_test, y_pred), 2)
    R2score = round(sm.r2_score(y_test, y_pred), 2)

    print("Mean absolute error =", MAE)
    print("Mean squared error =", MSE)
    print("Median absolute error =", MedienAE)
    print("Explained variance score =", round(sm.explained_variance_score(y_test, y_pred), 2))
    print("R2 score =", R2score)

    y_pred = numpy.round(y_pred,1)
    X_test.loc[:,'Predict_Rain'] = pandas.Series(y_pred, index=X_test.index)

    outFile = pandas.DataFrame(X_test[['Date','Lat','Long','Predict_Rain']])

    #print(dataTrain.loc[dataTrain['Rain'] >0, 'Rain'])
    outFile.to_csv(outputpath+'Result_predict_{0}.csv'.format(modelName),index=False)
    text = open(outputpath+'Result_{0}.txt'.format(modelName),mode='a')
    text.write("Mean absolute error ={0}\n".format(MAE))
    text.write("Mean squared error ={0}\n".format(MSE))
    text.write("Median absolute error ={0}\n".format(MedienAE))
    text.write("R2 score ={0}\n".format(R2score))
    e = datetime.datetime.now()
    text.write("Total Time:{0}\n".format(e-s))
    text.close()

def Linear(dataTrain,dataTest,TestCol,outputpath):
    modelName = 'LinearRegression'
    s = datetime.datetime.now()

    X_train = dataTrain.drop('Rain', axis=1)
    y_train = dataTrain['Rain']  # .loc[dataTrain['Rain'] >= 0, 'Rain']

    X_test = dataTest.drop('Rain', axis=1)
    y_test = dataTest['Rain']  # .loc[dataTest['Rain'] >= 0, 'Rain']

    X_train_Nodate = X_train[TestCol]
    X_test_Nodeate = X_test[TestCol]


    # Create the linear regressor model
    linear_regressor = linear_model.LinearRegression(n_jobs=-1)

    # Train the model using the training sets
    linear_regressor.fit(X_train_Nodate, y_train)

    # Predict the output
    y_pred = linear_regressor.predict(X_test_Nodeate)

    # Measure performance
    print("Linear Regressor performance:")
    MAE = round(sm.mean_absolute_error(y_test, y_pred), 2)
    MSE = round(sm.mean_squared_error(y_test, y_pred), 2)
    MedienAE = round(sm.median_absolute_error(y_test, y_pred), 2)
    R2score = round(sm.r2_score(y_test, y_pred), 2)

    print("Mean absolute error =", MAE)
    print("Mean squared error =", MSE)
    print("Median absolute error =", MedienAE)
    print("Explained variance score =", round(sm.explained_variance_score(y_test, y_pred), 2))
    print("R2 score =", R2score)

    y_pred = numpy.round(y_pred,1)
    X_test.loc[:,'Predict_Rain'] = pandas.Series(y_pred, index=X_test.index)

    outFile = pandas.DataFrame(X_test[['Date','Lat','Long','Predict_Rain']])

    #print(dataTrain.loc[dataTrain['Rain'] >0, 'Rain'])
    outFile.to_csv(outputpath+'Result_predict_{0}.csv'.format(modelName),index=False)
    text = open(outputpath+'Result_{0}.txt'.format(modelName),mode='a')
    text.write("Mean absolute error ={0}\n".format(MAE))
    text.write("Mean squared error ={0}\n".format(MSE))
    text.write("Median absolute error ={0}\n".format(MedienAE))
    text.write("R2 score ={0}\n".format(R2score))
    e = datetime.datetime.now()
    text.write("Total Time:{0}\n".format(e-s))
    text.close()

def Bayesian(dataTrain,dataTest,TestCol,outputpath):
    modelName = 'RandomForestRegress'
    s = datetime.datetime.now()

    X_train = dataTrain.drop('Rain', axis=1)
    y_train = dataTrain['Rain']  # .loc[dataTrain['Rain'] >= 0, 'Rain']

    X_test = dataTest.drop('Rain', axis=1)
    y_test = dataTest['Rain']  # .loc[dataTest['Rain'] >= 0, 'Rain']

    X_train_Nodate = X_train[TestCol]
    X_test_Nodeate = X_test[TestCol]

    model = AdaBoostRegressor(linear_model.BayesianRidge(),n_estimators=300)
    model.fit(X_train_Nodate, y_train)
    y_predict = model.predict(X_test_Nodeate)

    print("Baysian performance:")
    MAE = round(sm.mean_absolute_error(y_test, y_predict), 2)
    MSE = round(sm.mean_squared_error(y_test, y_predict), 2)
    MedienAE = round(sm.median_absolute_error(y_test, y_predict), 2)
    R2score = round(sm.r2_score(y_test, y_predict), 2)
    print("Mean absolute error =", MAE)
    print("Mean squared error =", MSE)
    print("Median absolute error =", MedienAE)
    print("Explained variance score =", round(sm.explained_variance_score(y_test, y_predict), 2))
    print("R2 score =", R2score)

    y_pred = numpy.round(y_predict, 1)
    X_test.loc[:, 'Predict_Rain'] = pandas.Series(y_pred, index=X_test.index)

    outFile = pandas.DataFrame(X_test[['Date', 'Lat', 'Long', 'Predict_Rain']])
    # print(outFile)
    # print(dataTrain.loc[dataTrain['Rain'] > 0, 'Rain'])
    outFile.to_csv(outputpath+'Result_predict_{0}.csv'.format(modelName), index=False)
    text = open(outputpath+'Result_{0}.txt'.format(modelName), mode='a')
    text.write("Mean absolute error ={0}\n".format(MAE))
    text.write("Mean squared error ={0}\n".format(MSE))
    text.write("Median absolute error ={0}\n".format(MedienAE))
    text.write("R2 score ={0}\n".format(R2score))
    e = datetime.datetime.now()
    text.write("Total Time:{0}".format(e - s))
    text.close()

def NN(dataTrain,dataTest,TestCol,outputpath):
    modelName = 'NeuronNetwork'
    s = datetime.datetime.now()

    X_train = dataTrain.drop('Rain', axis=1)
    y_train = dataTrain['Rain']  # .loc[dataTrain['Rain'] >= 0, 'Rain']

    X_test = dataTest.drop('Rain', axis=1)
    y_test = dataTest['Rain']  # .loc[dataTest['Rain'] >= 0, 'Rain']

    X_train_Nodate = X_train[TestCol]
    X_test_Nodeate = X_test[TestCol]

    NN = MLPRegressor(hidden_layer_sizes=10,activation='logistic',solver='adam')
    NN.fit(X_train_Nodate, y_train)
    y_predict = NN.predict(X_test_Nodeate)
    MAE = round(sm.mean_absolute_error(y_test, y_predict), 2)
    MSE = round(sm.mean_squared_error(y_test, y_predict), 2)
    MedienAE = round(sm.median_absolute_error(y_test, y_predict), 2)
    R2score = round(sm.r2_score(y_test, y_predict), 2)
    # print("pre:",y_pred.shape,"true:",y_test.shape)
    # score = linear_regressor.score(y_pred.reshape(1,),y_test.reshape(1,))
    print("Mean absolute error =", MAE)
    print("Mean squared error =", MSE)
    print("Median absolute error =", MedienAE)
    print("Explained variance score =", round(sm.explained_variance_score(y_test, y_predict), 2))
    print("R2 score =", R2score)
    # print("Accuracy:",accuracy_score(y_test,y_pred))
    y_pred = numpy.round(y_predict, 1)
    # data_frame = pd.DataFrame(y_pred)
    # data_frame['Rain_Predict'] = pd.Series(y_pred, index=data_frame.index)
    # result = pd.Series(y_pred, index=X_test.index)
    X_test.loc[:, 'Predict_Rain'] = pandas.Series(y_pred, index=X_test.index)

    outFile = pandas.DataFrame(X_test[['Date', 'Lat', 'Long', 'Predict_Rain']])
    # print(outFile)
    print(dataTrain.loc[dataTrain['Rain'] > 0, 'Rain'])
    outFile.to_csv(outputpath+'Result_predict_{0}.csv'.format(modelName), index=False)
    text = open(outputpath+'Result_{0}.txt'.format(modelName), mode='a')
    text.write("Mean absolute error ={0}\n".format(MAE))
    text.write("Mean squared error ={0}\n".format(MSE))
    text.write("Median absolute error ={0}\n".format(MedienAE))
    text.write("R2 score ={0}\n".format(R2score))
    e = datetime.datetime.now()
    text.write("Total Time:{0}".format(e - s))
    text.close()


def KNN(dataTrain,dataTest,TestCol,outputpath):
    s = datetime.datetime.now()
    modelName = 'KNN'
    X_train = dataTrain.drop('Rain', axis=1)
    y_train = dataTrain['Rain']#.loc[dataTrain['Rain'] >= 0, 'Rain']

    X_test = dataTest.drop('Rain', axis=1)
    y_test = dataTest['Rain']#.loc[dataTest['Rain'] >= 0, 'Rain']

    X_train_Nodate = X_train[TestCol]
    X_test_Nodeate = X_test[TestCol]

    KNN = KNeighborsRegressor(n_neighbors=8, weights='distance', algorithm='auto', n_jobs=-1)
    KNN.fit(X_train_Nodate, y_train)
    y_predict = KNN.predict(X_test_Nodeate)
    MAE = round(sm.mean_absolute_error(y_test, y_predict), 2)
    MSE = round(sm.mean_squared_error(y_test, y_predict), 2)
    MedienAE = round(sm.median_absolute_error(y_test, y_predict), 2)
    R2score = round(sm.r2_score(y_test, y_predict), 2)
    # print("pre:",y_pred.shape,"true:",y_test.shape)
    # score = linear_regressor.score(y_pred.reshape(1,),y_test.reshape(1,))
    print("Mean absolute error =", MAE)
    print("Mean squared error =", MSE)
    print("Median absolute error =", MedienAE)
    print("Explained variance score =", round(sm.explained_variance_score(y_test, y_predict), 2))
    print("R2 score =", R2score)
    # print("Accuracy:",accuracy_score(y_test,y_pred))
    y_pred = numpy.round(y_predict, 1)
    # data_frame = pd.DataFrame(y_pred)
    # data_frame['Rain_Predict'] = pd.Series(y_pred, index=data_frame.index)
    # result = pd.Series(y_pred, index=X_test.index)
    X_test.loc[:, 'Predict_Rain'] = pandas.Series(y_pred, index=X_test.index)

    outFile = pandas.DataFrame(X_test[['Date', 'Lat', 'Long', 'Predict_Rain']])
    # print(outFile)
    #print(dataTrain.loc[dataTrain['Rain'] > 0, 'Rain'])
    outFile.to_csv(outputpath+'Result_predict_{0}.csv'.format(modelName), index=False)
    text = open(outputpath+'Result_{0}.txt'.format(modelName), mode='a')
    text.write("Mean absolute error ={0}\n".format(MAE))
    text.write("Mean squared error ={0}\n".format(MSE))
    text.write("Median absolute error ={0}\n".format(MedienAE))
    text.write("R2 score ={0}\n".format(R2score))
    e = datetime.datetime.now()
    text.write("Total Time:{0}".format(e - s))
    text.close()

def start():
    
    path = input("Address of file:")
    File = [f for f in os.listdir(path) if f.endswith('.csv')]
    for i,f in enumerate(File):
        print(i,f)
    selectTrain = int(input("Select file Train:"))
    pathTrain = path+File[selectTrain]

    selectTest = int(input("Select file Test:"))
    pathTest = path+File[selectTest]
    #outputpath = '/home/team7/hackathon/output/'#input("path of output:")
    # pathTrain = '/home/team7/hackathon/Prepreocess_Train.csv'
    # pathTest = '/home/team7/hackathon/Clean_Prepreocess_Test.csv'
    # outputpath = '/home/team7/hackathon/'
    outputpath = './'
    SelectColumn =['Date','Lat', 'Long', 'avg_IR8', 'max_IR8', 'min_IR8',
             'avg_IR13', 'max_IR13','min_IR13',
             'avg_IR15', 'max_IR15', 'min_IR15',
             'diff_avg_IR8-13','diff_avg_IR8-15','diff_avg_IR13-15',
             'diff_max_IR8-13', 'diff_max_IR8-15', 'diff_max_IR13-15',
             'diff_min_IR8-13', 'diff_min_IR8-15', 'diff_min_IR13-15','Rain']

    #['Date', 'Lat', 'Long', 'avg_IR8', 'avg_IR13', 'avg_IR15', 'Rain']
    #TestCol = ['Lat', 'Long', 'avg_IR8', 'avg_IR13', 'avg_IR15']

    TestCol =['Lat', 'Long', 'avg_IR8', 'max_IR8', 'min_IR8',
             'avg_IR13', 'max_IR13','min_IR13',
             'avg_IR15', 'max_IR15', 'min_IR15',
             'diff_avg_IR8-13','diff_avg_IR8-15','diff_avg_IR13-15',
             'diff_max_IR8-13', 'diff_max_IR8-15', 'diff_max_IR13-15',
             'diff_min_IR8-13', 'diff_min_IR8-15', 'diff_min_IR13-15']

    # Load the data from the input file
    dataTrain = pandas.read_csv(pathTrain, usecols=SelectColumn)
    dataTest = pandas.read_csv(pathTest, usecols=SelectColumn)


    Linear(dataTrain, dataTest, TestCol,outputpath)
    Bayesian(dataTrain, dataTest,TestCol,outputpath)
    NN(dataTrain, dataTest, TestCol, outputpath)
    LinearBoot(dataTrain, dataTest, TestCol, outputpath)
    # KNN(dataTrain,dataTest,TestCol,outputpath)
    # RF(dataTrain,dataTest,TestCol,outputpath)
    # SVM(dataTrain,dataTest,TestCol,outputpath)

if __name__ == '__main__':
    start()