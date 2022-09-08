import requests
from bs4 import BeautifulSoup
import json


with open('all_cats.json') as file:
	src_list = json.load(file)


rep = [',', ', ', ' ']


all_iteration = len(src_list)
count = 1
print(f'# Всего итераций -- {all_iteration} #')

for k, v in src_list.items():
	print(f'# Итерация номер -- {count} #')
	count += 1 

	url = v
	if url == 'https://health-diet.ru/base_of_food/food_120438/':
		continue

	product_name_reform = k
	for i in product_name_reform:
		if i in rep:
			product_name_reform = product_name_reform.replace(i, '_')

	req = requests.get(url)
	src = req.text

	soup = BeautifulSoup(src, 'lxml')
	

	heads = soup.find('thead').find('tr').find_all('th')

	product = heads[0].text
	calories = heads[1].text
	proteins = heads[2].text
	fat = heads[3].text
	uglevodi = heads[4].text
	

	products = soup.find('tbody').find_all('tr')
	data_list = {}

	for product_one in products:

		product_data = product_one.find_all('td')

		product_name = product_data[0].text.strip()
		product_calories = product_data[1].text.strip()
		product_proteins = product_data[2].text.strip()
		product_fat = product_data[3].text.strip()
		product_uglevodi = product_data[4].text.strip()

		data_list[product_name] = {
			calories: product_calories,
			proteins: product_proteins,
			fat: product_fat,
			uglevodi: product_uglevodi
		}

	with open(f'res/{product_name_reform}.json', 'w', encoding='utf-8') as file:
		json.dump(data_list, file, indent=4, ensure_ascii=False)