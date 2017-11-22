import netCDF4
import pandas
import os
import numpy
import platform
import pp
import sys
import datetime

def ReadFile(date,IR,df,pathIR8,pathIR13,pathIR15,outputpath):

    a = df[df['Date'] == date]
    IR13 = netCDF4.Dataset(pathIR13+'IR13_'+IR, 'r')
    IR15 = netCDF4.Dataset(pathIR15+'IR15_' + IR, 'r')
    IR8= netCDF4.Dataset(pathIR8+'IR08_' + IR, 'r')

    print(date)
    # print(IR13)
    # print(IR15)
    # print(IR8)

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

    DistanceX = 0.05


    writeTofile=[]
    for i in a.index:

        temp8 = pandas.DataFrame(tbb8, columns=long, index=lat)
        temp13 = pandas.DataFrame(tbb13, columns=long, index=lat)
        temp15 = pandas.DataFrame(tbb15, columns=long, index=lat)

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
    day = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d")
    month = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y%m")
    WriteToCSV(month,f,outputpath)


def ReadMin(Filename):
    day = datetime.datetime.strptime(Filename, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d")
    time = datetime.datetime.strptime(Filename, "%Y-%m-%d %H:%M:%S").strftime("%H%M")
    t = (int)(time)
    while (t<=(int)(time)+50):
        IRfile = day+'_'+str(t)+'.nc'
        #ReadFile(Filename,IRfile)
        print(IRfile)
        t=t+10


def WriteToCSV(day,Frame,outputPath):
    if os.path.isfile(outputPath+'Prepreocess_{0}.csv'.format(day)):
        Frame.to_csv(outputPath+'Prepreocess_{0}.csv'.format(day), mode='a', index=False, header=False)
    else:
        Frame.to_csv(outputPath+'Prepreocess_{0}.csv'.format(day), mode='w', index=False)

def checkIR8(Filename):
    file = [f for f in os.listdir(pathIR8) if f.endswith('.nc') and f==Filename]
    if len(file)>0:
        return True

def checkIR13(Filename):
    file = [f for f in os.listdir(pathIR13) if f.endswith('.nc') and f==Filename]
    if len(file)>0:
        return True

def checkIR15(Filename):
    file = [f for f in os.listdir(pathIR15) if f.endswith('.nc') and f==Filename]
    if len(file)>0:
        return True

if __name__ == '__main__':
    file = ''
    pathIR8 = ''
    pathIR13 = ''
    pathIR15 = ''
    outputPath=''
    DateinOutput=datetime.datetime.now().strftime("%Y-%m-%d")



    if platform.system()=='Windows':
        file = '.\\data\\rain\\5-9_2017.csv'
        pathIR8 = '.\\data\\irdata\\ir08nc\\'
        pathIR13 = '.\\data\\irdata\\ir13nc\\'
        pathIR15 = '.\\data\\irdata\\ir15nc\\'
        outputPath = '.\\output_{0}\\'.format(DateinOutput)
        if os.path.isdir('.\\output_{0}\\'.format(DateinOutput)) == False:
            os.mkdir('.\\output_{0}\\'.format(DateinOutput))
        outputPath = '.\\output_{0}\\'.format(DateinOutput)

    else:
        file = '/data/rain/5-9_2017.csv'
        pathIR8 = '/data/irdata/ir08nc/'
        pathIR13 = '/data/irdata/ir13nc/'
        pathIR15 = '/data/irdata/ir15nc/'
        outputPath = './output_{0}/'.format(DateinOutput)
        if os.path.isdir('/home/team7/Parallel/output_preprocess_{0}/'.format(DateinOutput)) == False:
            os.mkdir('/home/team7/Parallel/output_preprocess_{0}/'.format(DateinOutput))
        outputPath = '/home/team7/Parallel/output_preprocess_{0}/'.format(DateinOutput)

    header = ['Date', 'Lat', 'Long', 'Rain']
    df = pandas.read_csv(file, names=header)
    #print(len(pandas.unique(df['Date'])))
    #print(df)
    date = pandas.unique(df['Date'])
    s = datetime.datetime.now()

    ppservers = ()
    # ppservers = ("10.0.0.1",)

    if len(sys.argv) > 1:
        ncpus = int(sys.argv[1])
        # Creates jobserver with ncpus workers
        job_server = pp.Server(ncpus, ppservers=ppservers)
    else:
        # Creates jobserver with automatically detected number of workers
        job_server = pp.Server(ppservers=ppservers)
    print("Starting pp with", job_server.get_ncpus(), "workers")

    #print(date)
    month=[]
    day=[]
    time=[]
    test=[]
    for dt in date:
        m = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").strftime("%Y%m")
        d = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").strftime("%d")
        t = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").strftime("%H%M")
        # month.append(m)
        # day.append(d)
        # time.append(t)
        # test.append(m+d+'_'+t)
        filename = m+d+'_'+t


        IR8_check = checkIR8('IR08_' + filename+ '.nc')
        IR13_check = checkIR13('IR13_' +filename + '.nc')
        IR15_check = checkIR15('IR15_' + filename+ '.nc')
        IRfile = filename + '.nc'
        #print(IRfile)
        if IR8_check == True and IR13_check == True and IR15_check == True:
            print(dt)
            job_server.submit(ReadFile, (dt,IRfile, df, pathIR8, pathIR13, pathIR15, outputPath,),
                              (WriteToCSV,),("os", "netCDF4", 'pandas', 'numpy', 'datetime'))


    e = datetime.datetime.now()
    print(e-s)

