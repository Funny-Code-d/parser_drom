import requests
from bs4 import BeautifulSoup
from bs4.element import AttributeValueWithCharsetSubstitution
from requests.packages import urllib3


class Parser:
	"""
	Класс для сбора информации с сайта Drom.ru

	Параметры: ---

	"""
	def __init__(self):
		self.HEADER = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0', 'accept' : '*/*'}

	def get_html_text(self, url, params=None):
		"""
		Метод для отправки запроса на получение страницы
		Возвращает объект класса BeautifulSoup
		"""
		proxies = {
		# "https" : "178.32.116.64:3128",
		"http" : '46.42.16.245:31565',
		"socks4" : "188.235.34.146:1080",
		"socks5" : "192.111.137.37:18762"
		}
		urllib3.disable_warnings()
		r = requests.get(url, headers=self.HEADER, params=params, proxies=proxies, verify=False)
		if r.status_code == 200:
			soup = BeautifulSoup(r.text, 'html.parser')
			return soup
		elif r.status_code == 404:
			return "PAGE NOT FOUND"
		else:
			return "Undefined code"


	def get_info_fields(self, url, city):
		"""Метод для получения информации об обявлениях со страницы

		Параметры:
		url - Ссылка на страницу
		city - Город

		Возвращает словарь {model_car, url, price, average_price, city}"""
		html = self.get_html_text(url)
		if html == "PAGE NOT FOUND":
			print("Удаляю")
			return "delete"
		else:
			# Получение табличек объявлений
			fields = html.find_all('a', class_='ewrty961')
			iteration = 1
			return_dict = {}
			for item in fields:
				model_car = item.find("span", {"data-ftid":"bull_title"}).get_text(strip=True)
				list_name = model_car.split(',')
				model_car = list_name[0]
				href = item.get("href")
				price = item.find("span", {"data-ftid":"bull_price"}).get_text(strip=True)
				list_price = price.split(' ')
				price = ''
				for i in list_price:
					price += i
				if 0 < int(price) <= 100000:
					average_price = '0-100'
				elif 100000 < int(price) <= 200000:
					average_price = '100-200'
				elif 200000 < int(price) <= 500000:
					average_price = '200-500'
				elif 500000 < int(price) <= 900000:
					average_price = '500-900'
				elif 900000 < int(price) <= 1500000:
					average_price = '900-1500'
				elif 1500000 < int(price) <= 2000000:
					average_price = '1500-2000'
				else:
					average_price = '2000-...'

				return_dict[iteration] = {
				"model_car" : model_car,
				"url" : href,
				"price" : price,
				"average_price" : average_price,
				"city" : city
				}
				iteration += 1
			return return_dict

	def get_info_page_field(self, url):
		"""
		Медот для извлечения информации со страницы объявления

		Параметры:
		url - Ссылка на страницу

		Возвращает словарь с данными {date_publication, number_view, url}
		"""
		html = self.get_html_text(url)

		if html == "PAGE NOT FOUND":
			return "delete"
		elif html == 'Undefined code':
			pass
		else:
			try:
			    check_delete_page = html.find("h1", class_="css-cgwg2n").get_text(strip=True)
			    if check_delete_page == 'Объявление удалено!':
			        return "delete"
			except AttributeError:
			    pass
			number_view = int(html.find("div", class_="css-193s9zx").get_text(strip=True))
			date_text = html.find("div", class_="css-pxeubi").get_text(strip=True)
			# Извлечение даты из декста
			list_date = date_text.split(' ')
			date_pub = list_date[-1].split('.')
			date_publication = date_pub[2] + '-' + date_pub[1] + '-' + date_pub[0]
			# Словарь с извлечёнными данными
			dict_info = {
			"date_publication" : date_publication,
			"number_view" : number_view,
			"url" : url
			}
			return dict_info
