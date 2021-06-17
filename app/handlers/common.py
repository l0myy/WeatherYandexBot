from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from app.bot_logger import log_in_file


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await log_in_file(message=message)
    await message.answer(
        "Выберите, что хотите сделать. Подписаться на рассылку (/subscriber), отписаться от рассылки (/unsubcsribe),"
        "узнать погоду в городе N (/weather).",
        reply_markup=types.ReplyKeyboardRemove()
    )


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await log_in_file(message=message)
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")

