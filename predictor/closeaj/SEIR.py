"""
传播代码
输入：
    adjacency_list      时序网络
    times               发现感染者的时刻（这里设置为120h）
    num_people          管控人数
    retroactive_time    追溯时长
    controls_time       经过多久管控
    probability         在times时刻下能够管控的感染者的概率（这里设置为了0.3）；
输出：
    各个时刻各个人的状态、各个时刻各个状态的人数；
"""

import numpy as np
import random
import predictor.closeaj.close as close


def Statistical_node_state(node_stata_list):
    # 重新统计各个节点状态
    Susceptibility_node_list = []  # 存放易感节点
    latent_node_list = []  # 存放潜伏节点
    Infect_node_list = []  # 存放感染节点
    recover_node_list = []  # 存放恢复节点
    controls_node_list = []  # 存放管控节点个数

    for i in range(len(node_stata_list)):

        if node_stata_list[i] == 1:
            Susceptibility_node_list.append(i)
        elif node_stata_list[i] == 2:
            latent_node_list.append(i)
        elif node_stata_list[i] == 3:
            Infect_node_list.append(i)
        elif node_stata_list[i] == 4:
            recover_node_list.append(i)
        # elif node_stata_list[i] == 5:
        #     controls_node_list.append(i)

        elif node_stata_list[i] == 0:
            Infect_node_list.append(i)
    return Susceptibility_node_list, latent_node_list, Infect_node_list, recover_node_list


def tem_hyper_SI(adjacency_list, times, num_people, retroactive_time, controls_time, probability):
    # beta1:易感->潜伏， beta2:免疫->潜伏， gamma：潜伏->感染， alpha：感染->免疫
    # 0.种子节点 1.易感 2.潜伏 3.感染 4.免疫 5.管控
    # num_people:管控人数 retroactive_time:追溯时间 controls_time:管控时间
    beta1 = 0.9
    beta2 = 0.005
    gamma = 0.1
    alpha = 0.01

    # find_inseparable_time = input("输入开始找寻密接节点的时间:")
    # print(find_inseparable_time)
    find_inseparable_time = 120
    node_list_all = []
    for m in range(len(adjacency_list)):
        for n in range(len(adjacency_list[m])):
            for o in range(len(adjacency_list[m][n])):
                if adjacency_list[m][n][o] not in node_list_all:
                    node_list_all.append(adjacency_list[m][n][o])
    node_list_all = sorted(node_list_all)
    node = max(node_list_all) + 1
    # print(node)

    for T in range(times):  # 循环次数
        all_Susceptibility_node_num_matrix = []  # 统计当前循环次易感节
        all_latent_node_num_matrix = []  # 统计当前循环潜伏节点数
        all_Infect_node_num_matrix = []  # 统计当前循环感染节点数
        all_recover_node_num_matrix = []  # 统计当前循免疫节点数

        # for n in range(len(node_list_all)): # 遍历每个初始节点为种子节点
        for n in range(5, 6):
            # print(n)
            Susceptibility_node_num_list = []  # 存放易感节点个数
            latent_node_num_list = []  # 存放潜伏节点个数
            Infect_node_num_list = []  # 存放感染节点个数
            recover_node_num_list = []  # 存放免疫节点个数

            Susceptibility_node_list = []  # 存放易感节点
            latent_node_list = []  # 存放潜伏节点
            Infect_node_list = []  # 存放感染节点
            recover_node_list = []  # 存放恢复节点
            controls_node_list = []  # 存放管控节点个数

            node_stata_list = [1] * node  # 存放所有节点的状态（初始全为易感节点）
            seed_node = n  # 选取种子节点
            node_stata_list[seed_node] = 0  # 种子节点状态置为0（且一直为0）
            Infect_node_list.append(seed_node)
            # matrix_node_stata = []
            for t in range(len(adjacency_list)):  # 遍历每个时刻
                np.save('data/' + str(num_people) + '_' + str(retroactive_time) + '_' + str(
                    controls_time) + '/state_time/node_state_time' + str(t) + '.npy', node_stata_list)

                if len(latent_node_list) != 0:  # 将潜伏节点转化为感染节点
                    Infect_node = np.random.choice(latent_node_list, size=int(len(latent_node_list) * gamma) + 1,
                                                   replace=False)
                    for m in Infect_node:
                        node_stata_list[m] = 3

                if len(Infect_node_list) != 0:  # 将感染节点转化为免疫节点
                    recover_node = np.random.choice(Infect_node_list, size=int(len(Infect_node_list) * alpha),
                                                    replace=False)
                    for m in recover_node:
                        if node_stata_list[m] != 0:
                            node_stata_list[m] = 4

                # 重新统计各个节点状态
                node_stata_list[seed_node] = 0
                Susceptibility_node_list, latent_node_list, Infect_node_list, recover_node_list = Statistical_node_state(
                    node_stata_list)

                # # 开始传播
                if t != find_inseparable_time and t != find_inseparable_time + controls_time:
                    for i in range(len(adjacency_list[t])):  # 遍历t时刻的超边
                        for I_node in Infect_node_list:  # 遍历每个感染节点
                            if I_node in adjacency_list[t][i]:  # 如果感染节点在这条超边内
                                for j in range(len(adjacency_list[t][i])):  # 遍历t时刻i超边中的节点j
                                    r = random.random()
                                    # 若为易感节点
                                    # print(adjacency_list[t][i][j])
                                    if node_stata_list[adjacency_list[t][i][j]] == 1:
                                        # print('okk1')
                                        if r <= beta1:
                                            # print('okk2')
                                            node_stata_list[adjacency_list[t][i][j]] = 2
                                    # 若免疫节点
                                    elif node_stata_list[adjacency_list[t][i][j]] == 4:
                                        if r <= beta2:
                                            node_stata_list[adjacency_list[t][i][j]] = 2
                elif t == find_inseparable_time:
                    Find_Infect_node_list = random.sample(Infect_node_list, int(len(Infect_node_list) * probability))
                    controls_node_list = close.Close(find_inseparable_time, Find_Infect_node_list, num_people,
                                                     retroactive_time)
                    for _ in Find_Infect_node_list:
                        node_stata_list[_] = 5
                    # 重新统计各个节点状态
                    node_stata_list[seed_node] = 0
                    Susceptibility_node_list, latent_node_list, Infect_node_list, recover_node_list = Statistical_node_state(
                        node_stata_list)
                    for i in range(len(adjacency_list[t])):  # 遍历t时刻的超边
                        for I_node in Infect_node_list:  # 遍历每个感染节点
                            if I_node in adjacency_list[t][i]:  # 如果感染节点在这条超边内
                                for j in range(len(adjacency_list[t][i])):  # 遍历t时刻i超边中的节点j
                                    r = random.random()
                                    # 若为易感节点
                                    if node_stata_list[adjacency_list[t][i][j]] == 1:
                                        if r <= beta1:
                                            node_stata_list[adjacency_list[t][i][j]] = 2
                                    # 若免疫节点
                                    elif node_stata_list[adjacency_list[t][i][j]] == 4:
                                        if r <= beta2:
                                            node_stata_list[adjacency_list[t][i][j]] = 2
                elif t == find_inseparable_time + controls_time:
                    print(controls_node_list)
                    for _ in controls_node_list:
                        node_stata_list[_] = 5
                    Susceptibility_node_list, latent_node_list, Infect_node_list, recover_node_list = Statistical_node_state(
                        node_stata_list)
                    for i in range(len(adjacency_list[t])):  # 遍历t时刻的超边
                        for I_node in Infect_node_list:  # 遍历每个感染节点
                            if I_node in adjacency_list[t][i]:  # 如果感染节点在这条超边内
                                for j in range(len(adjacency_list[t][i])):  # 遍历t时刻i超边中的节点j
                                    r = random.random()
                                    # 若为易感节点
                                    if node_stata_list[adjacency_list[t][i][j]] == 1:
                                        if r <= beta1:
                                            node_stata_list[adjacency_list[t][i][j]] = 2
                                    # 若免疫节点
                                    elif node_stata_list[adjacency_list[t][i][j]] == 4:
                                        if r <= beta2:
                                            node_stata_list[adjacency_list[t][i][j]] = 2
                node_stata_list[seed_node] = 0
                Susceptibility_node_list, latent_node_list, Infect_node_list, recover_node_list = Statistical_node_state(
                    node_stata_list)
                # 将每个时刻，各个状态的节点个数存入列表
                Susceptibility_node_num_list.append(len(Susceptibility_node_list))
                latent_node_num_list.append(len(latent_node_list))
                Infect_node_num_list.append(len(Infect_node_list))
                recover_node_num_list.append(len(recover_node_list))
                # print(Infect_node_list)

                # matrix_node_stata.append(node_stata_list)
            # 将每个节点为种子节点的传播结果存入矩阵

            all_Susceptibility_node_num_matrix.append(Susceptibility_node_num_list)
            all_latent_node_num_matrix.append(latent_node_num_list)
            all_Infect_node_num_matrix.append(Infect_node_num_list)
            all_recover_node_num_matrix.append(recover_node_num_list)

        # 计算平均值
        avg_all_Susceptibility_node_num_matrix = np.mean(all_Susceptibility_node_num_matrix, axis=0)
        avg_all_latent_node_num_matrix = np.mean(all_latent_node_num_matrix, axis=0)
        avg_all_Infect_node_num_matrix = np.mean(all_Infect_node_num_matrix, axis=0)
        avg_all_recover_node_num_matrix = np.mean(all_recover_node_num_matrix, axis=0)

        return avg_all_Susceptibility_node_num_matrix, avg_all_latent_node_num_matrix, avg_all_Infect_node_num_matrix, avg_all_recover_node_num_matrix
