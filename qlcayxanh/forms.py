from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,SetPasswordForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from qlcayxanh import models
from qlcayxanh.models import *
from django.contrib.gis.db.models import MultiPolygonField
from django.contrib.gis import forms
from leaflet.forms.widgets import LeafletWidget
LEAFLET_WIDGET_ATTRS = {
    'map_height': '600px',
    'map_width': '50%',
    'display_raw': 'true',
    'map_srid': 4326,
}

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=False, help_text='Không bắt buộc.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Không bắt buộc')
    username = forms.CharField(required=True, help_text = _('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'))
    is_staff= forms.BooleanField(required=False)
    is_active = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'is_superuser'
        )


class UserForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'is_superuser'
        )

class Password_ChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': _("Mật khẩu cũ của bạn không đúng, vui lòng nhập lại."),
    }
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password1 = forms.CharField(  label=_("Nhập mật khẩu mới"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),help_text=(""))
    new_password2 = forms.CharField(label=_("Nhập lại mật khẩu mới"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),help_text=_(""))
    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password
# Nhân viên form
class nhanvienForm(ModelForm):
    class Meta:
        model = nhanvien
        fields = '__all__'
#---------------------------------------#
# ranh giới form
class ranhgioiForm(ModelForm):
    geom = forms.MultiPolygonField(
        widget=LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS))
    class Meta:
        model = ranh_gioi
        fields = (
            'ma_ranh_gioi',
            'type_ranh_gioi',
            'ten_ranh_gioi',
            'geom',
            'ghichu'
        )
# cây xanh form
class cayxanhForm(ModelForm):
    geom = forms.PointField(
        widget=LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS))
    class Meta:
        model = cayxanh
        fields = (
            'ma_cay',
            'ten_cay',
            'chieucao',
            'vitri',
            'ngaytrong',
            'tinhtrang_id',
            'dacdiem',
            'geom',
            'duong_id',
            'loaicay_id'
        )

# ----------------------------#
# Đường giao thông form
class streetsForm(ModelForm):
    geom = forms.MultiLineStringField(
        widget=LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS))
    class Meta:
        model = duonggiaothong
        fields = (
            'ma_duong',
            'ten_duong',
            'geom',
            'ghichu',
            'ranh_gioi_id'
        )
# Chăm sóc cây
class chamsoccayForm(ModelForm):
    class Meta:
        model = chamsoccay
        fields = (
            'cong_viec',
            'ngay_cham_soc',
            'nhanvien_id',
            'cayxanh_id'
        )
class treeSearchForm(forms.ModelForm):
    class Meta:
        model = cayxanh
        fields = ['ma_cay','ten_cay','loaicay_id']

class loaicayForm(ModelForm):
    class Meta:
        model = loaicay
        fields = '__all__'

class tinhtrangcayForm(ModelForm):
    class Meta:
        model = tinhtrangcay
        fields = '__all__'