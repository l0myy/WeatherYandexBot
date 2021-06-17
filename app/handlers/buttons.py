from aiogram import types, Dispatcher
from app.keyboard import get_keyboard
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from app.db.db_methods import PostgreManager
from config.config import DB_PORT, DB_NAME, DB_PASS, DB_USER, DB_HOST
from app.bot_logger import log_in_file

# Устанавливаем соединение с БД
db = PostgreManager(db_name=DB_NAME, db_port=DB_PORT, db_pass=DB_PASS, db_host=DB_HOST, db_user=DB_USER)


# Объявляем класс для состояний
class Button(StatesGroup):
    city_name = State()


# Команда для вывода кнопок на экран
async def keyboard_command(message: types.Message):
    await log_in_file(message=message)
    await message.answer("Выберите действие:", reply_markup=get_keyboard())


# Подписка с помощью кнопок
async def process_callback_subscribe_button(callback_query: types.CallbackQuery):
    await callback_query.message.answer("На какой город хочешь подписаться? Если не придумал, напиши 'отмена' в чат.")
    await callback_query.answer()
    await Button.city_name.set()


# Сюда попадает название города после ввода
async def city_chosen_buttons(message: types.Message, state: FSMContext):
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


# Отписка с помощью кнопок
async def process_callback_unsubscribe_button(callback_query: types.CallbackQuery):
    if not db.subscriber_exists(callback_query.from_user.id):
        # Если юзера нет в БД, тогда добавляем его
        db.add_subscriber(callback_query.from_user.id, False)
        await callback_query.message.answer("Вы не подписаны.")
    else:
        # Если он уже есть в БД, тогда обновляем статус
        db.update_subscriber_status(callback_query.from_user.id, False)
    await callback_query.answer()
    await callback_query.message.answer("Вы успешно отписались от рассылки.\n")


def register_handlers_buttons(dp: Dispatcher):
    dp.register_message_handler(keyboard_command, commands="buttons")
    dp.register_callback_query_handler(process_callback_subscribe_button, lambda c: c.data == 'subscribe_button')
    dp.register_callback_query_handler(process_callback_unsubscribe_button, lambda c: c.data == 'unsubscribe_button')
    dp.register_message_handler(city_chosen_buttons, state=Button.city_name)
