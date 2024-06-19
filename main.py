import yaml
# from models import Order


class Order:
    def __init__(self, order_id, due_date, processing_time):
        self.order_id = order_id
        self.due_date = due_date
        self.processing_time = processing_time


class Resource:
    def __init__(self, resource_id, available_time=0):
        self.resource_id = resource_id
        self.available_time = available_time


class Schedule:
    def __init__(self):
        self.scheduled_jobs = []

    def add_job(self, order_id, start_time, end_time, resource_id):
        self.scheduled_jobs.append({
            'order_id': order_id,
            'start_time': start_time,
            'end_time': end_time,
            'resource_id': resource_id
        })


class Scheduler:
    def __init__(self, orders, resources):
        self.orders = orders
        self.resources = resources
        self.schedule = Schedule()

    def fcfs(self):
        for order in self.orders:
            for resource in self.resources:
                if resource.available_time <= order.due_date:
                    start_time = resource.available_time
                    end_time = start_time + order.processing_time
                    self.schedule.add_job(order.order_id, start_time, end_time, resource.resource_id)
                    resource.available_time = end_time
                    break
        return self.schedule

    def spt(self):
        sorted_orders = sorted(self.orders, key=lambda x: x.processing_time)
        for order in sorted_orders:
            for resource in self.resources:
                if resource.available_time <= order.due_date:
                    start_time = resource.available_time
                    end_time = start_time + order.processing_time
                    self.schedule.add_job(order.order_id, start_time, end_time, resource.resource_id)
                    resource.available_time = end_time
                    break
        return self.schedule

    def edd(self):
        sorted_orders = sorted(self.orders, key=lambda x: x.due_date)
        for order in sorted_orders:
            for resource in self.resources:
                if resource.available_time <= order.due_date:
                    start_time = resource.available_time
                    end_time = start_time + order.processing_time
                    self.schedule.add_job(order.order_id, start_time, end_time, resource.resource_id)
                    resource.available_time = end_time
                    break
        return self.schedule


def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


if __name__ == "__main__":
    # 示例数据
    orders = [
        Order(order_id=1, due_date=10, processing_time=3),
        Order(order_id=2, due_date=5, processing_time=2),
        Order(order_id=3, due_date=7, processing_time=1),
    ]

    resources = [
        Resource(resource_id=1),
        Resource(resource_id=2),
    ]

    # 读取配置文件
    config = load_config('config.yaml')

    # 调度器实例
    scheduler = Scheduler(orders, resources)

    # 根据配置文件选择调度算法
    algorithm_choice = config.get("algorithm", "fcfs")

    if algorithm_choice == "fcfs":
        schedule = scheduler.fcfs()
    elif algorithm_choice == "spt":
        schedule = scheduler.spt()
    elif algorithm_choice == "edd":
        schedule = scheduler.edd()
    else:
        raise ValueError("未知的调度算法")

    # 输出排产结果
    for job in schedule.scheduled_jobs:
        print(job)
