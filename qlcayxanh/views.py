from django.contrib import auth
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django import forms
from django.views.generic import TemplateView, FormView
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from django.contrib.auth.views import LoginView, LogoutView

from qlcayxanh.filters import treeFilter
from qlcayxanh.forms import *
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import logout
import xlwt
from datetime import datetime
from django.db.models import Q, Count
# Create your views here.
from qlcayxanh.models import ranh_gioi, cayxanh, duonggiaothong,loaicay
from django.db.models import Sum,Value as V
from django.db.models.functions import Concat
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.contrib.gis.serializers.geojson import Serializer
from datetime import date
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
#----------------

#---------------
# Đăng nhập
class loginPageView(LoginView):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'login/login.html')
        else:
            user = User.objects.filter(id=request.user.pk)
            if user[0].is_superuser:
                return redirect('/index/')
            else:
                return redirect('/index/')
    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.filter(username=username)
            if user:
                if user[0].is_active:
                    user_auth = authenticate(username=username, password=password)
                    if user_auth:
                        login(request, user_auth)
                        if user[0].is_superuser:
                            return redirect('/index/')
                        else:
                            return redirect('/index/')
                    else:
                        return render(request, 'login/login.html', {
                            'alert': 'Bạn hãy nhập đúng Tên tài khoản và mật khẩu. (Có phân biệt chữ hoa, thường)'})
                else:
                    return render(request, 'login/login.html',
                                  {'alert': 'Tài khoản của bạn chưa được kích hoạt. Vui lòng liên hệ với Quản trị.'})
            else:
                return render(request, 'login/login.html',
                              {'alert': 'Tài khoản của bạn chưa có. Liên hệ với Quản trị để tạo tài khoản.'})


# --------------------------
# logout
class Logout(View):
    @login_required(login_url='login/')
    def logout(self, request):
        auth.logout(request)
        return redirect('/login/')
#----------------------------------------



class index(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'




# quản lý người sử dụng
def listuser(request):
    listusers = User.objects.all()
    expenses = User.objects.all()
    query = request.GET.get('q')
    if query:
        expenses = User.objects.annotate(
                        full_name=Concat('last_name', V(' '), 'first_name')
                    ).filter(
            Q(username__icontains=query)| Q(first_name__icontains=query)| Q(last_name__icontains=query)| Q(full_name__icontains=query)
        ).distinct()
    paginator = Paginator(expenses, 10)  # Phân trang với pagination
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    return render(request, 'home/qlusers/users.html', {"listusers": listusers,'page_obj':page_obj})

#-----------------------------

#---------------------------------
    
# Tạo tài khoản
#---------------------------------
def register(request):
    firstname=''
    lastname=''
    emailvalue=''
    uservalue=''
    passwordvalue1=''
    passwordvalue2=''
    is_staffvalue = ''
    is_activevalue = ''
    is_superuservalue = ''
    listusers = User.objects.all()
    form= RegistrationForm(request.POST or None)
    if form.is_valid():
        fs= form.save(commit=False)
        firstname= form.cleaned_data.get("first_name")
        lastname= form.cleaned_data.get("last_name")
        emailvalue= form.cleaned_data.get("email")
        uservalue= form.cleaned_data.get("username")
        passwordvalue1= form.cleaned_data.get("password1")
        passwordvalue2= form.cleaned_data.get("password2")
        is_staffvalue = form.cleaned_data.get("is_staff")
        is_activevalue = form.cleaned_data.get("is_active")
        is_superuservalue = form.cleaned_data.get("is_superuser")
        if passwordvalue1 == passwordvalue2:
            user= User.objects.create_user(username=uservalue, password= passwordvalue1, email=emailvalue,first_name=firstname,last_name=lastname,is_staff=is_staffvalue,  is_active=is_activevalue,is_superuser=is_superuservalue  )
            user.save()
            return redirect('/index/list_users')
            context= {'form': form,'listusers': listusers}
            return render(request, 'home/qlusers/users.html', context)
        else:
            context= {'form': form, 'error':'The passwords that you provided don\'t match'}
            return render(request, 'home/qlusers/add.html', context)
    else:
        context= {'form': form,'listusers': listusers}
        return render(request, 'home/qlusers/add.html', context)

# Chỉnh sửa tài khoản
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thành công!')
            return redirect(reverse('qlcayxanh:users'))

    context = {'form': form, 'user': user}
    return render(request, 'home/qlusers/edit.html', context)

# Xóa tài khoản
def deleteUserpopup(request, pk):
    user = User.objects.get(id=pk)
    listusers = User.objects.all()
    if request.method == "POST":
        user.delete()
        messages.success(request, 'Xóa thành công!')
        return redirect(reverse('qlcayxanh:users'))
        context = {'item': user,'listusers':listusers}
        return render(request, 'home/qlusers/users.html', context)
    context = {'item': user}
    return render(request, 'home/qlusers/users.html', context)

# Thay đổi mật khẩu người đăng nhập
def change_password(request):
    if request.method == 'POST':
        form = Password_ChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Mật khẩu của bạn đã được cập nhật!')
            return redirect(reverse('qlcayxanh:change_password'))
        else:
            messages.error(request, 'Vui lòng sửa lỗi bên dưới!')
    else:
        form = Password_ChangeForm(request.user)
    return render(request, 'home/qlusers/change_pass.html', {
        'form': form
    })

# quản lý dữ liệu

# quản lý ranh giới
def list_ranhgioi(request):
    listboundarys = ranh_gioi.objects.all()
    expenses = ranh_gioi.objects.all()
    query = request.GET.get('q')
    if query:
        expenses = ranh_gioi.objects.filter(
            Q(ma_ranh_gioi__icontains=query) | Q(ten_ranh_gioi__icontains=query)
        ).distinct()
    paginator = Paginator(expenses, 5)  # Phân trang với pagination
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    return render(request, 'home/qldatas/qlboundarys/boundarys.html', {"listboundarys": listboundarys,'page_obj':page_obj})

# Tạo ranh giới
def create_boundary(request):
    form = ranhgioiForm()
    if request.method == 'POST':
        form = ranhgioiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('qlcayxanh:boundarys'))

    context = {'form': form}
    return render(request, 'home/qldatas/qlboundarys/add.html', context)

# Chỉnh sửa ranh giới
def update_boundary(request, pk):
    boun = ranh_gioi.objects.get(ma_ranh_gioi=pk)
    form = ranhgioiForm(instance=boun)
    if request.method == 'POST':
        form = ranhgioiForm(request.POST, instance=boun)      
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thành công!')
            return redirect(reverse('qlcayxanh:boundarys'))

    context = {'form': form,'boun':boun}
    return render(request, 'home/qldatas/qlboundarys/edit.html', context)
# Xóa ranh giới
def delete_boundarypopup(request, pk):
    boundary = ranh_gioi.objects.get(ma_ranh_gioi=pk)
    listboundarys = ranh_gioi.objects.all()
    if request.method == "POST":
        boundary.delete()
        messages.success(request, 'Xóa thành công!')
        return redirect(reverse('qlcayxanh:boundarys'))
    context = {'item': boundary}
    return render(request, 'home/qldatas/qlboundarys/boundarys.html', context)
def inf_boun(request, pk):
    boun = ranh_gioi.objects.get(ma_ranh_gioi=pk)
    form = ranhgioiForm(instance=boun)
    if request.method == 'POST':
        form = ranhgioiForm(request.POST, instance=boun)      
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thành công!')
            return redirect(reverse('qlcayxanh:boundarys'))

    context = {'form': form,'boun':boun}
    return render(request, 'home/qldatas/qlboundarys/infboun.html', context)

# quản lý cây
# danh sách cây
def listtrees(request):
    listtrees = cayxanh.objects.all()
    expenses = cayxanh.objects.all()
    query = request.GET.get('q')
    if query:
        expenses = cayxanh.objects.filter(
            Q(ma_cay__icontains=query) | Q(ten_cay__icontains=query)
        ).distinct()
    paginator = Paginator(expenses, 5)  # Phân trang với pagination
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    return render(request, 'home/qldatas/qltrees/trees.html', {"listtrees": listtrees,'page_obj':page_obj})

# Tạo cây
def addcayxanh(request):
    form = cayxanhForm()
    listtrees = cayxanh.objects.all()
    duongs = duonggiaothong.objects.all()
    loais = loaicay.objects.all()
    if request.method == 'POST':
        form = cayxanhForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('qlcayxanh:listtrees'))
    context = {'form':form,'duongs': duongs,'listtrees':listtrees,'loais':loais}
    return render(request, 'home/qldatas/qltrees/addtrees.html', context)
# Chỉnh sửa cây
def update_trees(request, pk):
    tree = cayxanh.objects.get(ma_cay=pk)
    listtrees = cayxanh.objects.all()
    duongs = duonggiaothong.objects.all()
    loais = loaicay.objects.all()
    form = cayxanhForm(instance=tree)
    if request.method == 'POST':
        form = cayxanhForm(request.POST, instance=tree)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thành công!')
            return redirect(reverse('qlcayxanh:listtrees'))

    context = {'form': form,'tree':tree,'duongs': duongs,'listtrees':listtrees,'loais':loais}
    return render(request, 'home/qldatas/qltrees/edit.html', context)
# Xóa cây
def delete_trees(request, pk):
    tree = cayxanh.objects.get(ma_cay=pk)
    listtrees = cayxanh.objects.all()
    if request.method == "POST":
        tree.delete()
        messages.success(request, 'Xóa thành công!')
        return redirect(reverse('qlcayxanh:listtrees'))
    context = {'item': tree}
    return render(request, 'home/qldatas/qltrees/trees.html', context)
def inf_tree(request, pk):
    tree = cayxanh.objects.get(ma_cay=pk)
    listtrees = cayxanh.objects.all()
    duongs = duonggiaothong.objects.all()
    loais = loaicay.objects.all()
    form = cayxanhForm(instance=tree)
    context = {'form': form, 'tree': tree, 'duongs': duongs, 'listtrees': listtrees, 'loais': loais}
    return render(request, 'home/qldatas/qltrees/inftree.html', context)
#quản lý đường giao thôgn
# Tạo đường giao thông
def addstreets(request):
    form = streetsForm()
    ranhgiois = ranh_gioi.objects.all()
    duongs = duonggiaothong.objects.all()
    if request.method == 'POST':
        form = streetsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('qlcayxanh:liststreets'))
    context = {'form':form,'duongs': duongs,'ranhgiois':ranhgiois }
    return render(request, 'home/qldatas/qlstreets/addstreets.html',context)

# Chỉnh sửa đường giao thông
def update_streets(request, pk):
    street = duonggiaothong.objects.get(ma_duong=pk)
    form = streetsForm(instance=street)
    if request.method == 'POST':
        form = streetsForm(request.POST, instance=street)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thành công!')
            return redirect(reverse('qlcayxanh:liststreets'))

    context = {'form': form,'street':street}
    return render(request, 'home/qldatas/qlstreets/edit.html', context)
# XÓa đường giao thông
def delete_streets(request, pk):
    street = duonggiaothong.objects.get(ma_duong=pk)
    liststreet = duonggiaothong.objects.all()
    if request.method == "POST":
        street.delete()
        messages.success(request, 'Xóa thành công!')
        return redirect(reverse('qlcayxanh:liststreets'))
    context = {'item': street}
    return render(request, 'home/qldatas/qlstreets/streets.html', context)
def inf_street(request, pk):
    street = duonggiaothong.objects.get(ma_duong=pk)
    form = streetsForm(instance=street)
    if request.method == 'POST':
        form = streetsForm(request.POST, instance=street)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thành công!')
            return redirect(reverse('qlcayxanh:liststreets'))

    context = {'form': form,'street':street}
    return render(request, 'home/qldatas/qlstreets/infstreet.html', context)
# danh sách đường giao thông
def liststreets(request):
    liststreet = duonggiaothong.objects.all()
    expenses = duonggiaothong.objects.all()
    query = request.GET.get('q')
    if query:
        expenses = duonggiaothong.objects.filter(
            Q(ma_duong__icontains=query) | Q(ten_duong__icontains=query)
        ).distinct()
    paginator = Paginator(expenses, 5)  # Phân trang với pagination
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    return render(request,'home/qldatas/qlstreets/streets.html',{"liststreet":liststreet,'page_obj':page_obj})
#-----------------------#
# Quản lý nhân viên
# danh sách nhân viên
def lists_staff(request):
    lists_staffs = nhanvien.objects.all()
    expenses = nhanvien.objects.all()
    query = request.GET.get('q')
    if query:
        expenses = nhanvien.objects.filter(
            Q(hoten__icontains=query) | Q(ma_nhan_vien__icontains=query)
        ).distinct()
    paginator = Paginator(expenses, 10)#Phân trang với pagination
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    return render(request,'home/qlstaffs/staffs.html',{"lists_staffs":lists_staffs,'page_obj': page_obj})
# Thêm nhân viên
def addstaffs(request):
    form = nhanvienForm()
    nhanviens = nhanvien.objects.all()
    if request.method == 'POST':
        form = nhanvienForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('qlcayxanh:lists_staff'))
    context = {'form':form,'nhanviens': nhanviens }
    return render(request, 'home/qlstaffs/addstaff.html',context)
# Chỉnh sửa nhân viên
def update_staffs(request, pk):
    staff = nhanvien.objects.get(ma_nhan_vien=pk)
    form = nhanvienForm(instance=staff)
    if request.method == 'POST':
        form = nhanvienForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thành công!')
            return redirect(reverse('qlcayxanh:lists_staff'))

    context = {'form': form,'staff':staff}
    return render(request, 'home/qlstaffs/edit.html', context)
# XÓa nhân viên
def delete_staffs(request, pk):
    staff = nhanvien.objects.get(ma_nhan_vien=pk)
    lists_staffs = nhanvien.objects.all()
    if request.method == "POST":
        staff.delete()
        messages.success(request, 'Xóa thành công!')
        return redirect(reverse('qlcayxanh:lists_staff'))
    context = {'item': staff,'lists_staffs':lists_staffs}
    return render(request, 'home/qlstaffs/staffs.html', context)
# Chăm sóc cây
# Quản lý chăm sóc cây
# danh sách chăm sóc cây

# thêm chăm sóc cây
def addtcotrees(request):
    form = chamsoccayForm()
    trees = cayxanh.objects.all()
    nhanviens = nhanvien.objects.all()
    tcotrees = chamsoccay.objects.all()
    if request.method == 'POST':
        form = chamsoccayForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('qlcayxanh:lists_tcotrees'))
    context = {'form':form,'tcotrees':tcotrees,'trees': trees,'nhanviens':nhanviens }
    return render(request, 'home/qltcotrees/addtcotrees.html',context)
# Chỉnh sửa chăm sóc cây
def update_tcotrees(request, pk):
    trees =cayxanh.objects.all()
    tcotree = chamsoccay.objects.get(id=pk)
    form = chamsoccayForm(instance=tcotree)
    if request.method == 'POST':
        form = chamsoccayForm(request.POST, instance=tcotree)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thành công!')
            return redirect(reverse('qlcayxanh:lists_tcotrees'))
    context = {'form': form,'tcotree':tcotree,'trees': trees,}
    return render(request, 'home/qltcotrees/edit.html', context)
# XÓa chăm sóc cây
def delete_tcotrees(request, pk):
    tcotree = chamsoccay.objects.get(id=pk)
    lists_tcotrees = chamsoccay.objects.all()
    if request.method == "POST":
        tcotree.delete()
        messages.success(request, 'Xóa thành công!')
        return redirect(reverse('qlcayxanh:lists_tcotrees'))
    context = {'item': tcotree,'lists_tcotrees':lists_tcotrees}
    return render(request, 'home/qltcotrees/tcotrees.html', context)
def inftco_trees(request, pk):
    tree = cayxanh.objects.get(ma_cay=pk)
    listtrees = cayxanh.objects.all()
    duongs = duonggiaothong.objects.all()
    loais = loaicay.objects.all()
    form = cayxanhForm(instance=tree)
    context = {'form': form, 'tree': tree, 'duongs': duongs, 'listtrees': listtrees, 'loais': loais}
    return render(request, 'home/qltcotrees/inftree.html', context)

def inftco_staff(request, pk):
    staff = nhanvien.objects.get(ma_nhan_vien=pk)
    liststaff = nhanvien.objects.all()
    form = nhanvienForm(instance=staff)
    context = {'form': form, 'staff': staff, 'listtrees': listtrees}
    return render(request, 'home/qltcotrees/infstaff.html', context)
def lists_tcotrees(request):
    lists_tcotrees = chamsoccay.objects.all()
    expenses = chamsoccay.objects.all()
    query = request.GET.get('q')
    if query:
        expenses = chamsoccay.objects.filter(
          Q(nhanvien_id__hoten__icontains=query)|Q(cayxanh_id__ten_cay__icontains=query)
        ).distinct()
    paginator = Paginator(expenses, 10)  # Phân trang với pagination
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    return render(request,'home/qltcotrees/tcotrees.html',{'page_obj':page_obj,"lists_tcotrees":lists_tcotrees})
# Thống kê
def statis(request):
    lists_tree = cayxanh.objects.all()
    loais = loaicay.objects.all()
    querysets = cayxanh.objects.all()
    user_filter = treeFilter(request.POST, queryset=querysets)
    return render(request, 'home/statistical/statis.html', {'queryset': user_filter,'lists_tree':lists_tree,'loais':loais})


def inf_trees(request, pk):
    tree = cayxanh.objects.get(ma_cay=pk)
    listtrees = cayxanh.objects.all()
    duongs = duonggiaothong.objects.all()
    loais = loaicay.objects.all()
    form = cayxanhForm(instance=tree)
    context = {'form': form, 'tree': tree, 'duongs': duongs, 'listtrees': listtrees, 'loais': loais}
    return render(request, 'home/statistical/inftree.html', context)
# ---------------------------------------------------------
# Loại cây
def typetrees(request):
    listloais = loaicay.objects.all()
    expenses = loaicay.objects.all()
    paginator = Paginator(expenses, 5)  # Phân trang với pagination
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    return render(request, 'home/qldatas/qltrees/typetrees/typetrees.html', {"listloais": listloais,'page_obj':page_obj})
def addtypetrees(request):
    form = loaicayForm()
    listloais = loaicay.objects.all()
    if request.method == 'POST':
        form = loaicayForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('qlcayxanh:typetrees'))
    context = {'form':form,'listloais':listloais}
    return render(request, 'home/qldatas/qltrees/typetrees/addtypetrees.html', context)
def update_typetrees(request, pk):
    loais = loaicay.objects.get(ma_loai_cay=pk)
    form = loaicayForm(instance=loais)
    if request.method == 'POST':
        form = loaicayForm(request.POST, instance=loais)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thành công!')
            return redirect(reverse('qlcayxanh:typetrees'))

    context = {'form': form,'loais':loais}
    return render(request, 'home/qldatas/qltrees/typetrees/edittypetrees.html', context)

def delete_typetreespopup(request, pk):
    loais= loaicay.objects.get(ma_loai_cay=pk)
    listloais = loaicay.objects.all()
    if request.method == "POST":
        loais.delete()
        messages.success(request, 'Xóa thành công!')
        return redirect(reverse('qlcayxanh:typetrees'))
    context = {'item': loaicay}
    return render(request, 'home/qldatas/qltrees/typetrees/typetrees.html', context)
# -------------------------------------------
# Tình trạng cây
def contrees(request):
    listcons = tinhtrangcay.objects.all()
    expenses = tinhtrangcay.objects.all()
    paginator = Paginator(expenses, 5)  # Phân trang với pagination
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    return render(request, 'home/qldatas/qltrees/conditiontree/contrees.html', {"listcons": listcons,'page_obj':page_obj})
def addcon(request):
    form = tinhtrangcayForm()
    listloais = tinhtrangcay.objects.all()
    if request.method == 'POST':
        form = tinhtrangcayForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('qlcayxanh:contrees'))
    context = {'form':form,'listloais':listloais}
    return render(request, 'home/qldatas/qltrees/conditiontree/add.html', context)
def update_con(request, pk):
    loais = tinhtrangcay.objects.get(id=pk)
    form = tinhtrangcayForm(instance=loais)
    if request.method == 'POST':
        form = tinhtrangcayForm(request.POST, instance=loais)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thành công!')
            return redirect(reverse('qlcayxanh:contrees'))

    context = {'form': form,'loais':loais}
    return render(request, 'home/qldatas/qltrees/conditiontree/edit.html', context)

def delete_con(request, pk):
    loais= tinhtrangcay.objects.get(id=pk)
    listloais = tinhtrangcay.objects.all()
    if request.method == "POST":
        loais.delete()
        messages.success(request, 'Xóa thành công!')
        return redirect(reverse('qlcayxanh:contrees'))
    context = {'item': tinhtrangcay}
    return render(request, 'home/qldatas/qltrees/conditiontree/contrees.html', context)
# Tương tấc bản đồ
def show_data(request):
    listtrees = cayxanh.objects.all()
    return render(request, 'map.html', {"listtrees": listtrees})
# lấy dữ liệu cây xanh
def child_tree(request):
    data =  cayxanh.objects.all()
    childstrees = serializers.serialize(format='geojson',queryset=data, 
    use_natural_foreign_keys=True, fields=['pk','ten_cay','chieucao', 'loaicay_id', 'vitri', 'geom','ngaytrong','tinhtrang_id','dacdiem','duong_id'], indent=4)
    return HttpResponse(childstrees,content_type ='json')

# lấy dữ liệu đường giao thông
def child_street(request):
    data =  duonggiaothong.objects.all()
    childstreets = serializers.serialize(format='geojson',queryset=data, 
    use_natural_foreign_keys=True, fields=['pk','ten_duong','ghichu', 'ranh_gioi_id', 'geom'], indent=4)
    return HttpResponse(childstreets,content_type ='json')

# lấy dữ liệu ranh giới
def child_boun(request):
    data =  ranh_gioi.objects.all()
    childbouns = serializers.serialize('geojson',data)
    return HttpResponse(childbouns,content_type ='json')
# #######
def child_da(request,id):
    data =  cayxanh.objects.filter(ma_cay=id)
    childs = serializers.serialize('geojson',data)
    return HttpResponse(childs,content_type ='json')
    
# ####################################################################
def export_pdf(request):
    # Thống kê cây theo loại cây
    # loai = loaicay.objects.annotate(Count('cayxanh'))
    # Creating http response

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename=danh-sach-cay-' + \
                                      str(date.today().strftime('%d-%m-%Y')) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    trees = cayxanh.objects.all()
    cou= cayxanh.objects.all().count()
    list=cayxanh.objects.values('ten_cay', 'loaicay_id__ten_loai_cay').annotate(count=Count('ten_cay'))
    html_string = render_to_string(
        'home/statistical/pdf-output.html', {'trees': trees, 'total': cou,'list':list}
    )
    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response