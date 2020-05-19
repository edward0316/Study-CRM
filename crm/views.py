from django.shortcuts import render, redirect, reverse, HttpResponse
from crm import models
import hashlib
from crm.forms import RegForm, CustomerForm


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        obj = models.UserProfile.objects.filter(username=username, password=md5.hexdigest(), is_active=True).first()
        if obj:
            # 登录成功
            request.session['is_login'] = True
            request.session['user_id'] = obj.pk

            return redirect('crm:index')
        else:
            return render(request, 'login.html', {"error": "Username or Password Wrong"})

    return render(request, 'login.html')


def index(request):
    return render(request, 'index.html')


def reg(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        # Checking the submitted data
        if form_obj.is_valid():
            # Data approved
            # First method to upload data to database
            # models.UserProfile.objects.create(**form_obj.cleaned_data)
            # Second method to upload data to database
            # Only forms created by ModelForm can use this method
            form_obj.save()
            # reverse is not necessary
            # return redirect('login')
            return redirect(reverse('crm:login'))
        print(form_obj.errors)
    return render(request, 'reg.html', {"form_obj": form_obj})


from django.views import View
from django.db.models import Q
from utils.pagelation import Pagination

class CustomerList(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query','')
        q = Q(Q(qq__contains=query)|Q(name__contains=query)|Q(phone__contains=query))
        if request.path_info == reverse('crm:customer_list'):
            all_customer = models.Customer.objects.filter(q,consultant__isnull=True)
            title = "客户列表"
        else:
            all_customer = models.Customer.objects.filter(q,consultant_id=request.session.get("user_id"))
            title = "我的客户"
        #     copy方法进行深拷贝，并且是可编辑的
        page = Pagination(request.GET.get('page',1),all_customer.count(),request.GET.copy(),2)
        return render(request, 'customer_list.html', {"all_customer": all_customer[page.start:page.end],"title":title,"page_html":page.page_html})

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        if not hasattr(self, action):
            return HttpResponse('Illegal action')
        getattr(self,action)()
        return self.get(request, *args, **kwargs)

    def multi_prv(self):
        # 公户转私户
        pk = self.request.POST.getlist('pk')
        # 方法1
        # models.Customer.objects.filter(pk__in=pk).update(consultant = self.request.user_obj)
        # 星号把列表打散
        self.request.user_obj.customers.add(*models.Customer.objects.filter(pk__in=pk))

    def multi_pub(self):
        pk = self.request.POST.getlist('pk')
        # 方法1
        # models.Customer.objects.filter(pk__in=pk).update(consultant = None)
        # 星号把列表打散
        self.request.user_obj.customers.remove(*models.Customer.objects.filter(pk__in=pk))


# def customer_list(request):
#     if request.path_info == reverse('crm:customer_list'):
#         all_customer = models.Customer.objects.filter(consultant__isnull=True)
#     else:
#         all_customer = models.Customer.objects.filter(consultant_id=request.session.get("user_id"))
#     return render(request, 'customer_list.html', {"all_customer": all_customer})


# 模拟用户数据
users = [{"name": "alex-{}".format(i), "pwd": "alexdsb"} for i in range(1, 452)]

from utils.pagelation import Pagination


def user_list(request):
    page = Pagination(request.GET.get('page', 1), len(users))

    return render(request, "user_list.html",
                  {"users": users[page.start:page.end], "total_number": range(page.page_start, page.page_end),
                   "page_html": page.page_html})


def add_customer(request):
    form_obj = CustomerForm()
    if request.method == "POST":
        # form_obj包含提交的数据
        form_obj = CustomerForm(request.POST)
        if form_obj.is_valid():
            #         校验成功
            form_obj.save()
            return redirect(reverse("crm:customer_list"))
    return render(request, "add_customer.html", {"form_obj": form_obj})


def edit_customer(request, pk):
    # 要修改的customer对象
    obj = models.Customer.objects.filter(pk=pk).first()
    # 把对象的数据导入到表单中
    form_obj = CustomerForm(instance=obj)
    if request.method == "POST":
        next = request.GET.get("next")
        form_obj = CustomerForm(data=request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            if next:
                return redirect(next)
            return redirect(reverse("crm:customer_list"))
    return render(request, "edit_customer.html", {"form_obj": form_obj})
