"""
绘制传播曲线
"""
import os.path

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from numpy import genfromtxt

# path1 = '1h_1.5m_n2000'
# path2 = 'beta1=0.9,beta2=0.005,gamma=0.1,alpha=0.01'


def plot(num_people=10, retroactive_time=12, controls_time=1):
    path = '' + str(num_people) + '_' + str(retroactive_time) + '_' + str(controls_time) + ''
    # print(path)
    # print(os.getcwd())
    # print(os.path.exists('data/' + path + '/avg_all_Susceptibility_node_num_matrix.npy'))
    node = 2000
    x = []
    A = []
    B = []
    C = []
    D = []
    a = np.load('data/' + path + '/avg_all_Susceptibility_node_num_matrix.npy')
    b = np.load('data/' + path + '/avg_all_latent_node_num_matrix.npy')
    c = np.load('data/' + path + '/avg_all_Infect_node_num_matrix.npy')
    d = np.load('data/' + path + '/avg_all_recover_node_num_matrix.npy')
    A.append(a)
    B.append(b)
    C.append(c)
    D.append(d)

    A_avg = np.mean(A, axis=0)
    B_avg = np.mean(B, axis=0)
    C_avg = np.mean(C, axis=0)
    D_avg = np.mean(D, axis=0)

    for i in range(len(A_avg)):
        x.append(i)

    plt.plot(x, A_avg / node, color='#02304a', label='Susceptibility')
    plt.plot(x, B_avg / node, color='#219ebc', label='Exposed')
    plt.plot(x, C_avg / node, color='#feb705', label='Infect')
    plt.plot(x, D_avg / node, color='#fa8600', label='Recover')

    plt.legend()
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    plt.title("%s" % path)
    if not os.path.exists('static/image/' + path):
        os.mkdir('static/image/' + path)
    if os.path.exists('static/image/' + path + '/spread.png'):
        os.remove('static/image/' + path + '/spread.png')
    plt.savefig('static/image/' + path + '/spread.png')
    plt.close()
    if os.path.exists('static/image/' + path + '/spread.png'):
        return 'static/image/' + path + '/spread.png'
    else:
        return 'error'

# num_people_list = [10, 20, 30]
# retroactive_time_list = [12, 15, 24]
# controls_time_list = [1, 12, 24, 48]
# for num_people in num_people_list:
#     for retroactive_time in retroactive_time_list:
#         for controls_time in controls_time_list:
#             path = '' + str(num_people) + '_' + str(retroactive_time) + '_' + str(controls_time) + ''
#             print(path)
#             node = 2000
#             x = []
#             A = []
#             B = []
#             C = []
#             D = []
#             for i in range(1, 2):
#                 # print(1)
#
#                 # a = np.load('./数据/'+path1+'/'+path2+'/'+str(i)+'/avg_all_Susceptibility_node_num_matrix.npy')
#                 # b = np.load('./数据/'+path1+'/'+path2+'/'+str(i)+'/avg_all_latent_node_num_matrix.npy')
#                 # c = np.load('./数据/'+path1+'/'+path2+'/'+str(i)+'/avg_all_Infect_node_num_matrix.npy')
#                 # d = np.load('./数据/'+path1+'/'+path2+'/'+str(i)+'/avg_all_recover_node_num_matrix.npy')
#                 a = np.load('../data/' + path + '/avg_all_Susceptibility_node_num_matrix.npy')
#                 b = np.load('../data/' + path + '/avg_all_latent_node_num_matrix.npy')
#                 c = np.load('../data/' + path + '/avg_all_Infect_node_num_matrix.npy')
#                 d = np.load('../data/' + path + '/avg_all_recover_node_num_matrix.npy')
#                 A.append(a)
#                 B.append(b)
#                 C.append(c)
#                 D.append(d)
#
#             A_avg = np.mean(A, axis=0)
#             B_avg = np.mean(B, axis=0)
#             C_avg = np.mean(C, axis=0)
#             D_avg = np.mean(D, axis=0)
#
#             for i in range(len(A_avg)):
#                 x.append(i)
#
#             # print(A_avg)
#             # print(B_avg)
#             # print(C_avg)
#             # print(D_avg)
#
#             plt.plot(x, A_avg / node, color='#02304a', label='Susceptibility')
#             plt.plot(x, B_avg / node, color='#219ebc', label='Exposed')
#             plt.plot(x, C_avg / node, color='#feb705', label='Infect')
#             plt.plot(x, D_avg / node, color='#fa8600', label='Recover')
#
#             plt.legend()
#             plt.xticks(fontsize=15)
#             plt.yticks(fontsize=15)
#             # plt.title("%s_%s" % (path1,path2))
#             plt.savefig('../data/' + path + '/spread.png')
#             plt.show()
