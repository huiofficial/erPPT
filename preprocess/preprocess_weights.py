import logging
import sqlite3
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('db_operations.log')
formatter = logging.Formatter('%(asctime)s | %(filename)s | %(name)s | %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def add_column_if_not_exists(cursor, table_name, column_name, column_type="TEXT"):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]
    if column_name not in columns:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
        logger.info(f"Added column {column_name} to {table_name} table")


def update_product_weights(cursor, weights):
    # 如果表中没有Weight列，添加Weight列
    add_column_if_not_exists(cursor, 'products', 'weight', 'REAL')

    # 更新产品重量
    for product_code, weight in weights.items():
        cursor.execute('UPDATE products SET Weight = ? WHERE product_code = ?', (weight, product_code))
        logger.info(f"Updated product {product_code} with weight {weight}")


def load_weight_data(file_path):
    # 读取 Excel 文件
    df = pd.read_excel(file_path)

    # 转换为字典
    weights = dict(zip(df['PartNumber零件号码'], df['Weight重量(kg)']))
    return weights


def update_weights(file_path, db_path='../database/longtai.db'):
    # 加载重量数据
    weights = load_weight_data(file_path)

    # 连接 SQLite 数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 更新产品重量
    update_product_weights(cursor, weights)

    # 提交更改并关闭连接
    conn.commit()
    conn.close()

    logger.info("Done updating product weights")


if __name__ == "__main__":
    weight_file_path = '../data/净重.xlsx'
    update_weights(weight_file_path)