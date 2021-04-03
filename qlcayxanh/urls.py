from django.urls import path
from qlcayxanh.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url

urlpatterns = [
    # Tài khoản user
    url(r'^list_users/$', listuser, name='users'),
    url(r'^adduser/$', register, name='adduser'),
    path('update_user/<str:pk>/', updateUser, name="update_user"),
    path('delete_Userpopup/<str:pk>/', deleteUserpopup, name="delete_Userpopup"),
    url(r'^change_password/$', change_password, name='change_password'),
    # ranh giới
    url(r'^list_boundarys/$', list_ranhgioi, name='boundarys'),
    url(r'^add_boundarys/$', create_boundary, name='add_boundary'),
    path('update_boundarys/<str:pk>/', update_boundary, name="update_boundary"),
    path('delete_boundarypopup/<str:pk>/', delete_boundarypopup, name="delete_boundarypopup"),
    path('inf_boundarys/<str:pk>/', inf_boun, name="inf_boun"),
    # ĐƯờng giao thông
    url(r'^list_street/$', liststreets, name='liststreets'),
    url(r'^add_street/$', addstreets, name='addstreets'),
    path('update_streets/<str:pk>/', update_streets, name="update_streets"),
    path('delete_streets/<str:pk>/', delete_streets, name="delete_streets"),
    path('inf_streets/<str:pk>/', inf_street, name="inf_street"),
    # popio
    # Cây xanh
    url(r'^list_trees/$', listtrees, name='listtrees'),
    url(r'^add_tree/$', addcayxanh, name='addcayxanh'),
    path('update_trees/<str:pk>/', update_trees, name="update_trees"),
    path('delete_trees/<str:pk>/', delete_trees, name="delete_trees"),
    path('inf_trees/<str:pk>/', inf_tree, name="inf_tree"),
    # Nhân viên
    url(r'^list_staffs/$', lists_staff, name='lists_staff'),
    url(r'^add_staff/$', addstaffs, name='addstaffs'),
    path('update_staffs/<str:pk>/', update_staffs, name="update_staffs"),
    path('delete_staffs/<str:pk>/', delete_staffs, name="delete_staffs"),
    # Thống kê
    url(r'^list_statis/$', statis, name='statis'),
    path('inf_tree/<str:pk>/', inf_trees, name="inf_trees"),

    # chăm sóc cây
    url(r'^list_tcotrees/$', lists_tcotrees, name='lists_tcotrees'),
    url(r'^add_tcotrees/$', addtcotrees, name='addtcotrees'),
    path('update_tcotrees/<str:pk>/', update_tcotrees, name="update_tcotrees"),
    path('delete_tcotrees/<str:pk>/', delete_tcotrees, name="delete_tcotrees"),
    path('inftco_trees/<str:pk>/', inftco_trees, name="inftco_trees"),
    path('inftco_staff/<str:pk>/', inftco_staff, name="inftco_staff"),
#Loại cây
    url(r'^list_typetrees/$', typetrees, name='typetrees'),
    url(r'^add_typetree/$', addtypetrees, name='addtypetrees'),
    path('update_typetrees/<str:pk>/', update_typetrees, name="update_typetrees"),
    path('delete_typetreespopup/<str:pk>/', delete_typetreespopup, name="delete_typetreespopup"),
#tình trạng cây
    url(r'^list_contrees/$', contrees, name='contrees'),
    url(r'^add_contree/$', addcon, name='addcon'),
    path('update_contrees/<str:pk>/', update_con, name="update_con"),
    path('delete_contreespopup/<str:pk>/', delete_con, name="delete_con"),
    # footer
    # Tương tác bản đồ
    path('map/', show_data, name="map"),
    path('child_tree/',child_tree, name = 'childtree'),
    path('child_street/',child_street, name = 'childstreet'),
    path('child_boun/',child_boun, name = 'childboun'),
    # ######
    path('class/<str:id>/', child_da, name="class"),
# export pdf danh sách cây

    path('export_pdf/', export_pdf, name="export-pdf"),







]
