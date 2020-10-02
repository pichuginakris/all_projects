import requests
import csv
from bs4 import BeautifulSoup

url1 = 'http://www.cbr.ru/scripts/XML_daily.asp?'
response = requests.get(url1)
html = response.text
soup = BeautifulSoup(html, 'lxml')
valutes = soup.find('html').find_all('valute')

for valute in valutes:
    id = valute.find('numcode').text
    nominal = valute.find('nominal').text
    if id == '356':
        rupiy = float(valute.find('value').text.replace(',', '.')) / float(nominal)
    if id == '826':
        funt = float(valute.find('value').text.replace(',', '.')) / float(nominal)
    if id == '978':
        euro = float(valute.find('value').text.replace(',', '.')) / float(nominal)
    if id == '710':
        rend = float(valute.find('value').text.replace(',', '.')) / float(nominal)
    if id == '840':
        dollar = float(valute.find('value').text.replace(',', '.')) / float(nominal)
print(rupiy)
all_symbols = ['₹', 'R', '£', '€']
with open ('indeed_India.csv', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    lines = list(reader)
    for line in lines:
        pointer = "False"
        sum1 = ''
        sum2 = ''
        money = str(line['Salary']).replace(',', '')
        if len(money) > 0:
            for one_sym in all_symbols:
                if money[0] == one_sym:
                    pointer = 'True'
            if pointer == 'True':
                k = 0
                while k < (len(money)):
                    if sum1 == '' and sum2 == '':
                        while '0' <= money[k] <= '9':
                            sum1 = sum1 + (money[k])
                            k = k + 1
                    if sum1 != '' and sum2 == '':
                        while '0' <= money[k] <= '9':
                            sum2 = sum2 + (money[k])
                            k = k + 1
                    k = k + 1
                print(sum1)
                if money[0] == all_symbols[0]:
                    sum1 = float(sum1) * rupiy / dollar
                    if sum2 != '':
                        sum2 = float(sum2) * rupiy / dollar
                if money[0] == all_symbols[1]:
                    sum1 = float(sum1) * rend / dollar
                    if sum2 != '':
                        sum2 = float(sum2) * rend / dollar
                if money[0] == all_symbols[2]:
                    sum1 = float(sum1) * funt / dollar
                    if sum2 != '':
                        sum2 = float(sum2) * funt / dollar
                if money[0] == all_symbols[3]:
                    sum1 = float(sum1) * euro / dollar
                    if sum2 != '':
                        sum2 = float(sum2) * euro / dollar


