import django_filters
from qlcayxanh.models import *

class treeFilter(django_filters.FilterSet):
    month_joined = django_filters.NumberFilter(field_name='ngaytrong', lookup_expr='month')
    class Meta:
        model = cayxanh
        fields = ['ten_cay','loaicay_id','tinhtrang_id','duong_id','month_joined' ]

class userFilter(django_filters.FilterSet) :
    class Meta:
        model = User
        fields=['username']