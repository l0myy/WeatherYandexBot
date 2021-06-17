import psycopg2


class PostgreManager:
    def __init__(self, db_name, db_user, db_pass, db_host, db_port):
        # Подключаемся к БД и сохраняем курсор соединения
        self.connection = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status=True):
        # Получаем всех активных подписчиков
        with self.connection:
            sql = f"SELECT * FROM subscriptions WHERE status = {status} and city IS NOT NULL;"
            self.cursor.execute(sql)
            return self.cursor.fetchall()

    def get_city(self, user_id):
        # Получаем город, на который подписан пользователь
        with self.connection:
            sql = f"SELECT user_id, city FROM subscriptions WHERE user_id = '{user_id}';"
            self.cursor.execute(sql)
            return self.cursor.fetchall()

    def subscriber_exists(self, user_id):
        # Проверяем есть ли уже юзер в базе
        with self.connection:
            sql = f"SELECT * FROM subscriptions WHERE user_id = '{user_id}';"
            self.cursor.execute(sql)
            return bool(len(self.cursor.fetchall()))

    def add_subscriber(self, user_id, city, status=True):
        # Добавляем нового подписчика
        with self.connection:
            sql = f"INSERT INTO subscriptions (user_id, status, city) VALUES('{user_id}', {status}, '{city}');"
            return self.cursor.execute(sql)

    def update_subscriber_status(self, user_id, status):
        # Обновляем статус подписки
        with self.connection:
            sql = f"UPDATE subscriptions SET status = {status} WHERE user_id = '{user_id}';"
            return self.cursor.execute(sql)

    def update_subscriber_city(self, user_id, new_city):
        # Обновляем город подписки
        with self.connection:
            sql = f"UPDATE subscriptions SET city = '{new_city}' WHERE user_id = '{user_id}';"
            return self.cursor.execute(sql)

    def close(self):
        # Закрываем соеднинение с БД
        self.connection.close()