from django.shortcuts import render,redirect
from django.contrib import auth
from crm.forms import RegForm
from crm import models
from utils.pagination import Pagination

def login(request):
    err_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj = auth.authenticate(request, username=username, password=password)
        if obj:
            return redirect('/index/')
        err_msg = '用户名或密码错误'
    return render(request, 'login.html', {'err_msg': err_msg})

# 注册
def reg(request):
    form_obj = RegForm()
    if request.method == "POST":
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            obj = form_obj.save()
            obj.set_password(obj.password)
            obj.save()
            return redirect('/login/')
            #方法一
           #  form_obj.cleaned_data.pop('re_password')
           #  models.UserProfile.objects.create_user(**form_obj.cleaned_data)
           #  return redirect('/login/')
           # #创建新用户

    return render(request,'reg.html',{'form_obj':form_obj})

#展示客户列表
def customer_list(request):
    all_customer = models.Customer.objects.all()
    # all_count =all_customer.count()
    # print(all_count)
    page = Pagination(request,all_customer.count(),'/crm/customer_list/')
    return render(request,'crm/customer_list.html',{'all_customer':all_customer[page.start,page.end],"pigination":page.show_li})



