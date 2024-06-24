import logging
import sqlite3

import pandas as pd

logging.basicConfig(
    filename=__file__,
    level=logging.INFO,
    format='%(asctime)s | %(filename)s | %(name)s | %(message)s')


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS exchange_type_time (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT,
            exchange_time TEXT
        )
        ''')
        self.conn.commit()
        logging.info(f"{self.db_name} | Database | exchange_type_time | Created tables")

    def insert_data(self, device_name, exchange_time):
        self.cursor.execute('''
        INSERT INTO exchange_type_time (device_name, exchange_time)
        VALUES (?, ?)
        ''', (device_name, exchange_time))
        self.conn.commit()
        logging.info(
            f"{self.db_name} | exchange_type_time | Inserted device_name={device_name}, exchange_time={exchange_time}")

    def close(self):
        self.conn.close()
        logging.info(f"{self.db_name} | exchange_type_time | | Connection closed")


def process_file(file_path, db_name):
    df = pd.read_excel(file_path, header=0)
    db = Database(db_name)

    for index, row in df.iterrows():
        if pd.notna(row['设备名称']):
            device_names = row['设备名称'].split('/')
            for device_name in device_names:
                db.insert_data(device_name, row['每班换型时间'])

    db.close()


def preprocess_exchange_type(file_path='../data/换型时间_MES.xlsx', db_name='database/longtai.db'):
    process_file(file_path, db_name)


if __name__ == '__main__':
    preprocess_exchange_type()