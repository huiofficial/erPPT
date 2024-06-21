import sqlite3

from models import Order
import logging

def init_db(cursor):
    # 创建orders表
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

    # 创建wares表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS wares_in_order (
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
        warehouse TEXT,
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


def insert_order(cursor, order):
    cursor.execute('''
    INSERT INTO orders (
        order_id, order_date, associate_sale_id, business_kind, associate_purchase_order_id, saler, customer,
        sale_amount, discount_price, discounted_price, order_state, delivery_date, order_maker, order_making_time,
        reviewer, remark, delivery_method, print_count
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order.order_id, order.order_date.strftime("%Y-%m-%d"), order.associate_sale_id, order.business_kind,
        order.associate_purchase_order_id, order.saler, order.customer, order.sale_amount, order.discount_price,
        order.discounted_price, order.order_state, order.delivery_date, order.order_maker, order.order_making_time,
        order.reviewer, order.remark, order.delivery_method, order.print_count
    ))


def insert_ware(cursor, ware, order_id):
    ware_dict = vars(ware)
    columns = ', '.join(ware_dict.keys()) + ', order_id'
    placeholders = ', '.join(['?'] * (len(ware_dict) + 1))
    values = list(ware_dict.values()) + [order_id]

    cursor.execute(f'''
        INSERT INTO wares_in_order ({columns})
        VALUES ({placeholders})
        ''', values)

    logging.info(f"Inserted ware: {ware.product_code}")


def order_preprocess(conn):

    cursor = conn.cursor()
    init_db(cursor)

    import pandas as pd

    file_path = './data/销货订单导出_202306241022.xlsx'
    df = pd.read_excel(file_path, header=4).ffill()
    print(df.columns)

    orders = []
    for order_id, group in df.groupby('订单编号'):
        order_row = group.iloc[0]
        wares_rows = group
        order = Order.from_dataframe_rows(order_row, wares_rows)
        orders.append(order)

    for order in orders:
        insert_order(cursor, order)
        for ware in order.wares:
            insert_ware(cursor, ware, order.order_id)

    # 提交插入数据的操作
    conn.commit()

    # 关闭数据库连接


if __name__ == "__main__":
    conn = sqlite3.connect("database/longtai.db")

    order_preprocess(conn)

    conn.close()
