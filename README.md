## Telegram weather bot using Yandex REST API and subscription for the weather forecast.

- Language - Python 3.9
- DB - Postgresql 12
- Telegram bot lib - aiogram

This application and DB built in docker containers.
If you want to check the bot, you can find it @l0myWeatherYandex_bot.

For the correctly install and using, please create a config.py file into config directory.
Add the neccecary API Tokens, DB connection information.

For example:
```
# @BotFather telegram API Token
API_TOKEN = '****'

# DB config_2
DB_HOST = '****'
DB_NAME = '****'
DB_USER = '****'
DB_PASS = '****'
DB_PORT = 5432

# Yandex REST API tokens
yandex_weather_token = '#####'
yandex_location_token = '#####'
```

********************
Also you should create table using CreateDB.sql.
********************
