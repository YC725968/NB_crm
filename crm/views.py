from django.shortcuts import render,redirect,reverse,HttpResponse
from django.contrib import auth
from crm.forms import RegForm,CustomerForm
from crm import models
from django.views import View
from django.db.models import Q
from utils.pager import PageInfo

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
# def customer_list(request):
#     if request.path_info == reverse('customer_list'):
#         all_customer = models.Customer.objects.filter(consultant__isnull=True)
#     else:
#         all_customer = models.Customer.objects.filter(consultant=request.user)
#     page = Pagination(request.GET.get('page'), request.path_info, all_customer.count())
#     return render(request, 'crm/customer_list.html',
#                   {"all_customer": all_customer[page.start:page.end], 'html_str': page.show_li})


#展示客户列表cbv
class CustomerList(View):
    def get(self,request):
        # print(request.path_info)
        # print(request.user)
        q = self.get_seach_contion(['name','qq'])
        if request.path_info == reverse('customer_list'):
            all_customer = models.Customer.objects.filter(q,consultant__isnull=True)
        else:
            all_customer = models.Customer.objects.filter(q,consultant=request.user)
            # print(request.user)
        page = PageInfo(request.GET.get('page'),all_customer.count(),request.path_info,5)
        return render(request, 'crm/customer_list.html',
                      {"all_customer": all_customer[page.start:page.end], 'html_str': page.pager})
    def post(self,request):
        #处理post提交的action数据
        # print(request.POST)
        action = request.POST.get('action')
        print(action)
        if not hasattr(self,action):
            return HttpResponse('非法操作')
        ret = getattr(self,action)()#获取action方法，如果存在加（）执行
        if ret:
            return ret
        return self.get(request)#post完之后在调用get返回customer_list
    def multi_apply(self):
        #公户变私户
        ids = self.request.POST.getlist('id')
        #方法1
        # models.Customer.objects.filter(id__in=ids).update(consultant =self.request.user)
        self.request.user.customers.add(*models.Customer.objects.filter(id__in=ids))
        # return HttpResponse('申请成功')
    def multi_pub(self):
        #私户变公户
        ids = self.request.POST.getlist('id')
        # 方法1
        # models.Customer.objects.filter(id__in=ids).update(consultant =None)
        #方法二
        self.request.user.customers.remove(*models.Customer.objects.filter(id__in=ids))
    def get_seach_contion(self,query_list):
        query = self.request.GET.get('query','')
        q= Q()
        q.connector = 'OR'
        for i in query_list:
            q.children.append(Q(('{}__contains'.format(i),query)))
        return q
        #Q( Q(qq_contains =query)| Q(name_contains =query))


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
            return redirect(reverse('customer_list'))
    return render(request,'crm/customer.html',{'form_obj':form_obj,'nid':nid})

# users = [{'name':'yc{}'.format(i)} for i in range(1,302)]
# def user_list(request):
#     page =PageInfo(request.GET.get('page','1'),len(users),request.path_info,5,5)
#     return render(request,'user_list.html',{'data':users[page.start:page.end],'html_str':page.pager})