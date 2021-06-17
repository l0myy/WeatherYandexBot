import logging

import asyncio
import aioschedule

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.handlers.common import register_handlers_common
from app.handlers.city import register_handlers_cities
from app.handlers.buttons import register_handlers_buttons
from app.handlers.scheduler import weather_forecast
from app.handlers.weather import register_handlers_weather
from app.bot_logger import clean_log_files

from config.config import *

logger = logging.getLogger(__name__)


# Установка команд бота
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="subscribe", description="Подписаться на рассылку"),
        BotCommand(command="unsubscribe", description="Отписаться от рассылки"),
        BotCommand(command="weather", description="Узнать погоду в городе N"),
        BotCommand(command="buttons", description="Вывести кнопки для управления ботом")
    ]
    await bot.set_my_commands(commands)


async def scheduler(bot: Bot):
    # указываем время UTC (Moscow time - 3 hours)
    aioschedule.every().day.at("19:00").do(clean_log_files)
    aioschedule.every().day.at("18:00").do(weather_forecast, bot)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",)
    logger.error("Starting bot")

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_handlers_cities(dp)
    register_handlers_buttons(dp)
    register_handlers_weather(dp)

    # Создаем задание на отправку прогноза погоды подписчикам
    asyncio.create_task(scheduler(bot))

    # Запуск поллинга
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
