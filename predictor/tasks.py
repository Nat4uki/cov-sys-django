import os

from celery import shared_task
import numpy as np
import shutil

from django.db import connection

from .models import CovPersonGis
from .models import CovPersonStatues
from .models import CovSumSeir
from celery.exceptions import Ignore
from celery_once import QueueOnce


class UpdateTask(object):
    def __init__(self, task):
        self.task = task

    def update_backup(self, num_people, retroactive_time, controls_time):
        path = '' + str(num_people) + '_' + str(retroactive_time) + '_' + str(controls_time) + ''
        print(path)

        update_queries = []  # 待更新列表
        to_update_num = 0  # 待更新条数
        to_update_total = 0
        update_num = 0  # 实际更新的条数

        for times in range(216):
            # 更新执行状态为读取与比较，并返回待更新的条数
            self.task.update_state(state=f'Compare and update on times {times}', meta={'current': times, 'total': 217})
            # 读取新数据
            new_time_data = np.load('data/' + path + '/state_time/node_state_time' + str(times) + '.npy')
            # 读取备份数据
            old_time_data = np.load('data/person_gis/state_time/node_state_time' + str(times) + '.npy')

            # 以personKey为批次，查询变化的状态
            for node in range(1, 2001):
                personKey = 1000000 + node
                indexId = (node - 1) * 216 + times + 1
                # 状态比较
                if not new_time_data[node] == old_time_data[node]:
                    # 查询得到需要更新的记录
                    recode = CovPersonGis.objects.get(indexId=indexId, personKey=personKey)
                    # 设置要更新的数据
                    recode.personStatus = new_time_data[node]
                    # 将记录添加到待更新列表
                    update_queries.append(recode)
                    # 待更新条数添加
                    to_update_num += 1
            # 执行更新，返回更新成功的条数
            # 更新执行状态为更新中
            print(str(times + 1) + " times; to_update_num:" + str(to_update_num))
            update_num += CovPersonGis.objects.bulk_update(update_queries, ['personStatus'])
            to_update_total += to_update_num
            # 更新后重置
            update_queries = []
            to_update_num = 0
            # 最后一次更新最新状态表
            if times == 215:
                self.update_latest_state(new_time_data)
        print("update_num:" + str(update_num))
        print("to_update_total:" + str(to_update_total))
        # 更新统计数据
        self.update_sum_seir()
        # 更新成功执行备份(转移文件）
        if update_num == to_update_total:
            self.task.update_state(state='Update success. Backup data', meta={'current': 217, 'total': 217})
            print("update success")
            # 更新执行状态为备份文件
            # self.task.update_state(state='Update end. Backup file now')
            dlist = os.listdir('data/' + path + '/state_time')
            file_copy_num = 0
            for f in dlist:
                file1 = os.path.join('data/' + path + '/state_time', f)
                file2 = os.path.join('data/person_gis/state_time', f)
                shutil.copyfile(file1, file2)
                file_copy_num += 1
            print("file copy num:" + str(file_copy_num))
        else:
            self.task.update_state(state='Update fail. Please retry', meta={'current': 217, 'total': 217})

    def update_latest_state(self, latest_np):
        self.task.update_state(state='Update latest statues', meta={'current': 217, 'total': 217})
        update_queries = []  # 待更新列表
        for node in range(1, 2001):
            personKey = 1000000 + node
            recode = CovPersonStatues.objects.get(personKey=personKey)
            recode.personStatues = latest_np[node]
            update_queries.append(recode)
        num = CovPersonStatues.objects.bulk_update(update_queries, ['personStatues'])
        # raise Exception
        # num = CovPersonStatues.objects.bulk_update(update_queries, [''])

    def update_sum_seir(self):
        self.task.update_state(state='Update seir', meta={'current': 216, 'total': 217})
        for days in range(1, 10):
            start_time = f"'2022-03-0{days} 00:00:00'"
            start_time_y = f"2022-03-0{days} 00:00:00"
            end_time = f"'2022-03-0{days + 1} 00:00:00'"
            sql_str = f"select personStatus,count(*) " \
                      f"from cov_person_gis " \
                      f"where (personKey,indexTime) " \
                      f"in (SELECT personKey,max(indexTime) as indexTime " \
                      f"from cov_person_gis WHERE indexTime>={start_time} and indexTime<{end_time} " \
                      f"group by personKey) " \
                      f"group by personStatus " \
                      f"order by personStatus"
            with connection.cursor() as cursor:
                recode = CovSumSeir.objects.get(date=start_time_y)
                recode.sType = 0
                recode.eType = 0
                recode.iType = 0
                recode.rType = 0
                recode.cType = 0
                cursor.execute(sql_str)
                result = cursor.fetchall()
                count = 0
                for row in result:
                    count += 1
                    if count == 1:
                        continue
                    elif count == 2:
                        recode.sType = row[1]
                    elif count == 3:
                        recode.eType = row[1]
                    elif count == 4:
                        recode.iType = row[1]
                    elif count == 5:
                        recode.rType = row[1]
                    elif count == 6:
                        recode.cType = row[1]
                recode.save()


@shared_task(base=QueueOnce, bind=True, once={'keys': []})
def async_update(self, num_people, retroactive_time, controls_time):
    t = UpdateTask(self)
    args = (num_people, retroactive_time, controls_time)
    t.update_backup(num_people=num_people, retroactive_time=retroactive_time, controls_time=controls_time)
    self.update_state(state='success', meta={'current': 216, 'total': 216})
    # 用来触发celery_once的解除线程锁
    self.after_return('', None, self.request.id, args, kwargs=None, einfo="")
    raise Ignore()
