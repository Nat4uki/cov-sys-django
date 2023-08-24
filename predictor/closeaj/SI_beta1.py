"""
调节参数运行SEIR.py
"""

import numpy as np
import pandas as pd
import predictor.closeaj.SEIR as SEIR


# 读取HT数据 返回一个DF HT数据有四列
def read_data_HT(path):
    data_HT = pd.read_csv(path)
    data_HT.columns = ['timestamp', 'v_s', 't', 'v']
    v_list = []
    for i in data_HT.v:
        v_list.append(eval(i))
    data_HT['v'] = v_list  # 放进DF
    return data_HT


def t_edge_table(df):
    dc = df.groupby('t')['v'].apply(list).to_dict()
    t_edge_list = []
    for i in dc.keys():
        edge = dc[i]
        t_edge_list.append(edge)
    return t_edge_list


def si_beta(times=1, num_people=10, retroactive_time=12, controls_time=1, probability=0.3):
    """
    调用执行SEIR.py
    t_edge_HT           时序网络
    times               发现感染者的时刻（这里设置为120h）
    num_people          管控人数
    retroactive_time    追溯时长
    controls_time       经过多久管控
    probability         在times时刻下能够管控的感染者的概率（这里设置为了0.3）
    """

    path = '1h_1.5m_n2000(random)'  # 时序网络的文件路径
    # H_T_path = './数据/'+path+'/processing_graph_'+path+'.csv'
    H_T_path = 'data/processing_graph_' + path + '.csv'
    H_T_data = read_data_HT(H_T_path)  # 时序超图数
    t_edge_HT = t_edge_table(H_T_data)

    a, b, c, d = SEIR.tem_hyper_SI(t_edge_HT, times, num_people,
                                   retroactive_time, controls_time,
                                   probability)  # 时序超图传播
    path1 = '' + str(num_people) + '_' + str(retroactive_time) + '_' + str(controls_time) + ''
    print(path1)
    # 保存数据
    np.save('data/' + path1 + '/avg_all_Susceptibility_node_num_matrix.npy', a)
    np.save('data/' + path1 + '/avg_all_latent_node_num_matrix.npy', b)
    np.save('data/' + path1 + '/avg_all_Infect_node_num_matrix.npy', c)
    np.save('data/' + path1 + '/avg_all_recover_node_num_matrix.npy', d)
    return 'success'
    # np.save('./数据/'+path+'/'+str(i)+'/node_state_list.npy', e)

# if __name__ == '__main__':
#     for i in range(1, 2):
#         # print('--------------------------------')
#         # print(i)
#         """
#         t_edge_HT           时序网络
#         times               发现感染者的时刻（这里设置为120h）
#         num_people          管控人数
#         retroactive_time    追溯时长
#         controls_time       经过多久管控
#         probability         在times时刻下能够管控的感染者的概率（这里设置为了0.3）；
#         """
#         times = 1
#         probability = 0.3
#         num_people_list = [10, 20, 30]
#         retroactive_time_list = [12, 15, 24]
#         controls_time_list = [1, 12, 24, 48]
#         for num_people in num_people_list:
#             for retroactive_time in retroactive_time_list:
#                 for controls_time in controls_time_list:
#                     path = '1h_1.5m_n2000(random)'
#                     # H_T_path = './数据/'+path+'/processing_graph_'+path+'.csv'
#                     H_T_path = '../data/processing_graph_' + path + '.csv'
#                     H_T_data = read_data_HT(H_T_path)  # 时序超图数
#                     t_edge_HT = t_edge_table(H_T_data)
#                     a, b, c, d = SEIR.tem_hyper_SI(t_edge_HT, times, num_people, retroactive_time, controls_time,
#                                                    probability)  # 时序超图传播
#                     path1 = '' + str(num_people) + '_' + str(retroactive_time) + '_' + str(controls_time) + ''
#                     print(path1)
#                     np.save('../data/' + path1 + '/avg_all_Susceptibility_node_num_matrix.npy', a)
#                     np.save('../data/' + path1 + '/avg_all_latent_node_num_matrix.npy', b)
#                     np.save('../data/' + path1 + '/avg_all_Infect_node_num_matrix.npy', c)
#                     np.save('../data/' + path1 + '/avg_all_recover_node_num_matrix.npy', d)
#                     # np.save('./数据/'+path+'/'+str(i)+'/node_state_list.npy', e)
