import logging
import sqlite3

import pandas as pd

from models import Order

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def init_db(conn):
    cursor = conn.cursor()
    # 创建 orders 表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        order_date TEXT,
        associate_sale_id TEXT,
        business_kind TEXT,
        associate_purchase_order_id TEXT,
        saler TEXT,
        customer TEXT,
        sale_amount REAL,
        discount_price REAL,
        discounted_price REAL,
        order_state TEXT,
        delivery_date TEXT,
        order_maker TEXT,
        order_making_time TEXT,
        reviewer TEXT,
        remark TEXT,
        delivery_method TEXT,
        print_count INTEGER
    )
    ''')

    # 创建 products 表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products_in_order (
        product_code TEXT,
        product_name TEXT,
        product_model TEXT,
        attribute TEXT,
        barcode TEXT,
        category TEXT,
        product_remark TEXT,
        unit TEXT,
        quantity INTEGER,
        sale_price REAL,
        estimated_purchase_price REAL,
        discount_rate REAL,
        discount_amount REAL,
        discount REAL,
        discounted_price REAL,
        amount REAL,
        reference_cost REAL,
        estimated_gross_profit REAL,
        estimated_gross_profit_rate REAL,
        latest_purchase_price REAL,
        product_house TEXT,
        remark TEXT,
        available_stock INTEGER,
        basic_unit TEXT,
        basic_unit_quantity INTEGER,
        whole_scatter TEXT,
        conversion_formula TEXT,
        is_gift TEXT,
        shelf TEXT,
        undelivered_quantity INTEGER,
        undelivered_basic_quantity INTEGER,
        delivered_quantity INTEGER,
        delivered_basic_quantity INTEGER,
        row_status TEXT,
        custom_column_one TEXT,
        custom_column_two TEXT,
        custom_column_three TEXT,
        custom_column_four TEXT,
        custom_column_five TEXT,
        order_id TEXT,
        FOREIGN KEY(order_id) REFERENCES orders(order_id)
    )
    ''')

    # 提交创建表的操作
    conn.commit()
    logger.info(f"Initialized database and created tables")


def insert_order(cursor, order):
    order_dict = vars(order)
    order_dict['order_date'] = order.order_date.strftime("%Y-%m-%d")  # 格式化日期

    # 获取除了最后一个键值对以外的所有键值对
    order_dict_items = list(order_dict.items())[:-1]
    order_dict = dict(order_dict_items)

    columns = ', '.join(order_dict.keys())
    placeholders = ', '.join(['?'] * len(order_dict))
    values = list(order_dict.values())

    cursor.execute(f'''
        INSERT INTO orders ({columns})
        VALUES ({placeholders})
        ''', values)

    logger.info(f"Inserted order: {order.order_id}")


def insert_product(cursor, product, order_id):
    product_dict = vars(product)
    columns = ', '.join(product_dict.keys()) + ', order_id'
    placeholders = ', '.join(['?'] * (len(product_dict) + 1))
    values = list(product_dict.values()) + [order_id]

    cursor.execute(f'''
        INSERT INTO products_in_order ({columns})
        VALUES ({placeholders})
        ''', values)

    logger.info(f"Inserted product: {product.product_code}")


def preprocess_orders(file_path='./data/销货订单导出_202306241022.xlsx', db_path="./database/longtai.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    init_db(conn)

    df = pd.read_excel(file_path, header=4).ffill()

    orders = []
    for order_id, group in df.groupby('订单编号'):
        order_row = group.iloc[0]
        products_rows = group
        order = Order.from_dataframe_rows(order_row, products_rows)
        orders.append(order)

    for order in orders:
        insert_order(cursor, order)
        for product in order.products:
            insert_product(cursor, product, order.order_id)

    # 提交插入数据的操作
    conn.commit()
    logger.info(f"Processed orders from {file_path}")
    conn.close()


if __name__ == "__main__":
    preprocess_orders()
