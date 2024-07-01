from django.db import models


class ExchangeTypeTime(models.Model):
    device_name = models.CharField(max_length=255, unique=True)
    exchange_time = models.CharField(max_length=255)
    current_raw = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.device_name


class Order(models.Model):
    order_id = models.CharField(max_length=255, primary_key=True)
    order_date = models.CharField(max_length=255)
    associate_sale_id = models.CharField(max_length=255, blank=True, null=True)
    business_kind = models.CharField(max_length=255, blank=True, null=True)
    associate_purchase_order_id = models.CharField(max_length=255, blank=True, null=True)
    saler = models.CharField(max_length=255, blank=True, null=True)
    customer = models.CharField(max_length=255, blank=True, null=True)
    sale_amount = models.FloatField()
    discount_price = models.FloatField()
    discounted_price = models.FloatField()
    order_state = models.CharField(max_length=255, blank=True, null=True)
    delivery_date = models.CharField(max_length=255)
    order_maker = models.CharField(max_length=255, blank=True, null=True)
    order_making_time = models.CharField(max_length=255, blank=True, null=True)
    reviewer = models.CharField(max_length=255, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    delivery_method = models.CharField(max_length=255, blank=True, null=True)
    print_count = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.order_id


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_code = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    product_model = models.CharField(max_length=255)
    attribute = models.CharField(max_length=255, blank=True, null=True)
    barcode = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    product_remark = models.TextField(blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField()
    sale_price = models.FloatField()
    estimated_purchase_price = models.FloatField(blank=True, null=True)
    discount_rate = models.FloatField(blank=True, null=True)
    discount_amount = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    discounted_price = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    reference_cost = models.FloatField(blank=True, null=True)
    estimated_gross_profit = models.FloatField(blank=True, null=True)
    estimated_gross_profit_rate = models.FloatField(blank=True, null=True)
    latest_purchase_price = models.FloatField(blank=True, null=True)
    product_house = models.CharField(max_length=255, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    available_stock = models.IntegerField(blank=True, null=True)
    basic_unit = models.CharField(max_length=255, blank=True, null=True)
    basic_unit_quantity = models.IntegerField(blank=True, null=True)
    whole_scatter = models.CharField(max_length=255, blank=True, null=True)
    conversion_formula = models.CharField(max_length=255, blank=True, null=True)
    is_gift = models.BooleanField(default=False)
    shelf = models.CharField(max_length=255, blank=True, null=True)
    undelivered_quantity = models.IntegerField(blank=True, null=True)
    undelivered_basic_quantity = models.IntegerField(blank=True, null=True)
    delivered_quantity = models.IntegerField(blank=True, null=True)
    delivered_basic_quantity = models.IntegerField(blank=True, null=True)
    row_status = models.CharField(max_length=255, blank=True, null=True)
    custom_column_one = models.CharField(max_length=255, blank=True, null=True)
    custom_column_two = models.CharField(max_length=255, blank=True, null=True)
    custom_column_three = models.CharField(max_length=255, blank=True, null=True)
    custom_column_four = models.CharField(max_length=255, blank=True, null=True)
    custom_column_five = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.order_id} - {self.product_code}"


class Raw(models.Model):
    raw_code = models.CharField(max_length=255, unique=True)
    raw_name = models.CharField(max_length=255)

    def __str__(self):
        return self.raw_code


class Product(models.Model):
    product_code = models.CharField(max_length=255, unique=True)
    product_category = models.CharField(max_length=255, blank=True, null=True)
    raw = models.ForeignKey(Raw, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.product_code


class ProcessFlow(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.product_code} - Flow {self.id}"


class Process(models.Model):
    flow = models.ForeignKey(ProcessFlow, on_delete=models.CASCADE)
    process_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    duration = models.FloatField()
    equipment = models.CharField(max_length=255)
    completion_date = models.CharField(max_length=255)
    flow_range = models.IntegerField()

    def __str__(self):
        return f"{self.flow} - {self.process_name}"
