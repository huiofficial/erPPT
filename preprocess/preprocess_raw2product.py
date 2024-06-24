import logging
import os
import sqlite3

import pandas as pd

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('./logging/preprocess_raw2product.log')
formatter = logging.Formatter('%(asctime)s | %(filename)s | %(name)s | %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Raw:
    def __init__(self, raw_code, raw_name):
        self.raw_code = raw_code
        self.raw_name = raw_name


class Product:
    def __init__(self, product_code):
        self.product_code = product_code


class Raw2Product:
    def __init__(self, raw, product):
        self.raw = raw
        self.product = product


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS raw (
            raw_id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_code TEXT UNIQUE,
            raw_name TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS product (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_code TEXT UNIQUE
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS raw2product (
            raw_code TEXT,
            product_code TEXT,
            FOREIGN KEY(raw_code) REFERENCES raw(raw_code),
            FOREIGN KEY(product_code) REFERENCES product(product_code)
        )
        ''')

        self.conn.commit()
        logger.info(f"{self.db_name} | Database | raw, product, raw2product | Created tables")

    def insert_raw(self, raw):
        if raw.raw_code and raw.raw_name:  # 检查是否为空
            self.cursor.execute('''
            INSERT OR IGNORE INTO raw(raw_code, raw_name) VALUES (?, ?)
            ''', (raw.raw_code, raw.raw_name))
            self.cursor.execute('SELECT raw_id FROM raw WHERE raw_code = ?', (raw.raw_code,))
            logger.info(
                f"{self.db_name} | raw | raw_code={raw.raw_code}, raw_name={raw.raw_name} | "
                f"Inserted raw material")
            return raw.raw_code
        return None

    def insert_product(self, product):
        if product.product_code:  # 检查是否为空
            self.cursor.execute('''
            INSERT OR IGNORE INTO product (product_code) VALUES (?)
            ''', (product.product_code,))
            self.cursor.execute('SELECT product_code FROM product WHERE product_code = ?',
                                (product.product_code,))
            logger.info(
                f"{self.db_name} | product | product_code={product.product_code} | Inserted finished product")
            return product.product_code
        return None

    def insert_raw_to_product(self, raw_code, product_code):
        if raw_code and product_code:  # 检查是否为空
            self.cursor.execute('''
            INSERT INTO raw2product (raw_code, product_code) VALUES (?, ?)
            ''', (raw_code, product_code))
            self.conn.commit()
            logger.info(
                f"{self.db_name} | raw2product | raw_code={raw_code}, product_code={product_code} | Inserted relationship")

    def close(self):
        self.conn.close()
        logger.info(f"{self.db_name} | Database | | Connection closed")


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
                        product_code = row[col]
                        if pd.notna(product_code):  # 检查是否为空
                            product = Product(product_code)
                            product_code = db.insert_product(product)
                            if product_code:  # 检查插入的product_id是否为空
                                db.insert_raw_to_product(raw_code, product_code)


def preprocess_raw2product(file_path=f"data/毛坯和成品对应表.xlsx", db_path="database/longtai.db"):
    os.makedirs('../database', exist_ok=True)
    db = Database(db_path)
    process_file(file_path, db)
    db.close()


if __name__ == "__main__":
    preprocess_raw2product()
