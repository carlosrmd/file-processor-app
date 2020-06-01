import mysql.connector.pooling
from mysql.connector import IntegrityError
from config import AppConfig


class Item:

    def __init__(self, site, item_id, price, name, description, nickname, start_time):
        self.data = (
            site,
            item_id,
            price,
            name,
            description,
            nickname,
            start_time
        )

    def get_data(self):
        return self.data


class MysqlDatabaseManager:

    def __init__(self):
        self.pool = None

    def init_app(self, app):
        self.pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=32,
            **AppConfig.db_connection_params
        )

    def store_record(self, item):
        current_conn = self.pool.get_connection()
        current_cursor = current_conn.cursor()
        try:
            current_cursor.execute(AppConfig.sql_add_item, item.get_data())
            current_conn.commit()
        except IntegrityError:
            pass
        finally:
            current_cursor.close()
            current_conn.close()


db_connection = MysqlDatabaseManager()
