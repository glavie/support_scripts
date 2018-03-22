#Поступила просьба от клиента сформировать репозиторий со всеми фотографиями его товаров
#Данный скрипт парсит файл экспорта в DataFrame после чего загружает изображения в указанную папку 


import pandas as pd
import time
import urllib.request


xls = pd.ExcelFile('/home/v.efimenko/test.Export_test.xlsx')
df = xls.parse(header=0, index_col=None).fillna('')

#Итерируемся по строкам DF
for row in df.iterrows():
	#Поскольку в поле ссылки на изображение может быть несколько изображений - необходимо дополнительно итерироваться по
	#списку изображений для каждой позиции.
	for link in row[1]['Ссылка_изображения'].split(', '):
		#На данном этапе происходит загрузка изображения с присваиванием порядкового номера в соответствии с файлом 
		#экспорта и соответствующего формата картинки.
		urllib.request.urlretrieve(link, '/home/v.efimenko/test/image {0}.{1}'.format(str(row[0] + 2), link.split('.')[4]))
		#Дабы не напороться на капчу добавляем интервал выполнения итераций
		time.sleep(3)
