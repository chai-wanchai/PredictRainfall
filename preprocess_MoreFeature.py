from netCDF4 import Dataset
import pandas as pd
import os
import numpy as np
import platform
from datetime import datetime
def ReadFile(date,IR):
    a = df[df['Date'] == date]
    IR13 = Dataset(pathIR13+'IR13_'+IR, 'r')
    IR15 = Dataset(pathIR15+'IR15_' + IR, 'r')
    IR8= Dataset(pathIR8+'IR08_' + IR, 'r')
    print(date)
    # print(IR13)
    # print(IR15)
    # print(IR8)

    LatCenter = a['Lat']
    LongCenter = a['Long']

    lat = np.asarray(IR13.variables['latitude'])
    long = np.asarray(IR13.variables['longitude'])
    tbb13 = np.asarray(IR13.variables['tbb13'])
    tbb15 = np.asarray(IR15.variables['tbb15'])
    tbb8 = np.asarray(IR8.variables['tbb08'])

    IR13.close()
    IR15.close()
    IR8.close()

    DistanceX = 0.05


    writeTofile=[]
    for i in a.index:

        temp8 = pd.DataFrame(tbb8, columns=long, index=lat)
        temp13 = pd.DataFrame(tbb13, columns=long, index=lat)
        temp15 = pd.DataFrame(tbb15, columns=long, index=lat)
        #print(tbbb)
        #tbb8.index = pd.to_numeric(tbb8.index)
        #print(LatCenter)
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
                    np.mean(temp8),np.max(temp8),np.min(temp8),
                    np.mean(temp13),np.max(temp13),np.min(temp13),
                    np.mean(temp15),np.max(temp15),np.min(temp15),
                    abs(np.mean(temp8)-np.mean(temp13)),abs(np.mean(temp8)-np.mean(temp15)),abs(np.mean(temp13)-np.mean(temp15)),
                    abs(np.max(temp8)-np.max(temp13)),abs(np.max(temp8)-np.max(temp15)),abs(np.max(temp13)-np.max(temp15)),
                    abs(np.min(temp8)-np.min(temp13)), abs(np.min(temp8) - np.min(temp15)),abs(np.min(temp13) - np.min(temp15)),
                    a['Rain'][i]])
    f = pd.DataFrame(writeTofile,
                    columns=['Date', 'Lat', 'Long', 'avg_IR8', 'max_IR8', 'min_IR8',
                             'avg_IR13', 'max_IR13','min_IR13',
                             'avg_IR15', 'max_IR15', 'min_IR15',
                             'diff_avg_IR8-13','diff_avg_IR8-15','diff_avg_IR13-15',
                             'diff_max_IR8-13', 'diff_max_IR8-15', 'diff_max_IR13-15',
                             'diff_min_IR8-13', 'diff_min_IR8-15', 'diff_min_IR13-15',
                             'Rain'])
    day = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d")

    WriteToCSV(month,f)


def ReadMin(Filename):
    day = datetime.strptime(Filename, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d")
    time = datetime.strptime(Filename, "%Y-%m-%d %H:%M:%S").strftime("%H%M")
    t = (int)(time)
    while (t<=(int)(time)+50):
        IRfile = day+'_'+str(t)+'.nc'
        #ReadFile(Filename,IRfile)
        print(IRfile)
        t=t+10


def WriteToCSV(day,Frame):
    if os.path.isfile(outputPath+'Prepreocess_{0}.csv'.format(day)):
        Frame.to_csv(outputPath+'Prepreocess_{0}.csv'.format(day), mode='a', index=False, header=False)
    else:
        Frame.to_csv(outputPath+'Prepreocess_{0}.csv'.format(day), mode='w', index=False)

def checkIR8(Filename):
    file = [f for f in os.listdir(pathIR8) if f.endswith('.nc') and f==Filename]
    if len(file)>0:
        return True
    else:
        return False

def checkIR13(Filename):
    file = [f for f in os.listdir(pathIR13) if f.endswith('.nc') and f==Filename]
    if len(file)>0:
        return True
    else:
        return False

def checkIR15(Filename):
    file = [f for f in os.listdir(pathIR15) if f.endswith('.nc') and f==Filename]
    if len(file)>0:
        return True
    else:
        return False

if __name__ == '__main__':
    file = ''
    pathIR8 = ''
    pathIR13 = ''
    pathIR15 = ''
    outputPath=''
    DateinOutput=datetime.now().strftime("%Y-%m-%d")
    if os.path.isdir('.\\output_{0}\\'.format(DateinOutput)) == False:
        os.mkdir('.\\output_{0}\\'.format(DateinOutput))


    if platform.system()=='Windows':
        file = '.\\data\\rain\\5-9_2017.csv'
        pathIR8 = '.\\data\\irdata\\ir08nc\\'
        pathIR13 = '.\\data\\irdata\\ir13nc\\'
        pathIR15 = '.\\data\\irdata\\ir15nc\\'
        outputPath = '.\\output_{0}\\'.format(DateinOutput)

    else:
        file = '/data/rain/5-9_2017.csv'
        pathIR8 = '/data/irdata/ir08nc/'
        pathIR13 = '/data/irdata/ir13nc/'
        pathIR15 = '/data/irdata/ir15nc/'
        outputPath = './output_{0}/'.format(DateinOutput)

    header = ['Date', 'Lat', 'Long', 'Rain']
    df = pd.read_csv(file, names=header)
    #print(len(pd.unique(df['Date'])))
    #print(df)
    date = pd.unique(df['Date'])
    s = datetime.now()
    for dt in date:
        day = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d")
        time = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").strftime("%H%M")
        month = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").strftime("%Y%m")
        #print(month)
        #print('IR13_'+day+'_'+time+'.nc')
        IR8_check=checkIR8('IR08_'+day+'_'+time+'.nc')
        IR13_check=checkIR13('IR13_' + day + '_' + time + '.nc')
        IR15_check=checkIR15('IR15_' + day + '_' + time + '.nc')

        if IR8_check==True and IR13_check==True and  IR15_check==True:
            IRfile = day+'_'+time+'.nc'
            #print(IRfile)
            ReadFile(dt,IRfile)

    e = datetime.now()
    print(e-s)

