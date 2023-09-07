import json
import os
import shutil
import time

from django.db import connection
from django.http import JsonResponse, HttpResponse

from .closeaj.SI_beta1 import si_beta
from .closeaj.drawing import plot

from .models import *
from .tasks import async_update

from celery.result import AsyncResult
from celery_once import AlreadyQueued


# Create your views here.
# 100 normal
# 250 success
# 550 param get fail
# 551 plot fail
# 552 update fail
# 553 predict fail


def predict(request):
    """
    执行密接预测
    :param request: http request
    :return: Json response 执行状态
    """
    print("predict task")

    na = init_param(request)
    print(na.num_people, na.retroactive_time, na.controls_time)

    result = 100
    status = ''
    if na.status:
        try:
            status = si_beta()
        except RuntimeError as e:
            print(e)
            result = 553
        if status == 'success':
            result = 250
    else:
        result = 550
    json_data = {
        "result": result,
    }
    return JsonResponse(json_data)


def plot_spread(request):
    """
    绘制传播图
    :param request: http request
    :return: Json response 包括执行状态与传播图路径地址
    """
    # 获取参数
    print("polt task")
    na = init_param(request)
    img_path = ''
    print(na.num_people, na.retroactive_time, na.controls_time)
    result = 100
    if na.status:
        try:
            img_path = plot(na.num_people, na.retroactive_time, na.controls_time)
        except OSError as e:
            print('runtime error. Maybe not file find' + e)
            img_path = 'error'
        if img_path == 'error':
            result = 551
        else:
            result = 250
    else:
        result = 550

    json_data = {
        'result': result,
        'img_path': img_path,
        "response_obj": request.POST
    }
    return JsonResponse(json_data)


def update_person(request):
    """
    更新人员的状态
    :param request: http request
    :return: Json response 执行状态
    """
    print("update task")
    print(request.POST)
    na = init_param(request)
    print(na.num_people, na.retroactive_time, na.controls_time)
    try:
        result = async_update.apply_async(args=[
            na.num_people, na.retroactive_time, na.controls_time])
        print(result.task_id)
    except AlreadyQueued as e:
        # 触发线程锁
        json_data = {'state': 'ignore',
                     'msg': 'already a task running'
                     }
        return JsonResponse(json_data)

    message = "running"
    json_data = {
        'task_id': result.task_id,
        'state': 'start',
        'msg': message,
        'request_obj': request.POST
    }
    return JsonResponse(json_data)


def init_param(request):
    na = NetArgument()
    na.status = 0
    if request.method == 'POST':
        try:
            na.controls_time = request.POST.get('controls_time')
            na.num_people = request.POST.get('num_people')
            na.retroactive_time = request.POST.get('retroactive_time')
            na.status = 1
        except Exception as e:
            pass
    return na


# 异步操作
# 方法一：delay方法
# task_name.delay(args1, args2, kwargs=value_1, kwargs2=value_2)
# 方法二： apply_async方法，与delay类似，但支持更多参数
# task.apply_async(args=[arg1, arg2], kwargs={key:value, key:value})
def task_listen(request, task_id):
    task_status = AsyncResult(task_id)
    # meta = task_status.meta
    json_data = {
        'state': task_status.status,
        'current': task_status.result['current'],
        'total': task_status.result['total']
    }
    # json_data = {
    #     'state': task_status.state,
    #     'current': task_status.result['current'],
    #     'total': task_status.result['total']
    # }
    return JsonResponse(json_data)


# def task_exec(request):
#     for days in range(1, 10):
#         start_time = f"'2022-03-0{days} 00:00:00'"
#         start_time_y = f"2022-03-0{days} 00:00:00"
#         end_time = f"'2022-03-0{days + 1} 00:00:00'"
#         sql_str = f"select personStatus,count(*) " \
#                   f"from cov_person_gis " \
#                   f"where (personKey,indexTime) " \
#                   f"in (SELECT personKey,max(indexTime) as indexTime " \
#                   f"from cov_person_gis WHERE indexTime>={start_time} and indexTime<{end_time} " \
#                   f"group by personKey) " \
#                   f"group by personStatus " \
#                   f"order by personStatus"
#         with connection.cursor() as cursor:
#             recode = CovSumSeir.objects.get(date=start_time_y)
#             recode.sType = 0
#             recode.eType = 0
#             recode.iType = 0
#             recode.rType = 0
#             recode.cType = 0
#             cursor.execute(sql_str)
#             result = cursor.fetchall()
#             count = 0
#             for row in result:
#                 count += 1
#                 if count == 1:
#                     continue
#                 elif count == 2:
#                     recode.sType = row[1]
#                 elif count == 3:
#                     recode.eType = row[1]
#                 elif count == 4:
#                     recode.iType = row[1]
#                 elif count == 5:
#                     recode.rType = row[1]
#                 elif count == 6:
#                     recode.cType = row[1]
#             recode.save()
#     return HttpResponse("OK")
