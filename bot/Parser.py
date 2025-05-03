from bs4 import BeautifulSoup  # импортируем библиотеку BeautifulSoup
import requests  # импортируем библиотеку requests


def parse() -> float:
    url = "https://www.sravni.ru/valjuty/cb-rf/usd/"  # передаем необходимы URL адрес

    page = requests.get(url)  # отправляем запрос методом Get
    soup = BeautifulSoup(page.text, "html.parser")  # передаем страницу в bs4
    price = soup.find("label", attrs={'class': True, 'for': True}).text.split(" ")[-2]

    return float(price)
