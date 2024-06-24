import sqlite3
from collections import defaultdict

import pandas as pd


# 产品数据结构
class ProductProcess:
    def __init__(self):
        self.data = defaultdict(list)

    def add_process_flow(self, product, process_flow):
        self.data[product].append(process_flow)

    def to_dict(self):
        return dict(self.data)


def load_data(file_path, sheet_name):
    # 读取 Excel 文件
    xls = pd.ExcelFile(file_path)
    # 读取指定表，设置正确的header行
    df = pd.read_excel(xls, sheet_name=sheet_name, header=[1, 2])
    # 填充整个 DataFrame 的缺失值，用前一行数据进行填充
    df = df.ffill()
    return df


def process_data(df):
    # 初始化产品数据结构
    product_processes = ProductProcess()

    # 遍历数据框，收集每个产品型号的工序信息
    for _, row in df.iterrows():
        product = row[('产品型号', 'Unnamed: 1_level_1')]
        process_flow = []
        for i in range(1, 11):  # 工序 1 到 工序 10
            process_info = {
                '工序名称': row.get(('工序' + str(i), '工序名称'), None),
                '加工数量': row.get(('工序' + str(i), '加工数量'), None),
                '加工时间': row.get(('工序' + str(i), '加工时间'), None),
                '设备名称': row.get(('工序' + str(i), '设备名称'), None),
                '统计完成时间': row.get(('工序' + str(i), '统计完成时间（日期）'), None)
            }
            if pd.notna(process_info['工序名称']):  # 只有当工序名称不为空时才添加
                process_flow.append(process_info)
        if process_flow:
            product_processes.add_process_flow(product, process_flow)

    return product_processes


def create_tables(conn):
    cursor = conn.cursor()
    # 创建表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_model TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS process_flows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS processes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flow_id INTEGER,
        process_name TEXT,
        quantity INTEGER,
        duration REAL,
        equipment TEXT,
        completion_date TEXT,
        FOREIGN KEY (flow_id) REFERENCES process_flows (id)
    )
    ''')
    conn.commit()


def insert_data(conn, product_processes):
    cursor = conn.cursor()
    # 插入数据
    for product, flows in product_processes.items():
        # 插入产品数据
        cursor.execute('INSERT INTO products (product_model) VALUES (?)', (product,))
        product_id = cursor.lastrowid

        for flow in flows:
            # 插入工序流程数据
            cursor.execute('INSERT INTO process_flows (product_id) VALUES (?)', (product_id,))
            flow_id = cursor.lastrowid

            for process in flow:
                # 插入具体工序数据
                cursor.execute('''
                INSERT INTO processes (flow_id, process_name, quantity, duration, equipment, completion_date)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    flow_id,
                    process['工序名称'],
                    process['加工数量'],
                    process['加工时间'],
                    process['设备名称'],
                    process['统计完成时间']
                ))
    conn.commit()


def preprocess_process(file_path='../data/产品加工用时统计进度表.xlsx',
                       sheet_name='史密斯',
                       db_path='../database/longtai.db'):
    # 加载数据
    df = load_data(file_path, sheet_name)
    # 处理数据
    product_processes = process_data(df)
    # 连接 SQLite 数据库（如果数据库不存在，将自动创建）
    conn = sqlite3.connect(db_path)
    # 创建表
    create_tables(conn)
    # 插入数据
    insert_data(conn, product_processes.to_dict())
    # 关闭连接
    conn.close()
    print("数据已成功写入 SQLite3 数据库")


if __name__ == "__main__":
    preprocess_process()
