import pandas as pd
import os

def MixAndCleanFile(pathOfFile,Filename):
    col = ['Date', 'Lat', 'Long', 'avg_IR8', 'max_IR8', 'min_IR8',
           'avg_IR13', 'max_IR13', 'min_IR13',
           'avg_IR15', 'max_IR15', 'min_IR15',
           'diff_avg_IR8-13', 'diff_avg_IR8-15', 'diff_avg_IR13-15',
           'diff_max_IR8-13', 'diff_max_IR8-15', 'diff_max_IR13-15',
           'diff_min_IR8-13', 'diff_min_IR8-15', 'diff_min_IR13-15',
           'Rain']

    datatype = {'Date': str, 'Lat': float, 'Long': float,
                'avg_IR8': float, 'max_IR8': float, 'min_IR8': float,
                'avg_IR13': float, 'max_IR13': float, 'min_IR13': float,
                'avg_IR15': float, 'max_IR15': float, 'min_IR15': float,
                'diff_avg_IR8-13': float, 'diff_avg_IR8-15': float, 'diff_avg_IR13-15': float,
                'diff_max_IR8-13': float, 'diff_max_IR8-15': float, 'diff_max_IR13-15': float,
                'diff_min_IR8-13': float, 'diff_min_IR8-15': float, 'diff_min_IR13-15': float,
                'Rain': float}


    df = pd.read_csv(pathOfFile)


    NoneFile = df[df['Rain'] != 'None']
    NoneFile.astype(datatype)
    result = pd.DataFrame(NoneFile, columns=col)
    result.to_csv('Clean_{0}'.format(Filename), mode='w', index=False)

if __name__ == '__main__':
    
    pathIn = input("Address of file to clean :")#'/home/team7/hackathon/Prepreocess_Test.csv'
    file = [f for f in os.listdir(pathIn) if f.endswith('.csv')]
    for i,f in enumerate(file):
        print(i,f)
    s = int(input("select:"))
    pathIn = pathIn+file[s]
    #pathOut =input("Path of output file:")#'/home/team7/hackathon/'
    MixAndCleanFile(pathIn,file[s])
   