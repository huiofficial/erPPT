class Product:
    def __init__(self, product_code, product_name, product_model, attribute, barcode, category, product_remark, unit,
                 quantity, sale_price, estimated_purchase_price, discount_rate, discount_amount, discount,
                 discounted_price, amount, reference_cost, estimated_gross_profit, estimated_gross_profit_rate,
                 latest_purchase_price, product_house, remark, available_stock, basic_unit, basic_unit_quantity,
                 whole_scatter, conversion_formula, is_gift, shelf, undelivered_quantity, undelivered_basic_quantity,
                 delivered_quantity, delivered_basic_quantity, row_status, custom_column_one, custom_column_two,
                 custom_column_three, custom_column_four, custom_column_five):
        self.product_code = product_code
        self.product_name = product_name
        self.product_model = product_model
        self.attribute = attribute
        self.barcode = barcode
        self.category = category
        self.product_remark = product_remark
        self.unit = unit
        self.quantity = quantity
        self.sale_price = sale_price
        self.estimated_purchase_price = estimated_purchase_price
        self.discount_rate = discount_rate
        self.discount_amount = discount_amount
        self.discount = discount
        self.discounted_price = discounted_price
        self.amount = amount
        self.reference_cost = reference_cost
        self.estimated_gross_profit = estimated_gross_profit
        self.estimated_gross_profit_rate = estimated_gross_profit_rate
        self.latest_purchase_price = latest_purchase_price
        self.product_house = product_house
        self.remark = remark
        self.available_stock = available_stock
        self.basic_unit = basic_unit
        self.basic_unit_quantity = basic_unit_quantity
        self.whole_scatter = whole_scatter
        self.conversion_formula = conversion_formula
        self.is_gift = is_gift
        self.shelf = shelf
        self.undelivered_quantity = undelivered_quantity
        self.undelivered_basic_quantity = undelivered_basic_quantity
        self.delivered_quantity = delivered_quantity
        self.delivered_basic_quantity = delivered_basic_quantity
        self.row_status = row_status
        self.custom_column_one = custom_column_one
        self.custom_column_two = custom_column_two
        self.custom_column_three = custom_column_three
        self.custom_column_four = custom_column_four
        self.custom_column_five = custom_column_five

    @classmethod
    def from_dataframe_row(cls, row):
        return cls(
            row['商品编码'],
            row['商品名称'],
            row['商品型号'],
            row['属性'],
            row['商品条码'],
            row['商品类别'],
            row['商品备注'],
            row['单位'],
            row['数量'],
            row['销售单价'],
            row['预计采购价'],
            row['折扣率(%)'],
            row['折扣额'],
            row['折扣(折)'],
            row['折后单价'],
            row['金额'],
            row['参考成本'],
            row['预估毛利'],
            row['预估毛利率%'],
            row['最近一次采购价'],
            row['仓库'],
            row['备注.1'],
            row['可用库存'],
            row['基本单位'],
            row['基本单位数量'],
            row['整件散包'],
            row['换算公式'],
            row['是否赠品'],
            row['货架'],
            row['未出库数量'],
            row['未出库基本数量'],
            row['已出库数量'],
            row['已出库基本数量'],
            row['行状态'],
            row['自定义列一'],
            row['自定义列二'],
            row['自定义列三'],
            row['自定义列四'],
            row['自定义列五']
        )

    def __repr__(self):
        return f"商品编码: {self.product_code}, 商品名称: {self.product_name}, 商品型号: {len(self.product_model)}"
