import telebot
import datetime
import requests
from bs4 import BeautifulSoup  # Модуль для работы с HTML
import pyowm


class Currency:
    # Ссылка на нужную страницу
    Won_RUB = 'http://google.com/finance/quote/KRW-RUB?sa=X&ved=2ahUKEwjW9qri6Oj5AhWyLqYKHUouBd0QmY0JegQIChAb'
    # Заголовки для передачи вместе с URL

    current_converted_price = 0

    def __init__(self):
        self.current_converted_price = float(self.get_currency_price())

    def get_currency_price(self):
        full_page = requests.get(self.Won_RUB)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.find_all("div", class_="YMlKec fxKbKc")
        return convert[0].text


currency = Currency()


owm = pyowm.OWM('efb3419c724aa1f12c1cd2416a3a508a')
mng= owm.weather_manager()
observation = mng.weather_at_place('Chinju,KR')
w = observation.weather
print()


bot = telebot.TeleBot('5554380645:AAHyRhH97JpRnivcwVTf0tZ-KAJ041SiQik')


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Good morning ^_^   today is {str(datetime.date.today())} курс валюты: 1 вона = {currency.current_converted_price} weather today is {w.temperature("celsius")["temp"]}degrees and we have { w.detailed_status} '
    bot.send_message(message.chat.id, mess, parse_mode='html')


bot.polling(none_stop=True)
