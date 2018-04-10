from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import pandas as pd

#На вход подается файл экспорта из GA по посещениям справки(первые 4 колонки),
#с колонками: url, views, unique_views, time, img_count, video, text_doc, len_doc

#Цель - заполнить остальные колонки и попытаться определить зависимость количества и времени просмотров от:
#наличия видео на странице, количества изображений, длинны текста.

xls = pd.ExcelFile('/home/v.efimenko/MySpace/Analytics.xlsx')

df = xls.parse('prom', header=0, index_col=None).fillna('')

#Основная функция для скрапинга
#Поскольку на входе url в виде /documents/334 или /questions/101 в этих случаях необходимый тег и его атрибут отличаются

def scrapp(url):

	url = 'http://support.prom.ua' + url
	html = urlopen(url)
	bsObj = BeautifulSoup(html)

	if 'documents' in url:

		doc_html = bsObj.findAll("div", {"class": "b-user-support__user-content b-user-support__user-content_type_document"})[0]

	else:

		doc_html = bsObj.findAll("blockquote", {"class": "b-teachers-info h-layout-vm-20"})[0]
		
	return [str(doc_html).count('alt=""'), '<iframe' in str(doc_html), doc_html.get_text().strip()]


for ind in range(len(df.index)):

	url = df['url'][ind]

	try:
		print(url)
		result = scrapp(url)
		df.loc[ind] = list(df.loc[ind][:4]) + result + [len(result[2])]		

	except (IndexError, HTTPError) as e:
		continue



writer = pd.ExcelWriter('result.xlsx')
df.to_excel(writer, 'Sheet1')
writer.save()
