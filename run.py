import sqlite3
import logging
from datetime import datetime, timedelta

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('process_log.log')
formatter = logging.Formatter('%(asctime)s | %(filename)s | %(name)s | %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_latest_order_id(cursor):
    cursor.execute('SELECT order_id FROM orders ORDER BY delivery_date ASC LIMIT 1')
    return cursor.fetchone()[0]


def get_order_products(cursor, order_id):
    cursor.execute('SELECT product_code FROM order_products WHERE order_id = ?', (order_id,))
    return cursor.fetchall()


def get_process_flow(cursor, product_code):
    cursor.execute('SELECT flow_id FROM process_flows WHERE product_code = ?', (product_code,))
    return cursor.fetchone()[0]


def get_processes(cursor, flow_id):
    cursor.execute('SELECT * FROM processes WHERE flow_id = ?', (flow_id,))
    return cursor.fetchall()


def get_raw_code(cursor, product_code):
    cursor.execute('SELECT raw_code FROM products WHERE product_code = ?', (product_code,))
    return cursor.fetchone()[0]


def get_exchange_time(cursor, equipment):
    cursor.execute('SELECT exchange_time FROM exchange_type_time WHERE device_name = ?', (equipment,))
    result = cursor.fetchone()
    return result[0] if result else 0


def process_orders(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 获取最近的订单ID
    latest_order_id = get_latest_order_id(cursor)
    logger.info(f"Latest order id: {latest_order_id}")

    # 获取订单中的所有产品
    products = get_order_products(cursor, latest_order_id)
    product_codes = [product[0] for product in products]
    logger.info(f"Products in the latest order: {product_codes}")

    current_time = datetime.now()
    equipment_usage = {}

    for product_code in product_codes:
        # 获取流程ID
        flow_id = get_process_flow(cursor, product_code)

        # 获取所有工序
        processes = get_processes(cursor, flow_id)

        # 获取产品对应的毛坯raw code
        raw_code = get_raw_code(cursor, product_code)

        for process in processes:
            process_id, flow_id, process_name, quantity, duration, equipment, completion_date, flow_range = process

            if equipment in equipment_usage:
                current_raw_code = equipment_usage[equipment]
                if current_raw_code != raw_code:
                    # 需要换型
                    exchange_time = get_exchange_time(cursor, equipment)
                    current_time += timedelta(minutes=exchange_time)

            equipment_usage[equipment] = raw_code

            # 计算工序完成时间
            completion_time = current_time + timedelta(minutes=duration)
            logger.info(
                f"Product {product_code} - Process {process_name} on equipment {equipment} will be completed by {completion_time}")
            current_time = completion_time

    conn.close()


if __name__ == "__main__":
    process_orders('./database/longtai.db')