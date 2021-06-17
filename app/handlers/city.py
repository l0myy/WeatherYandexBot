from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.db.db_methods import PostgreManager
from config.config import DB_PORT, DB_NAME, DB_PASS, DB_USER, DB_HOST

from app.bot_logger import log_in_file


class City(StatesGroup):
    city_name = State()
    subs_status = State()


db = PostgreManager(db_name=DB_NAME, db_port=DB_PORT, db_pass=DB_PASS, db_host=DB_HOST, db_user=DB_USER)


# Запускаем диалог с подпиской
async def subscribe_start(message: types.Message):
    await City.city_name.set()
    await log_in_file(message=message)
    await message.reply("На какой город хочешь подписаться? Если не придумал, напиши 'отмена' в чат.")


# Сюда попадает название города
async def city_chosen(message: types.Message, state: FSMContext):
    await log_in_file(message=message)
    async with state.proxy() as data:
        data['city'] = message.text
    if not db.subscriber_exists(message.from_user.id):
        # Если юзера нет в БД, тогда добавляем его
        db.add_subscriber(message.from_user.id, data['city'])
    else:
        # Если он уже есть в БД, тогда обновляем город и статус
        db.update_subscriber_city(message.from_user.id, data['city'])
        db.update_subscriber_status(message.from_user.id, True)

    # Отправляем сообщение, об успешной подписке
    await message.answer(f"Вы успешно подписались на прогноз погоды в городе : {data['city']}\n"
                         f"Ожидайте уведомления каждый день в 21:00.\n"
                         f"Хорошего дня!")
    await state.finish()


# Отписка через команду в чате
async def unsubscribe(message: types.Message):
    await log_in_file(message=message)
    if not db.subscriber_exists(message.from_user.id):
        # Если юзера нет в БД, тогда добавляем его c неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы не подписаны.")
    else:
        # Если он уже есть в БД, тогда обновляем статус
        db.update_subscriber_status(message.from_user.id, False)
    await message.reply("Вы успешно отписались от рассылки.\n")


def register_handlers_cities(dp: Dispatcher):
    dp.register_message_handler(subscribe_start, commands="subscribe", state="*")
    dp.register_message_handler(city_chosen, state=City.city_name)
    dp.register_message_handler(unsubscribe, commands="unsubscribe", state="*")
