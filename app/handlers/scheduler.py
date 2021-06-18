import requests
from app.code_to_smile import code_to_smile
import pytz
from app.db.db_methods import PostgreManager
from config.config import DB_PORT, DB_NAME, DB_PASS, DB_USER, DB_HOST, yandex_location_token, yandex_weather_token
from datetime import datetime, timedelta
import logging

from app.bot_logger import log_in_file, log_error_in_file


logger = logging.getLogger(__name__)

# Устанавливаем необходимую временную зону
tz_Moscow = pytz.timezone('Europe/Moscow')

# Устанавливаем соединение с БД
db = PostgreManager(db_name=DB_NAME, db_port=DB_PORT, db_pass=DB_PASS, db_host=DB_HOST, db_user=DB_USER)


# Получаем прогноз погоды по названию города и отправляем его пользователю
async def get_weather_forecast(user_id, city, bot):
    # Получаем координаты введеного города
    city_search = requests.get(
        f"https://geocode-maps.yandex.ru/1.x/?apikey={yandex_location_token}&format=json&geocode={city}")

    # Полученные данные преобразуем из json
    city_data = city_search.json()

    try:
        # Вытаскиваем координаты города
        position = city_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"][
            "pos"].split()
        # Вытаскиваем название города, если пользователь ошибся при вводе названия.
        city = city_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["" \
               "GeocoderMetaData"]["Address"]["Components"][-1]["name"]
    except:
        await bot.send_message(user_id, "\U00002620 Проверьте название города! \U00002620")
        return 0

    try:
        # Получаем данные о погоде на основе переданных координат
        r = requests.get(
            f"https://api.weather.yandex.ru/v1/forecast?lat={position[1]}&lon={position[0]}&lang=ru_RU",
            headers={'X-Yandex-API-Key': yandex_weather_token}
        )
        # Ответ преобразуем из json
        data = r.json()

        # Вытаскиваем данные погоды на завтра
        day_data = data["forecasts"][1]["parts"]["day"]

        # Вытаскиваем описание погоды, чтобы подставить соответствующий смайлик
        weather_description = day_data["condition"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Там творится что-то страшное!!!"

        # Заполняем переменные информацией о погоде
        city = city
        cur_weather = day_data["temp_avg"]
        humidity = day_data["humidity"]
        pressure = day_data["pressure_mm"]
        wind = day_data["wind_speed"]

        # Получаем дату следующего дня
        tomorrow = datetime.today() + timedelta(days=1)

        # Отправляем ответное сообщение с прогонозом погоды
        await bot.send_message(user_id, f"\n***{datetime.now(tz_Moscow).strftime('%d-%m-%Y %H:%M')}***\n"
              f"Прогноз погоды в городе: {city} на {tomorrow.strftime('%d-%m-%Y')}\nТемпература: {cur_weather}C° {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nСкорость ветра: {wind} м/с\n"
              f"Хорошего дня!")

    except:
        await bot.send_message(user_id, "\U00002620 Проверьте название города! \U00002620")
        return 0


# отправляем прогноз погоды всем подписанным пользователям
async def weather_forecast(bot):
    # выбираем всех подписанных пользователей из БД
    result = db.get_subscriptions()
    await log_error_in_file(result)
    for item in range(len(result)):
        # отправляем всем пользователям прогноз погоды
        logger.info(f"Sent weather forecast to user:{result[item][1]} for the city: {result[item][4]}")
        await log_error_in_file(f"Sent weather forecast to user:{result[item][1]} for the city: {result[item][4]}")
        await get_weather_forecast(user_id=result[item][1], city=result[item][4], bot=bot)
