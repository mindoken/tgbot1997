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


markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Сегодня")
btn2 = types.KeyboardButton("Валюта")
btn3 = types.KeyboardButton("Погода")
markup.add(btn1, btn2, btn3)


@bot.message_handler(content_types=['text'])
def startbot(message):
    if message.text == "Сегодня":
        mess = f'Good morning ^_^   today is {str(datetime.date.today())} currency is 1 kw = {currency.current_converted_price} R. weather today is {w.temperature("celsius")["temp"]} degrees and we have { w.detailed_status} '
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
    elif message.text == "Погода":
        mess = f'weather today is {w.temperature("celsius")["temp"]} degrees and we have {w.detailed_status} '
        bot.send_message(message.chat.id, mess, parse_mode='html')
    elif message.text == "Валюта":
        mess = f'currency now : 1 kw = {currency.current_converted_price} R '
        bot.send_message(message.chat.id, mess, parse_mode='html')
    else:
        pass


bot.polling(none_stop=True)
