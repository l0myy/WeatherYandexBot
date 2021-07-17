import requests
from datetime import datetime
from config.config import yandex_weather_token, yandex_location_token
from aiogram import types
from aiogram.dispatcher import Dispatcher
import pytz
from app.code_to_smile import code_to_smile
import logging
from app.bot_logger import log_in_file

logger = logging.getLogger(__name__)

# выбираем тайм зону - Europe/Moscow
tz_Moscow = pytz.timezone('Europe/Moscow')


# Метод получения прогноза погоды по введеному пользователю городу
async def get_weather(message: types.Message):
    await log_in_file(message=message)

    full_msg = message.text.split()
    if message.get_args():
        input_city = message.get_args()
    elif message.text in ("/weather"):
        await message.reply("Введите '/weather город' или напишите просто название города боту.")
        return 0
    else:
        input_city = message.text

    # Получаем координаты введеного города
    city_search = requests.get(
        f"https://geocode-maps.yandex.ru/1.x/?apikey={yandex_location_token}&format=json&geocode={input_city}")

    # Полученные данные преобразуем из json
    city_data = city_search.json()

    try:
        # Вытаскиваем координаты города
        position = city_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()
        # Вытаскиваем название города, если пользователь ошибся при вводе названия.
        city = city_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][""\
                         "GeocoderMetaData"]["Address"]["Components"][-1]["name"]
    except:
        await message.reply("\U00002620 Проверьте название города! \U00002620")
        return 0

    try:
        # Получаем данные о погоде на основе переданных координат
        r = requests.get(
            f"https://api.weather.yandex.ru/v2/informers?lat={position[1]}&lon={position[0]}&lang=ru_RU",
            headers={'X-Yandex-API-Key': yandex_weather_token}
        )
        # Ответ преобразуем из json
        data = r.json()
        data = data["fact"]

        # Вытаскиваем описание погоды, чтобы подставить соответствующий смайлик
        weather_description = data["condition"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Там творится что-то страшное!!!"

        # Вытаскиваем необходимые данные о температуре, влажности, скорости ветра и тд.
        cur_weather = data["temp"]
        humidity = data["humidity"]
        pressure = data["pressure_mm"]
        wind = data["wind_speed"]

        logger.info(f"Message from {str(message.from_user.first_name)} {str(message.from_user.last_name)}"
                    f" (id: {str(message.from_user.id)})")
        logger.info(f"Text: {str(message.text)}")

        # Отправляем ответное сообщение с прогонозом погоды
        await message.reply(f"*** {datetime.now(tz_Moscow).strftime('%d.%m.%Y %H:%M')} ***\n"
                            f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nСкорость ветра: {wind} м/с\n"
                            f"Хорошего дня!")

    except:
        await message.reply("\U00002620 Проверьте название города! \U00002620")
        return 0


def register_handlers_weather(dp: Dispatcher):
    dp.register_message_handler(get_weather, commands="weather", state="*")
    dp.register_message_handler(get_weather)
