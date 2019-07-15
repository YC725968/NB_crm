from django.shortcuts import render,redirect,reverse
from django.contrib import auth
from crm.forms import RegForm,CustomerForm
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
    all_count =all_customer.count()
    # print(all_count)
    page = Pagination(request.GET.get('page'),'/crm/customer_list/',all_count)
    return render(request,'crm/customer_list.html',{'all_customer':all_customer[page.start:page.end],"html_str":page.show_li})

#增加客户
# def add_customer(request):
#     form_obj = CustomerForm()
#     if request.method =="POST":
#         form_obj =CustomerForm(request.POST)
#         #d对数据进行校验
#         if form_obj.is_valid():
#             form_obj.save()
#             return redirect(reverse('customer_list'))
#
#     return  render(request,'crm/add_customer.html',{"form_obj":form_obj})
#
# #编辑客户
# def edit_customer(request,nid):
#     #根据id查出所需要编辑的客户
#     obj = models.Customer.objects.filter(id=nid).first()
#     form_obj = CustomerForm(instance=obj)#实例instance 把对象的内容实例
#     if request.method=="POST":
#         form_obj = CustomerForm(request.POST,instance=obj)
#         if form_obj.is_valid():
#             form_obj.save()
#             return redirect(reverse(customer_list))
#     return render(request,'crm/edit_customer.html',{'form_obj':form_obj})
#新增编辑客户
def customer(request,nid=None):
    obj = models.Customer.objects.filter(id=nid).first()
    form_obj = CustomerForm(instance=obj)#实例instance 把对象的内容实例
    if request.method=="POST":
        form_obj = CustomerForm(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse(customer_list))
    return render(request,'crm/customer.html',{'form_obj':form_obj,'nid':nid})
