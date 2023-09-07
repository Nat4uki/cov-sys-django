import os
from celery import Celery

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoBackend.settings')

# 实例化
app = Celery('djangoBackend')

# namespace='CELERY' 作用是允许你在Django配置文件中对Celery进行配置
# 但所有Celery配置项必须以CELERY开头，防止冲突
app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.ONCE = {
#   'backend': 'celery_once.backends.Redis',
#   'settings': {
#     'url': 'redis://covsys@127.0.0.1:6379/3',
#     'default_timeout': 60 * 60
#   }
# }
app.conf.ONCE = {
  'backend': 'celery_once.backends.Redis',
  'settings': {
    'url': 'redis://:covsys@127.0.0.1:6379/2',
    'default_timeout': 60 * 10
  }
}
# 自动从Django的已注册app中发现任务

