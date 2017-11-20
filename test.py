
from datetime import datetime
str1 ='2017-05-01 00:00:00'
str2 = '5/1/2017  1:00:00 AM'
str2 = datetime.strptime(str2, "%m/%d/%Y %I:%M:%S %p").strftime("%Y-%m-%d %H:%M:%S")
print(str2)
print(datetime.strptime(str2, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d'))
print(datetime.strptime(str1, '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S'))

a = '20160228'
date = datetime.strptime(a, '%Y%m%d').strftime('%m%d%Y')
print(date)


