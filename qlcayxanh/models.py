from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
import django.db.models.deletion
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
import django.db.models.deletion
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
import django.db.models.deletion
from django.db.models.signals import post_save
from django.dispatch import receiver


class nhanvien(models.Model):
    GENRE_CHOICES = (
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ'),
    )
    ma_nhan_vien = models.CharField('Mã nhân viên', max_length=100, primary_key=True)
    hoten = models.CharField('Họ và tên', max_length=100)
    gioitinh = models.CharField(max_length=3, choices=GENRE_CHOICES)
    dienthoai = models.IntegerField(default=0)
    diachi = models.CharField('Địa chỉ', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.hoten


class ranh_gioi(models.Model):
    GENRE_CHOICES = (
        ('Phường', 'Phường'),
        ('Xã', 'Xã'),
    )
    ma_ranh_gioi = models.CharField('Mã ranh giới',max_length=100, primary_key=True)
    ten_ranh_gioi = models.CharField('Tên ranh giới', max_length=100)
    type_ranh_gioi= models.CharField('Loại ranh giới',max_length=6, choices=GENRE_CHOICES)
    geom = models.MultiPolygonField(srid=4326)
    ghichu = models.CharField(max_length=150, null=True, blank=True)
    def __str__(self):
        return self.ten_ranh_gioi
    def natural_key(self):
        return (self.ten_ranh_gioi)


class duonggiaothong(models.Model):
    ma_duong = models.CharField('Mã đường', max_length=100, primary_key=True)
    ten_duong = models.CharField('Tên đường', max_length=100)
    geom = models.MultiLineStringField(srid=4326)
    ghichu = models.CharField(max_length=150, null=True, blank=True)
    ranh_gioi_id = models.ForeignKey(ranh_gioi, verbose_name="Tên ranh giới", on_delete=models.CASCADE)

    def __str__(self):
        return self.ten_duong

    def natural_key(self):
        return (self.ten_duong)


class loaicay(models.Model):
    ma_loai_cay = models.CharField('mã loại cây', max_length=50, primary_key=True)
    ten_loai_cay = models.CharField('tên loại cây', max_length=100)

    def __str__(self):
        return self.ten_loai_cay

    def natural_key(self):
        return (self.ten_loai_cay)

class tinhtrangcay(models.Model):
    ten_tinh_trang= models.CharField('tên tình trạng cây', max_length=100)

    def __str__(self):
        return self.ten_tinh_trang

    def natural_key(self):
        return (self.ten_tinh_trang)


class cayxanh(models.Model):
    ma_cay = models.CharField(max_length=100, primary_key=True)
    ten_cay = models.CharField(max_length=100)
    chieucao = models.IntegerField()
    vitri = models.CharField(max_length=100)
    ngaytrong = models.DateField('Ngày trồng')
    tinhtrang_id = models.ForeignKey(tinhtrangcay, verbose_name="Tình trạng", on_delete=models.CASCADE)
    dacdiem = models.CharField('Đặc điểm ', max_length=200, null=True, blank=True)
    geom = models.PointField(srid=4326)
    duong_id = models.ForeignKey(duonggiaothong, verbose_name="Tên đường giao thông", on_delete=models.CASCADE)
    loaicay_id = models.ForeignKey(loaicay, verbose_name="Loại cây", on_delete=models.CASCADE)


    def __str__(self):
        return self.ma_cay

class chamsoccay(models.Model):
    cong_viec = models.CharField('Công việc', max_length=100)
    ngay_cham_soc = models.DateField('Ngày chăm sóc')
    nhanvien_id = models.ForeignKey(nhanvien, verbose_name="Nhân viên ", on_delete=models.CASCADE)
    cayxanh_id = models.ForeignKey(cayxanh, verbose_name="Cây xanh", on_delete=models.CASCADE)

    def __unicode__(self):
        return self.cayxanh_id