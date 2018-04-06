from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import pandas as pd

#На вход подается файл экспорта из GA по посещениям справки(первые 4 колонки),
#с колонками: url, views, unique_views, time, video, img_count, text_doc, len_doc

#Цель - заполнить остальные колонки и попытаться определить зависимость количества и времени просмотров от:
#наличия видео на странице, количества изображений, длинны текста.

xls = pd.ExcelFile('/home/v.efimenko/MySpace/Analytics.xlsx')

df = xls.parse('prom', header=0, index_col=None).fillna('')

#Основная функция для скрапинга
#Поскольку на входе url в виде /documents/334 или /questions/101 в этих случаях необходимый тег и его атрибут отличаются

def scrapp(url):

	#Для страниц документации
	
	if 'documents' in url:

		url = 'http://support.prom.ua' + url
		html = urlopen(url)
		bsObj = BeautifulSoup(html)
		doc_html = bsObj.findAll("div", {"class": "b-user-support__user-content b-user-support__user-content_type_document"})[0]
		return [str(doc_html).count('alt=""'), '<iframe' in str(doc_html), doc_html.get_text().strip()]

	elif 'questions' in url:
	
	#Для страниц с вопросами
	
		url = 'http://support.prom.ua' + url
		html = urlopen(url)
		bsObj = BeautifulSoup(html)
		doc_html = bsObj.findAll("blockquote", {"class": "b-teachers-info h-layout-vm-20"})[0]
		return [str(doc_html).count('alt=""'), '<iframe' in str(doc_html), doc_html.get_text().strip()]

	else:
	
	#Для страниц навигации, которые попали в выборку (или поисковых запров)
		return []


for ind in range(len(df.index)):
	try:
		print(df['url'][ind])
		result = scrapp(df['url'][ind])
		df.loc[ind] = [df['url'][ind], df['views'][ind], df['unique_views'][ind], df['time'][ind], result[1], result[0], result[2], len(result[2])]		

	except IndexError:
		continue
	except HTTPError:
		continue


writer = pd.ExcelWriter('result.xlsx')
df.to_excel(writer, 'Sheet1')
writer.save()
