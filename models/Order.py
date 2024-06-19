import datetime


class Order:

    def __init__(self, *args):
        self.order_date = datetime.datetime.strptime(args.order_date, "%Y-%m-%d")
        self.order_id = args.order_id
        self.associate_sale_id = args.associate_sale_id
        self.bussiness_kind = args.bussiness_kind
        self.associate_purchase_order_id = args.associate_purchase_order_id
        self.saler = args.saler
        self.customer = args.customer
        self.sale_price = args.sale_amount
        self.discount_price = args.discount_price
        self.discounted_price = args.discounted_price
        self.order_state = args.order_state
        self.delivery_date = args.delivery_date
        self.order_maker = args.order_maker
        self.order_making_time = args.order_making_time
        self.reviewer = args.reviewer
        self.remark = args.remark
        self.delivery_method = args.delivery_method
        self.print_time = args.print_time
        self.wares = args.wares

        assert self.sale_price == self.discount_price + self.discounted_price, "销售金额、优惠金额与优惠后金额有问题！"

    @classmethod
    def from_dataframe_row(cls, row):
        return cls(**row.to_dict())


if __name__ == "__main__":
    import pandas as pd

    # 读取Excel文件
    file_path = '../data/销货订单导出_202306241022.xlsx'
    df = pd.read_excel(file_path, header=4)
    print(df)
    print(df.columns)

    # 从 DataFrame 构建 Order 对象列表
    orders = [Order.from_dataframe_row(row) for index, row in df.iterrows()]

    # 查看第一个 Order 对象
    print(vars(orders[0]))
