import netCDF4
import pandas
import os
import numpy
import platform
import pp
import sys
import datetime

def ReadFile(date,df,pathIR8,pathIR13,pathIR15,outputpath):

    a = df[df['Date'] == date]

    IR13 = netCDF4.Dataset(pathIR13, 'r')

    IR15 = netCDF4.Dataset(pathIR15, 'r')

    IR8 = netCDF4.Dataset(pathIR8, 'r')


    LatCenter = a['Lat']
    LongCenter = a['Long']

    lat = numpy.asarray(IR13.variables['latitude'])
    long = numpy.asarray(IR13.variables['longitude'])


    tbb13 = numpy.asarray(IR13.variables['tbb13'])
    tbb15 = numpy.asarray(IR15.variables['tbb15'])
    tbb8 = numpy.asarray(IR8.variables['tbb08'])

    IR13.close()
    IR15.close()
    IR8.close()

    DistanceX = 0.02


    writeTofile=[]
    for i in a.index:

        temp8 = pandas.DataFrame(tbb8, columns=long, index=lat)
        temp13 = pandas.DataFrame(tbb13, columns=long, index=lat)
        temp15 = pandas.DataFrame(tbb15, columns=long, index=lat)
        #print(temp8)
        temp8=temp8[temp8.index>=LatCenter[i]-DistanceX]
        temp8=temp8[temp8.index<=LatCenter[i]+DistanceX]

        temp13 = temp13[temp13.index >= LatCenter[i] - DistanceX]
        temp13 = temp13[temp13.index <= LatCenter[i] + DistanceX]

        temp15 = temp15[temp15.index >= LatCenter[i] - DistanceX]
        temp15 = temp15[temp15.index <= LatCenter[i] + DistanceX]

        col_8 = [f for f in temp8.columns if f <= LongCenter[i] + DistanceX and f >= LongCenter[i] - DistanceX]
        col_13 = [f for f in temp13.columns if f <= LongCenter[i] + DistanceX and f >= LongCenter[i] - DistanceX]
        col_15 = [f for f in temp15.columns if f <= LongCenter[i] + DistanceX and f >= LongCenter[i] - DistanceX]

        temp8 = temp8[col_8].values.flatten()
        temp13 = temp13[col_13].values.flatten()
        temp15 = temp15[col_15].values.flatten()


        writeTofile.append([date, LatCenter[i], LongCenter[i],
                    numpy.mean(temp8),numpy.max(temp8),numpy.min(temp8),
                    numpy.mean(temp13),numpy.max(temp13),numpy.min(temp13),
                    numpy.mean(temp15),numpy.max(temp15),numpy.min(temp15),
                    abs(numpy.mean(temp8)-numpy.mean(temp13)),abs(numpy.mean(temp8)-numpy.mean(temp15)),abs(numpy.mean(temp13)-numpy.mean(temp15)),
                    abs(numpy.max(temp8)-numpy.max(temp13)),abs(numpy.max(temp8)-numpy.max(temp15)),abs(numpy.max(temp13)-numpy.max(temp15)),
                    abs(numpy.min(temp8)-numpy.min(temp13)), abs(numpy.min(temp8) - numpy.min(temp15)),abs(numpy.min(temp13) - numpy.min(temp15)),
                    a['Rain'][i]])

    f = pandas.DataFrame(writeTofile,
                    columns=['Date', 'Lat', 'Long', 'avg_IR8', 'max_IR8', 'min_IR8',
                             'avg_IR13', 'max_IR13','min_IR13',
                             'avg_IR15', 'max_IR15', 'min_IR15',
                             'diff_avg_IR8-13','diff_avg_IR8-15','diff_avg_IR13-15',
                             'diff_max_IR8-13', 'diff_max_IR8-15', 'diff_max_IR13-15',
                             'diff_min_IR8-13', 'diff_min_IR8-15', 'diff_min_IR13-15',
                             'Rain'])

    month = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y%m")
    WriteToCSV(month,f,outputpath)

def WriteToCSV(day,Frame,outputPath):
    filename = 'Prepreocess_Test_{0}.csv'.format(day)
    Frame = Frame[Frame['Rain'] != 'None']
    datatype = {'Date': str, 'Lat': float, 'Long': float,
                'avg_IR8': float, 'max_IR8': float, 'min_IR8': float,
                'avg_IR13': float, 'max_IR13': float, 'min_IR13': float,
                'avg_IR15': float, 'max_IR15': float, 'min_IR15': float,
                'diff_avg_IR8-13': float, 'diff_avg_IR8-15': float, 'diff_avg_IR13-15': float,
                'diff_max_IR8-13': float, 'diff_max_IR8-15': float, 'diff_max_IR13-15': float,
                'diff_min_IR8-13': float, 'diff_min_IR8-15': float, 'diff_min_IR13-15': float,
                'Rain': float}
    Frame.astype(datatype)
    if os.path.isfile(outputPath+filename):
        Frame.to_csv(outputPath+filename, mode='a', index=False, header=False)
    else:
        Frame.to_csv(outputPath+filename, mode='w', index=False)

def checkIR8(Filename,pathIR8):
    day = datetime.datetime.strptime(Filename, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d")
    time = datetime.datetime.strptime(Filename, "%Y-%m-%d %H:%M:%S").strftime("%H%M")

    filename = 'IR08_' + day + '_' + time + '.nc'
    file = [f for f in os.listdir(pathIR8) if f.endswith('.nc') and f == filename]
    path8 = pathIR8 + filename

    i = 10
    if len(file) > 0:
        path8 = pathIR8 + filename
        return path8
    else:
        while i < 60:
            time = time[:2] + str(i)
            filename = 'IR08_' + day + '_' + time + '.nc'
            file = [f for f in os.listdir(pathIR8) if f.endswith('.nc') and f == filename]
            path8 = pathIR8 + filename
            i = i + 10
            # print(path15,'dgsgjkskgjbrkhj')
            if len(file) > 0:
                return path8
                break

def checkIR13(Filename,pathIR13):
    day = datetime.datetime.strptime(Filename, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d")
    time = datetime.datetime.strptime(Filename, "%Y-%m-%d %H:%M:%S").strftime("%H%M")
    filename = 'IR13_' + day + '_' + time + '.nc'
    file = [f for f in os.listdir(pathIR13) if f.endswith('.nc') and f == filename]
    path13 = pathIR13 + filename

    i = 10
    if len(file) > 0:
        path13 = pathIR13 + filename
        return path13
    else:
        while i < 60:
            time = time[:2] + str(i)
            filename = 'IR13_' + day + '_' + time + '.nc'
            file = [f for f in os.listdir(pathIR13) if f.endswith('.nc') and f == filename]
            path13 = pathIR13 + filename
            i = i + 10
            # print(path15,'dgsgjkskgjbrkhj')
            if len(file) > 0:
                return path13
                break

def checkIR15(Filename,pathIR15):
    day = datetime.datetime.strptime(Filename, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d")
    time = datetime.datetime.strptime(Filename, "%Y-%m-%d %H:%M:%S").strftime("%H%M")
    filename = 'IR15_' + day + '_' + time + '.nc'
    file = [f for f in os.listdir(pathIR15) if f.endswith('.nc') and f == filename]
    path15 = pathIR15 + filename
    i = 10
    if len(file) > 0:
        path15 = pathIR15 + filename
        return path15
    else:
        while i < 60:
            time = time[:2] + str(i)
            filename = 'IR15_' + day + '_' + time + '.nc'
            file = [f for f in os.listdir(pathIR15) if f.endswith('.nc') and f == filename]
            path15 = pathIR15 + filename
            i = i + 10
            # print(path15,'dgsgjkskgjbrkhj')
            if len(file) > 0:
                return path15
                break


def start():

    DateinOutput=datetime.datetime.now().strftime("%Y-%m-%d")
    if platform.system() == 'Windows':
        file = '..\\..\\data\\rain\\5-9_2017.csv'
        pathIR8 = '..\\..\\data\\irdata\\ir08nc\\'
        pathIR13 = '..\\..\\data\\irdata\\ir13nc\\'
        pathIR15 = '..\\..\\data\\irdata\\ir15nc\\'
        outputPath = '..\\..\\output_{0}\\'.format(DateinOutput)

    else:
        file = '/data/rain/8-9_2017.csv'
        pathIR8 = '/data/dl_hackathon_data_2/ir08nc/'
        pathIR13 = '/data/dl_hackathon_data_2/ir13nc/'
        pathIR15 = '/data/dl_hackathon_data_2/ir15nc/'
        outputPath = '/home/team7/hackathon/Test'

    if os.path.isdir(outputPath) == False:
        os.mkdir(outputPath)


    header = ['Date', 'Lat', 'Long', 'Rain']
    df = pandas.read_csv(file, names=header)
    date = pandas.unique(df['Date'])

    #######################################  Parallel  ####################################################
    ppservers = ()


    if len(sys.argv) > 1:
        ncpus = int(sys.argv[1])
        # Creates jobserver with ncpus workers
        job_server = pp.Server(ncpus, ppservers=ppservers)
    else:
        # Creates jobserver with automatically detected number of workers
        job_server = pp.Server(ppservers=ppservers)
    print("Starting pp with", job_server.get_ncpus(), "workers")
    #################################################################################################

    for dt in date:

        IR8_check = checkIR8(dt,pathIR8)
        IR13_check = checkIR13(dt,pathIR13)
        IR15_check = checkIR15(dt,pathIR15)
        if IR15_check != None and IR13_check != None and IR8_check != None:
            print(dt)
            job_server.submit(ReadFile, (dt, df, IR8_check, IR13_check, IR15_check, outputPath,),(WriteToCSV,), ("os", "netCDF4", 'pandas', 'numpy', 'datetime'))


if __name__ == '__main__':
    s = datetime.datetime.now()
    start()
    e = datetime.datetime.now()
    print(e-s)