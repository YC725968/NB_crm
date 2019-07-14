from django.contrib import admin
from crm import models
admin.site.register(models.Customer)#客户列表
admin.site.register(models.ClassList)#班级列表
admin.site.register(models.Campuses)#校区表
