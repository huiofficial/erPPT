import datetime

from .product import Product


class Order:
    def __init__(self, order_date, order_id, associate_sale_id, business_kind, associate_purchase_order_id, saler,
                 customer, sale_amount, discount_price, discounted_price, order_state, delivery_date, order_maker,
                 order_making_time, reviewer, remark, delivery_method, print_count, products):
        self.order_date = datetime.datetime.strptime(order_date, "%Y-%m-%d")
        self.order_id = order_id
        self.associate_sale_id = associate_sale_id
        self.business_kind = business_kind
        self.associate_purchase_order_id = associate_purchase_order_id
        self.saler = saler
        self.customer = customer
        self.sale_amount = sale_amount
        self.discount_price = discount_price
        self.discounted_price = discounted_price
        self.order_state = order_state
        self.delivery_date = delivery_date
        self.order_maker = order_maker
        self.order_making_time = order_making_time
        self.reviewer = reviewer
        self.remark = remark
        self.delivery_method = delivery_method
        self.print_count = print_count
        self.products = products

        assert self.sale_amount == self.discount_price + self.discounted_price, "销售金额、优惠金额与优惠后金额有问题！"

    @classmethod
    def from_dataframe_rows(cls, order_row, products_rows):
        products = [Product.from_dataframe_row(row) for _, row in products_rows.iterrows()]
        return cls(
            order_row['订单日期'],
            order_row['订单编号'],
            order_row['关联销货单号'],
            order_row['业务类别'],
            order_row['关联购货订单号'],
            order_row['销售人员'],
            order_row['客户'],
            order_row['销售金额'],
            order_row['优惠金额'],
            order_row['优惠后金额'],
            order_row['订单状态'],
            order_row['交货日期'],
            order_row['制单人'],
            order_row['制单时间'],
            order_row['审核人'],
            order_row['备注'],
            order_row['交货方式'],
            order_row['打印次数'],
            products
        )


if __name__ == "__main__":
    import pandas as pd

    file_path = '../data/销货订单导出_202306241022.xlsx'
    df = pd.read_excel(file_path, header=4).ffill()
    print(df.columns)

    orders = []
    for order_id, group in df.groupby('订单编号'):
        order_row = group.iloc[0]
        products_rows = group
        order = Order.from_dataframe_rows(order_row, products_rows)
        orders.append(order)

    print(vars(orders[0]))
    for product in orders[0].products:
        print(vars(product))
