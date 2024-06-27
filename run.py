import logging
import sqlite3
from datetime import datetime, timedelta, time

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('process_log.log')
formatter = logging.Formatter('%(asctime)s | %(filename)s | %(name)s | %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_orders_sorted_by_delivery_date(cursor):
    cursor.execute('SELECT order_id, delivery_date FROM orders ORDER BY delivery_date ASC')
    result = cursor.fetchall()
    if not result:
        raise ValueError("No orders found.")
    return result


def get_order_products(cursor, order_id):
    cursor.execute('SELECT product_code FROM order_products WHERE order_id = ?', (order_id,))
    result = cursor.fetchall()
    if not result:
        raise ValueError(f"No products found for order id: {order_id}")
    return result


def get_process_flow(cursor, product_code):
    product_code = product_code.strip()
    cursor.execute('SELECT flow_id FROM process_flows WHERE TRIM(product_code) = ?', (product_code,))
    result = cursor.fetchone()
    if result is None:
        raise ValueError(f"No process flow found for product code: {product_code}")
    return result[0]


def get_processes(cursor, flow_id):
    cursor.execute('SELECT * FROM processes WHERE flow_id = ?', (flow_id,))
    result = cursor.fetchall()
    if not result:
        raise ValueError(f"No processes found for flow id: {flow_id}")
    return result


def get_exchange_time(cursor, equipment):
    cursor.execute('SELECT exchange_time FROM exchange_type_time WHERE device_name = ?', (equipment,))
    result = cursor.fetchone()
    return int(result[0]) if result else 0


def adjust_for_working_hours(start_time, duration):
    """
    Adjust the given start_time and duration to fit within working hours (9 AM - 12 PM and 2 PM - 6 PM).
    """
    work_start = time(9, 0)
    work_end = time(18, 0)
    lunch_start = time(12, 0)
    lunch_end = time(14, 0)

    end_time = start_time  # 初始化 end_time

    while duration > 0:
        if work_start <= start_time.time() < lunch_start:
            available_time = (datetime.combine(start_time.date(), lunch_start) - start_time).seconds // 60
            if duration <= available_time:
                end_time = start_time + timedelta(minutes=duration)
                duration = 0
            else:
                start_time = start_time + timedelta(minutes=available_time) + timedelta(hours=2)
                duration -= available_time
        elif lunch_end <= start_time.time() < work_end:
            available_time = (datetime.combine(start_time.date(), work_end) - start_time).seconds // 60
            if duration <= available_time:
                end_time = start_time + timedelta(minutes=duration)
                duration = 0
            else:
                start_time = start_time + timedelta(minutes=available_time) + timedelta(hours=15)
                duration -= available_time
        else:
            start_time += timedelta(days=1)
            start_time = start_time.replace(hour=9, minute=0, second=0)

    return start_time, end_time


def process_orders(db_path, start_date=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 获取按交货日期排序的所有订单
    orders = get_orders_sorted_by_delivery_date(cursor)

    equipment_usage = {}
    all_orders_schedule = []

    # 如果未指定开始日期，使用默认值 2023-01-01
    if start_date is None:
        start_date = datetime(2023, 1, 1, 9, 0)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').replace(hour=9, minute=0, second=0, microsecond=0)

    current_time = start_date

    for order_id, delivery_date in orders:
        products = get_order_products(cursor, order_id)
        product_codes = [product[0] for product in products]

        order_schedule = []

        for product_code in product_codes:
            try:
                flow_id = get_process_flow(cursor, product_code)
                processes = get_processes(cursor, flow_id)
            except ValueError as e:
                logger.warning(str(e))
                print(str(e))
                continue

            for process in processes:
                process_id, flow_id, process_name, quantity, duration, equipment, completion_date, flow_range = process

                if equipment in equipment_usage:
                    current_product_code = equipment_usage[equipment]
                    if current_product_code != product_code:
                        exchange_time = get_exchange_time(cursor, equipment)
                        current_time += timedelta(minutes=exchange_time)
                        current_time, _ = adjust_for_working_hours(current_time, 0)

                equipment_usage[equipment] = product_code

                start_time, end_time = adjust_for_working_hours(current_time, duration)
                order_schedule.append((product_code, process_name, equipment, start_time, end_time))
                current_time = end_time

        if not order_schedule:
            continue
        last_completion_time = max(end_time for _, _, _, _, end_time in order_schedule)

        if last_completion_time > datetime.strptime(delivery_date, '%Y-%m-%d'):
            logger.warning(f"Order {order_id} cannot be delivered on time.")
            print(f"Order {order_id} cannot be delivered on time.")
            conn.close()
            return
        else:
            logger.info(f"Order {order_id} can be delivered on time.")
            all_orders_schedule.extend(order_schedule)

    conn.close()

    # 输出生产时间顺序表
    for schedule in all_orders_schedule:
        print(
            f"Product {schedule[0]} - Process {schedule[1]} on equipment {schedule[2]} from {schedule[3]} to {schedule[4]}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process orders.")
    parser.add_argument("--db_path", type=str, default="./database/longtai.db", help="Path to the database file.")
    parser.add_argument("--start_date", type=str, default="2023-01-01",
                        help="Start date for processing in YYYY-MM-DD format.")

    args = parser.parse_args()
    process_orders(args.db_path, args.start_date)