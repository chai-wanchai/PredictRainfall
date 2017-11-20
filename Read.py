from datetime import datetime
import pandas as pd
from netCDF4 import Dataset
import numpy as np
################ชื่อไฟบล์  CDF
IR13 = Dataset('.\\Data\\Band13\\IR13_20170505_0230.nc', 'r')
FileIR = 'IR13_20170505_0200.nc'
DateTimeIR = FileIR.replace('.nc', '')
DateTimeIR = DateTimeIR.split('_')
DateTimeIR = datetime.strptime(DateTimeIR[1] + DateTimeIR[2], '%Y%m%d%H%M')
DateTimeIR =str(DateTimeIR)

#########################  อ่านไฟล์ csv

#e = datetime.strptime(str2, "%m/%d/%Y %I:%M:%S %p").strftime("%Y-%m-%d %H:%M:%S")

file = '.\\Data\\5-9_2017.csv'

header=['Date','Lat','Long','Rain']
df = pd.read_csv(file,names=header)
print(len(pd.unique(df['Date'])))
print(pd.unique(df['Date']))
a = df[df['Date'] == DateTimeIR]

LatCenter = a['Lat']
LongCenter = a['Long']

lat = np.asarray(IR13.variables['latitude'])
long = np.asarray(IR13.variables['longitude'])
temp = np.asarray(IR13.variables['tbb13'])

tempArea = []
DistanceY = 0.1
DistanceX = 0.1

########
TopCenterLat=[]
TopCenterLong=[]
TopLeftLat=[]
TopLeftLong=[]
TopRightLat=[]
TopRightLong=[]
LeftCenterLat=[]
LeftCenterLong=[]
RightCenterLat=[]
RightCenterLong=[]
BottonLeftLat=[]
BottonLeftLong=[]
BottonRightLat=[]
BottonRightLong=[]
BottonCenterLat=[]
BottonCenterLong=[]

IR13.close()
writeTofile=[]
for index in a.index:
    TopCenterLat = [i for i, l in enumerate(lat) if l <= LatCenter[index] + DistanceY and l >= LatCenter[index]]
    TopCenterLong = [i for i, l in enumerate(long) if l <= LongCenter[index] + DistanceY and l >= LongCenter[index]]
    TopCenter=[]
    for i in TopCenterLat:
        for j in TopCenterLong:
            TopCenter.append(temp[i][j])
    if len(TopCenter)>0 :
        tempArea.append(np.mean(TopCenter))
        TopCenter=[]


    TopLeftLat = [i for i, l in enumerate(long) if l <= LatCenter[index] + DistanceY - DistanceX and l >= LatCenter[index]]
    TopLeftLong = [i for i, l in enumerate(long) if l <= LongCenter[index] + DistanceY - DistanceX and l >= LongCenter[index]]
    TopLeft =[]
    for i in TopLeftLat:
        for j in TopLeftLong:
            TopLeft.append(temp[i][j])
    if len(TopLeft)>0:
        tempArea.append(np.mean(TopLeft))
        TopLeft=[]

    TopRightLat = [i for i, l in enumerate(long) if l <= LatCenter[index] + DistanceY + DistanceX and l >= LatCenter[index]]
    TopRightLong = [i for i, l in enumerate(long) if l <= LongCenter[index] + DistanceY + DistanceX and l >= LongCenter[index]]
    TopRight=[]
    for i in TopRightLat:
        for j in TopRightLong:
            TopRight.append(temp[i][j])
    if len(TopRight) > 0:
        tempArea.append(np.mean(TopRight))
        TopRight=[]

    LeftCenterLat = [i for i, l in enumerate(long) if l <= LatCenter[index] - DistanceX and l >= LatCenter[index]]
    LeftCenterLong = [i for i, l in enumerate(long) if l <= LongCenter[index] - DistanceX and l >= LongCenter[index]]
    LeftCenter =[]
    for i in LeftCenterLat:
        for j in LeftCenterLong:
            LeftCenter.append(temp[i][j])
    if len(LeftCenter) > 0:
        tempArea.append(np.mean(LeftCenter))
        LeftCenter=[]

    RightCenterLat = [i for i, l in enumerate(long) if l <= LatCenter[index] + DistanceX and l >= LatCenter[index]]
    RightCenterLong = [i for i, l in enumerate(long) if l <= LongCenter[index] + DistanceX and l >= LongCenter[index]]
    RightCenter = []
    for i in RightCenterLat:
        for j in RightCenterLong:
            RightCenter.append(temp[i][j])
    if len(RightCenter) > 0:
        tempArea.append(np.mean(RightCenter))
        RightCenter=[]

    BottonLeftLat = [i for i, l in enumerate(long) if l <= LatCenter[index] - DistanceX - DistanceY and l >= LatCenter[index]]
    BottonLeftLong = [i for i, l in enumerate(long) if l <= LongCenter[index] - DistanceX - DistanceY and l >= LongCenter[index]]
    BottonLeft = []
    for i in BottonLeftLat:
        for j in BottonLeftLong:
            BottonLeft.append(temp[i][j])
    if len(BottonLeft) > 0:
        tempArea.append(np.mean(BottonLeft))
        BottonLeft=[]

    BottonRightLat = [i for i, l in enumerate(long) if l <= LatCenter[index] + DistanceX - DistanceY and l >= LatCenter[index]]
    BottonRightLong = [i for i, l in enumerate(long) if l <= LongCenter[index] + DistanceX - DistanceY and l >= LongCenter[index]]
    BottonRight = []
    for i in BottonRightLat:
        for j in BottonRightLong:
            BottonRight.append(temp[i][j])
    if len(BottonRight) > 0:
        tempArea.append(np.mean(BottonRight))
        BottonRight=[]

    BottonCenterLat = [i for i, l in enumerate(long) if l <= LatCenter[index] - DistanceY and l >= LatCenter[index]]
    BottonCenterLong = [i for i, l in enumerate(long) if l <= LongCenter[index] - DistanceY and l >= LongCenter[index]]
    BottonCenter=[]
    for i in BottonCenterLat:
        for j in BottonCenterLong:
            BottonCenter.append(temp[i][j])
    if len(BottonCenter) > 0:
        tempArea.append(np.mean(BottonCenter))
        BottonCenter=[]
    print(index)
    writeTofile.append([DateTimeIR, LatCenter[index], LongCenter[index],np.mean(tempArea) ,a['Rain'][index]])


f = pd.DataFrame(writeTofile,columns=['Date','Lat','Long','IR13','Rain'])
f.to_csv('tes.csv',index=False)

