import logging
import os
import sqlite3

import pandas as pd

# 配置日志
logging.basicConfig(
    filename='db_operations.log',
    level=logging.INFO,
    format='%(asctime)s | %(filename)s | %(name)s | %(message)s'
)


class Raw:
    def __init__(self, raw_code, raw_name):
        self.raw_code = raw_code
        self.raw_name = raw_name


class Ware:
    def __init__(self, ware_code):
        self.ware_code = ware_code


class RawToWare:
    def __init__(self, raw, ware):
        self.raw = raw
        self.ware = ware


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS raws (
            raw_id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_code TEXT UNIQUE,
            raw_name TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS wares (
            ware_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ware_code TEXT UNIQUE
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS raw_to_ware (
            raw_code TEXT,
            ware_code TEXT,
            FOREIGN KEY(raw_code) REFERENCES raws(raw_code),
            FOREIGN KEY(ware_code) REFERENCES wares(ware_code)
        )
        ''')

        self.conn.commit()
        logging.info(f"{self.db_name} | Database | raws, wares, raw_to_ware | Created tables")

    def insert_raw(self, raw):
        if raw.raw_code and raw.raw_name:  # 检查是否为空
            self.cursor.execute('''
            INSERT OR IGNORE INTO raws (raw_code, raw_name) VALUES (?, ?)
            ''', (raw.raw_code, raw.raw_name))
            self.cursor.execute('SELECT raw_id FROM raws WHERE raw_code = ?', (raw.raw_code,))
            logging.info(
                f"{self.db_name} | raws | raw_code={raw.raw_code}, raw_name={raw.raw_name} | "
                f"Inserted raw material")
            print(f"{self.db_name} | raws | raw_code={raw.raw_code}, raw_name={raw.raw_name} | "
                f"Inserted raw material")
            return raw.raw_code
        return None

    def insert_ware(self, ware):
        if ware.ware_code:  # 检查是否为空
            self.cursor.execute('''
            INSERT OR IGNORE INTO wares (ware_code) VALUES (?)
            ''', (ware.ware_code,))
            self.cursor.execute('SELECT ware_code FROM wares WHERE ware_code = ?', (ware.ware_code,))
            logging.info(
                f"{self.db_name} | wares | ware_code={ware.ware_code} | Inserted finished product")
            print(f"{self.db_name} | wares | ware_code={ware.ware_code} | Inserted finished product")
            return ware.ware_code
        return None

    def insert_raw_to_ware(self, raw_code, ware_code):
        if raw_code and ware_code:  # 检查是否为空
            self.cursor.execute('''
            INSERT INTO raw_to_ware (raw_code, ware_code) VALUES (?, ?)
            ''', (raw_code, ware_code))
            self.conn.commit()
            print(raw_code, ware_code)
            logging.info(f"{self.db_name} | raw_to_ware | raw_code={raw_code}, ware_code={ware_code} | Inserted relationship")

    def close(self):
        self.conn.close()
        logging.info(f"{self.db_name} | Database | | Connection closed")


def process_file(file_path, db):
    df = pd.read_excel(file_path, header=1)

    for index, row in df.iterrows():
        if pd.notna(row['毛坯料号']) or pd.notna(row['中文名称']):  # 检查毛坯编码和名称是否为空
            raw = Raw(row['毛坯料号'], row['中文名称'])
            raw_code = db.insert_raw(raw)

            if raw_code:  # 检查插入的raw_id是否为空
                # 遍历商品编号列，插入对应的商品
                for col in df.columns:
                    if col.startswith('商品编号'):
                        ware_code = row[col]
                        if pd.notna(ware_code):  # 检查是否为空
                            ware = Ware(ware_code)
                            ware_code = db.insert_ware(ware)
                            if ware_code:  # 检查插入的ware_id是否为空
                                db.insert_raw_to_ware(raw_code, ware_code)


if __name__ == "__main__":
    os.makedirs('database', exist_ok=True)
    db = Database('database/longtai.db')
    process_file('data/毛坯和成品对应表.xlsx', db)
    db.close()
