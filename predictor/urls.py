from django.urls import path
from .views import *

urlpatterns = {
    path('predict/', predict, name='predict'),
    path('plot/', plot_spread, name='plot'),
    path('update/', update_person, name='update'),
    # path('task_exec/', task_exec, name='task_exec'),
    path('task_listen/<str:task_id>', task_listen, name='task_listen')
}
