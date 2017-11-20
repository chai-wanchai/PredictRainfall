from netCDF4 import Dataset
import pandas as pd
import os
import numpy as np

from datetime import datetime
def ReadFile(date,IR):
    a = df[df['Date'] == date]
    IR13 = Dataset('.\\Data\\Band13\\IR13_'+IR, 'r')
    IR15 = Dataset('.\\Data\\Band15\\IR15_' + IR, 'r')
    IR8= Dataset('.\\Data\\Band8\\IR08_' + IR, 'r')
    #print(a)
    print(IR13)
    print(IR15)
    print(IR8)

    LatCenter = a['Lat']
    LongCenter = a['Long']

    lat = np.asarray(IR13.variables['latitude'])
    long = np.asarray(IR13.variables['longitude'])
    tbb13 = np.asarray(IR13.variables['tbb13'])
    tbb15 = np.asarray(IR15.variables['tbb15'])
    tbb8 = np.asarray(IR8.variables['tbb08'])
    tbb13Area = []
    tbb15Area = []
    tbb8Area = []
    DistanceY = 0.05
    DistanceX = 0.05

    ########
    TopCenterLat = []
    TopCenterLong = []
    TopLeftLat = []
    TopLeftLong = []
    TopRightLat = []
    TopRightLong = []
    LeftCenterLat = []
    LeftCenterLong = []
    RightCenterLat = []
    RightCenterLong = []
    BottonLeftLat = []
    BottonLeftLong = []
    BottonRightLat = []
    BottonRightLong = []
    BottonCenterLat = []
    BottonCenterLong = []

    IR13.close()
    IR15.close()
    IR8.close()
    writeTofile = []
    for index in a.index:
        TopCenterLat = [i for i, l in enumerate(lat) if l <= LatCenter[index] + DistanceY and l >= LatCenter[index]]
        TopCenterLong = [i for i, l in enumerate(long) if l <= LongCenter[index] + DistanceY and l >= LongCenter[index]]

        for i in TopCenterLat:
            for j in TopCenterLong:
                tbb13Area.append(tbb13[i][j])
                tbb15Area.append(tbb15[i][j])
                tbb8Area.append(tbb8[i][j])


        TopLeftLat = [i for i, l in enumerate(long) if l <= LatCenter[index] + DistanceY - DistanceX and l >= LatCenter[index]]
        TopLeftLong = [i for i, l in enumerate(long) if l <= LongCenter[index] + DistanceY - DistanceX and l >= LongCenter[index]]

        for i in TopLeftLat:
            for j in TopLeftLong:
                tbb13Area.append(tbb13[i][j])
                tbb15Area.append(tbb15[i][j])
                tbb8Area.append(tbb8[i][j])

        TopRightLat = [i for i, l in enumerate(long) if l <= LatCenter[index] + DistanceY + DistanceX and l >= LatCenter[index]]
        TopRightLong = [i for i, l in enumerate(long) if l <= LongCenter[index] + DistanceY + DistanceX and l >= LongCenter[index]]

        for i in TopRightLat:
            for j in TopRightLong:
                tbb13Area.append(tbb13[i][j])
                tbb15Area.append(tbb15[i][j])
                tbb8Area.append(tbb8[i][j])

        LeftCenterLat = [i for i, l in enumerate(long) if l <= LatCenter[index] - DistanceX and l >= LatCenter[index]]
        LeftCenterLong = [i for i, l in enumerate(long) if l <= LongCenter[index] - DistanceX and l >= LongCenter[index]]

        for i in LeftCenterLat:
            for j in LeftCenterLong:
                tbb13Area.append(tbb13[i][j])
                tbb15Area.append(tbb15[i][j])
                tbb8Area.append(tbb8[i][j])

        RightCenterLat = [i for i, l in enumerate(long) if l <= LatCenter[index] + DistanceX and l >= LatCenter[index]]
        RightCenterLong = [i for i, l in enumerate(long) if l <= LongCenter[index] + DistanceX and l >= LongCenter[index]]

        for i in RightCenterLat:
            for j in RightCenterLong:
                tbb13Area.append(tbb13[i][j])
                tbb15Area.append(tbb15[i][j])
                tbb8Area.append(tbb8[i][j])

        BottonLeftLat = [i for i, l in enumerate(long) if l <= LatCenter[index] - DistanceX - DistanceY and l >= LatCenter[index]]
        BottonLeftLong = [i for i, l in enumerate(long) if l <= LongCenter[index] - DistanceX - DistanceY and l >= LongCenter[index]]

        for i in BottonLeftLat:
            for j in BottonLeftLong:
                tbb13Area.append(tbb13[i][j])
                tbb15Area.append(tbb15[i][j])
                tbb8Area.append(tbb8[i][j])

        BottonRightLat = [i for i, l in enumerate(long) if l <= LatCenter[index] + DistanceX - DistanceY and l >= LatCenter[index]]
        BottonRightLong = [i for i, l in enumerate(long) if l <= LongCenter[index] + DistanceX - DistanceY and l >= LongCenter[index]]

        for i in BottonRightLat:
            for j in BottonRightLong:
                tbb13Area.append(tbb13[i][j])
                tbb15Area.append(tbb15[i][j])
                tbb8Area.append(tbb8[i][j])

        BottonCenterLat = [i for i, l in enumerate(long) if l <= LatCenter[index] - DistanceY and l >= LatCenter[index]]
        BottonCenterLong = [i for i, l in enumerate(long) if l <= LongCenter[index] - DistanceY and l >= LongCenter[index]]
        BottonCenter = []
        for i in BottonCenterLat:
            for j in BottonCenterLong:
                tbb13Area.append(tbb13[i][j])
                tbb15Area.append(tbb15[i][j])
                tbb8Area.append(tbb8[i][j])

        writeTofile.append([date, LatCenter[index], LongCenter[index], np.mean(tbb8Area),np.mean(tbb13Area),np.mean(tbb15Area), a['Rain'][index]])

        tbb13Area=[]
        tbb15Area=[]
        tbb8Area=[]
        print(index)
        #if index==116232:break
    f = pd.DataFrame(writeTofile, columns=['Date', 'Lat', 'Long', 'IR8','IR13','IR15', 'Rain'])
    day = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d")
    time = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").strftime("%H%M")
    WriteToCSV(day+'_'+time,f)

def WriteToCSV(Filename,Frame):
    if os.path.isfile('.\\output\\Pre_{0}.csv'.format(Filename)):
        Frame.to_csv('.\\output\\Pre_{0}.csv'.format(Filename), mode='a', index=False, header=False)
    else:
        Frame.to_csv('.\\output\\Pre_{0}.csv'.format(Filename), mode='w', index=False)

def checkIR8(Filename):
    file = [f for f in os.listdir('.\\Data\\Band8') if f.endswith('.nc') and f==Filename]
    if len(file)>0:
        return True

def checkIR13(Filename):
    file = [f for f in os.listdir('.\\Data\\Band13') if f.endswith('.nc') and f==Filename]
    if len(file)>0:
        return True

def checkIR15(Filename):
    file = [f for f in os.listdir('.\\Data\\Band15') if f.endswith('.nc') and f==Filename]
    if len(file)>0:
        return True
if __name__ == '__main__':
    file = '.\\Data\\5-9_2017.csv'
    pathIR13 = '.\\Data\\'
    header = ['Date', 'Lat', 'Long', 'Rain']
    df = pd.read_csv(file, names=header)
    #print(len(pd.unique(df['Date'])))
    date = pd.unique(df['Date'])
    for dt in date:
        day = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d")
        time = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").strftime("%H%M")
        #print('IR13_'+day+'_'+time+'.nc')
        IR8_check=checkIR8('IR08_'+day+'_'+time+'.nc')
        IR13_check=checkIR13('IR13_' + day + '_' + time + '.nc')
        IR15_check=checkIR15('IR15_' + day + '_' + time + '.nc')
        if IR8_check==True and IR13_check==True and  IR15_check==True:
            IRfile = day+'_'+time+'.nc'
            print(IRfile)
            ReadFile(dt,IRfile)
