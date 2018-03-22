import pandas as pd
import time
import urllib.request


xls = pd.ExcelFile('/home/v.efimenko/test.Export_test.xlsx')
df = xls.parse(header=0, index_col=None).fillna('')

for row in df.iterrows():
	for link in row[1]['Ссылка_изображения'].split(', '):
		print(link)
		urllib.request.urlretrieve(link, '/home/v.efimenko/test/image {0}.{1}'.format(str(row[0] + 2), link.split('.')[4]))
		time.sleep(3)
