from datetime import datetime, timedelta
from aiogram import types
import os
from pathlib import Path

dtn = datetime.now()


# Записываем информацию которая пришла боту в файл
async def log_in_file(message: types.Message):
    curr_date = dtn.strftime('%d%m%Y')
    bot_log_file = open(f"weatherBot_{curr_date}.log", 'a')
    print(dtn.strftime("%d-%m-%Y %H:%M"), 'Пользователь ' + message.from_user.first_name, message.from_user.id,
          'написал следующее: ' + message.text, file=bot_log_file)
    bot_log_file.close()


async def log_error_in_file(error):
    curr_date = dtn.strftime('%d%m%Y')
    bot_log_file = open(f"weatherBot_{curr_date}.log", 'a')
    print(dtn.strftime("%d-%m-%Y %H:%M"), "   ", error)
    bot_log_file.close()


# Удаляем старые лог файлы
async def clean_log_files():
    old_log_date = datetime.today() + timedelta(days=-7)
    file_name = f"weatherBot_{old_log_date.strftime('%d%m%Y')}.log"
    if os.path.isfile(file_name):
        os.remove(file_name)
        print(f"{file_name} deleted successfully.")
    else:
        print("No log files.")


# Удаляем старые файлы логов
async def del_old_log_files():
    p = Path("./")
    glob_pattern = "*.log"
    for f in p.glob(glob_pattern):
        if f.is_file() and (dtn - dtn.fromtimestamp(f.stat().st_mtime)).days >= 5:
            print(f"deleting: [{str(f)}]")
            f.unlink()


# Находим все лог файлы в каталоге
async def find_log_files():
    p = Path("./")
    glob_pattern = "*.log"
    for f in p.glob(glob_pattern):
        if f.is_file():
            print(f"deleting: [{str(f)}]")
