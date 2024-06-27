import argparse
import logging

from common.utils import log_execution
from preprocess import preprocess_orders, preprocess_process, preprocess_exchange_type, preprocess_raw2product, preprocess_weights

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@log_execution
def preprocess(args):
    preprocess_exchange_type(file_path=args.exchange_type_file_path, db_path=args.db_path)
    preprocess_raw2product(file_path=args.raw_product_file_path, db_path=args.db_path)
    preprocess_process(file_path=args.process_file_path, db_path=args.db_path)
    preprocess_weights(file_path=args.weights_file_path, db_path=args.db_path)
    preprocess_orders(file_path=args.order_file_path, db_path=args.db_path)


def main(args):
    preprocess(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess data and save to database.")
    parser.add_argument('--db_path', type=str, default='database/longtai.db', help='Path to the database file')
    parser.add_argument('--exchange_type_file_path', type=str, default='data/换型时间_MES.xlsx',
                        help='Path to the exchange type file')
    parser.add_argument('--raw_product_file_path', type=str, default='data/毛坯和成品对应表.xlsx',
                        help='Path to the raw product file')
    parser.add_argument('--order_file_path', type=str, default='data/销货订单导出_202306241022.xlsx',
                        help='Path to the order file')
    parser.add_argument('--weights_file_path', type=str, default='data/净重.xlsx',
                        help='Path to the weights file')
    parser.add_argument('--process_file_path', type=str, default='data/产品加工用时统计进度表.xlsx',
                        help='Path to the process file')

    args = parser.parse_args()
    main(args)
