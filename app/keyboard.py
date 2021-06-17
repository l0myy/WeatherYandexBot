from aiogram import types


# Генерация клавиатуры
def get_keyboard():
    buttons = [
        types.InlineKeyboardButton(text="Подписаться", callback_data="subscribe_button"),
        types.InlineKeyboardButton(text="Отписаться", callback_data="unsubscribe_button"),
        # types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")
    ]
    # Размер кнопок row_width=2 чтобы было 2 кнопки в ряд
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard
