import pymysql
from dotenv import load_dotenv
import os


class Db:
    def __init__(self):
        load_dotenv()
        self._host = os.getenv("DB_HOST")
        self._port = int(os.getenv("DB_PORT"))
        self._user = os.getenv("DB_USER")
        self._password = os.getenv("DB_PASSWORD")
        self._database = os.getenv("DB_DATABASE")
        self._connection = pymysql.connect(
            host=self._host, port=self._port, user=self._user, password=self._password, database=self._database)

        self._table = "Orders"

    # insert data into database
    def insert(self, table, data):
        with self._connection.cursor() as cursor:
            sql = "INSERT INTO " + table + " VALUES " + data
            print(sql)
            cursor.execute(sql)
        self._connection.commit()

    # update data in database
    def update(self, table, data, where):
        with self._connection.cursor() as cursor:
            sql = "UPDATE " + table + " SET " + data + " WHERE " + where
            cursor.execute(sql)
        self._connection.commit()

    # delete data from database
    def delete(self, table, where):
        with self._connection.cursor() as cursor:
            sql = "DELETE FROM " + table + " WHERE " + where
            cursor.execute(sql)
        self._connection.commit()

    # select data from database
    def select(self, table, where):
        with self._connection.cursor() as cursor:
            sql = "SELECT * FROM " + table + " WHERE " + where + ";"
            print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
        return result

    def select_all(self, table):
        with self._connection.cursor() as cursor:
            sql = "SELECT * FROM " + table + ";"
            print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
        return result


class Orders(Db):
    def __init__(self):
        super().__init__()

    def get_next_order_id(self):
        with self._connection.cursor() as cursor:
            sql = "SELECT MAX(ID) FROM " + self._table + ";"
            cursor.execute(sql)
            result = cursor.fetchone()
        return result[0] + 1

    def create_order(self, id, name, email, phone, address, type):
        data = "('" + str(id) + "', '" + name + "', '" + address + "', '" + \
            type + "', '" + phone + "', '" + email + "', 'PENDING')"
        try:
            print(data)
            self.insert(self._table, data)
            return True
        except:
            return False
