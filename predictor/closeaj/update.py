"""
输出各个人各个时刻状态的列表存成csv文件
"""

import numpy as np
import pandas as pd


def update_status(num_people=10, retroactive_time=12, controls_time=1):
    path = '' + str(num_people) + '_' + str(retroactive_time) + '_' + str(controls_time) + ''
    print(path)
    for node in range(1, 2001):
        # print(node)
        print(r'data/' + path + '/node_state/node_state' + str(t) + '.csv')
        # 读取原始每个人的state_node文件，从1-2001
        node_data = pd.read_csv(
            r'data/' + path + '/node_state/node_state' + str(t) + '.csv',
            header=None,
            skiprows=1)

        # print(node_data)
        column_to_drop = node_data.columns[3]  # 获取第三列的列名
        print(column_to_drop)
        node_data = node_data.drop(columns=[column_to_drop])
        # print(node_data)

        state_list = []
        for t in range(216):
            time_data = np.load('data/' + path + '/state_time/node_state_time' + str(t) + '.npy')
            state_list.append(time_data[node])

        node_data['3'] = state_list

        # print(node_data)
        # print('------------------------')
        row1 = pd.read_csv(
            r'data/' + path + '/node_state/node_state' + str(t) + '.csv',
            header=None,
            nrows=1)
        row1.to_csv('data/' + path + '/node_state/node_state' + str(node) + '.csv', mode='a',
                    index=False,
                    header=False)
        node_data.to_csv('data/' + path + '/node_state/node_state' + str(node) + '.csv', mode='a',
                         index=False, header=False)
    return 'succeed'

# num_people_list = [10, 20, 30]
# retroactive_time_list = [12, 15, 24]
# controls_time_list = [1, 12, 24, 48]
# for num_people in num_people_list:
#     for retroactive_time in retroactive_time_list:
#         for controls_time in controls_time_list:
#
#             path = '' + str(num_people) + '_' + str(retroactive_time) + '_' + str(controls_time) + ''
#             print(path)
#             for node in range(1, 2001):
#                 # print(node)
#                 node_data = pd.read_csv(
#                     r'/Volumes/T7/代码/传播/code/数据/1h_1.5m_n2000(random)/state/(' + str(node) + ').csv', header=None,
#                     skiprows=1)
#                 # print(node_data)
#                 column_to_drop = node_data.columns[3]  # 获取第三列的列名
#                 node_data = node_data.drop(columns=[column_to_drop])
#                 # print(node_data)
#
#                 state_list = []
#                 for t in range(216):
#                     time_data = np.load('../data/' + path + '/state_time/node_state_time' + str(t) + '.npy')
#                     state_list.append(time_data[node])
#
#                 node_data['3'] = state_list
#
#                 # print(node_data)
#                 # print('------------------------')
#                 row1 = pd.read_csv(
#                     r'/Volumes/T7/代码/传播/code/数据/1h_1.5m_n2000(random)/state/(' + str(node) + ').csv', header=None,
#                     nrows=1)
#                 row1.to_csv('../data/' + path + '/node_state/node_state' + str(node) + '.csv', mode='a', index=False,
#                             header=False)
#                 node_data.to_csv('../data/' + path + '/node_state/node_state' + str(node) + '.csv', mode='a',
#                                  index=False, header=False)
