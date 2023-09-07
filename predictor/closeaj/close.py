"""
判断密接
输入：
    find_inseparable_time发现感染者的时间
    numbers_list各个节点的在当时刻的状态列表
    num_people管控人数
    retroactive_time追溯时长
输出：
    密接者列表；
"""

import numpy as np
import random
import pandas as pd


def Close(find_inseparable_time, numbers_list, num_people, retroactive_time):
    # 在t=215时刻随机选取感染节点，找到其每个时刻的密接节点
    df = pd.read_csv('data/graph_1h_1.5m_n2000(random).txt', sep='\t', header=None)
    df.columns = ['T', 'node1', 'node2']
    # print(df)

    # print(numbers_list)

    result_dict = {}
    end_time = find_inseparable_time - retroactive_time
    for t in range(find_inseparable_time, end_time, -1):
        for node in numbers_list:
            df_new = df[df['T'] == t]
            # print(df_new)
            df_1 = df_new[(df_new['node1'] == node) | (df_new['node2'] == node)]
            # print(df_1)
            # 处理第二列中不是 37 的数字
            column2_values = df_1.loc[df_1['node1'] != node, 'node1']
            for value in column2_values:
                result_dict[value] = result_dict.get(value, 0) + 1

            # 处理第三列中不是 37 的数字
            column3_values = df_1.loc[df_1['node2'] != node, 'node2']
            for value in column3_values:
                result_dict[value] = result_dict.get(value, 0) + 1

        # numbers_list = list(result_dict.keys())
        # numbers_list = list(set(numbers_list))
        # 打印结果字典

    # 使用 sorted 函数对字典的 value 进行排序，设置 reverse=True 以降序排列
    sorted_dict = sorted(result_dict.items(), key=lambda item: item[1], reverse=True)
    # 获取前十个 key 值
    top_ten_keys = [item[0] for item in sorted_dict[:num_people]]
    # 打印结果
    print('时间间隔为' + str(retroactive_time) + '时刻排名前' + str(num_people) + '的密接节点', top_ten_keys)
    return top_ten_keys
