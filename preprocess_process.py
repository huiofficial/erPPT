from collections import defaultdict

import pandas as pd

if __name__ == "__main__":

    # 读取 Excel 文件
    file_path = './data/产品加工用时统计进度表.xlsx'
    xls = pd.ExcelFile(file_path)

    # 读取"史密斯"表，设置正确的header行
    df_smith = pd.read_excel(xls, sheet_name='史密斯', header=[1, 2])

    # 填充整个 DataFrame 的缺失值，用前一行数据进行填充
    df_smith = df_smith.ffill()

    # 初始化一个字典来存储产品型号的工序信息
    product_processes = defaultdict(list)

    # 遍历数据框，收集每个产品型号的工序信息
    for _, row in df_smith.iterrows():
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
            product_processes[product].append(process_flow)

    # 示例输出
    example_output = {product: processes for product, processes in list(product_processes.items())[:3]}

    # 打印示例输出
    for product, processes in example_output.items():
        print(f"产品型号: {product}")
        for process_flow in processes:
            print("工序流程:")
            for process in process_flow:
                print(process)
            print("\n")
