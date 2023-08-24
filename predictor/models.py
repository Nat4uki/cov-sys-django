from django.db import models


# Create your models here.
#
class NetArgument:
    num_people = 10 #管控人数
    retroactive_time = 12 # 追溯时间
    controls_time = 1 # 经过多久管控
    status = 0


class CovPeopleForm(models.Model):
    targetId = models.AutoField(null=False, blank=False, auto_created=True, primary_key=True,)
    targetName = models.CharField(max_length=10, default="NULL", null=True)
    targetAge = models.IntegerField(default="NULL", null=True)
    targetSex = models.CharField(max_length=3, default="NULL", null=True)
    occupationType = models.CharField(max_length=25, default="NULL", null=True)

    class Meta:
        db_table = 'cov_person_form'


class CovPersonGis(models.Model):
    indexId = models.AutoField(primary_key=True, auto_created=True, null=False, blank=False)
    personKey = models.IntegerField(default=0, null=False, blank=False,)
    indexTime = models.DateTimeField(default=None, null=True)
    lng = models.DecimalField(default=None, max_digits=9, decimal_places=6, null=True)
    lat = models.DecimalField(default=None, max_digits=9, decimal_places=6, null=True)
    personStatus = models.IntegerField(default=None, null=True)

    class Meta:
        db_table = 'cov_person_gis'


class CovPersonStatues(models.Model):
    personKey = models.IntegerField(null=False, blank=False, default=0, primary_key=True)
    refreshTime = models.DateTimeField(default='NULL', null=True)
    personStatues = models.IntegerField(default='NULL', null=True)

    class Meta:
        db_table = 'cov_person_statues'


class CovSumSeir(models.Model):
    date = models.DateTimeField(null=False, blank=False, default="2000-01-01 00:00:00", primary_key=True)
    sType = models.IntegerField(default='NULL', null=True)
    eType = models.IntegerField(default='NULL', null=True)
    iType = models.IntegerField(default='NULL', null=True)
    rType = models.IntegerField(default='NULL', null=True)
    cType = models.IntegerField(default='NULL', null=True)
    class Meta:
        db_table = 'cov_sum_seir'
