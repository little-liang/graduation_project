from django.contrib import admin

# Register your models here.
'''admin的扩展属性'''

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from hosts.myauth import UserProfile

'''这里admin的认证登陆具体内容，被admin导入了'''

#密码验证表单，创建用户
class UserCreationForm(forms.ModelForm):
    #密码双重验证
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('email', 'token')

    # 密码双重验证
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    #保存密码
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

#改用户
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    #出现的改密码的地方,这个修改密码一直不出现。。
    password = ReadOnlyPasswordHashField(label="Password")

    ##改密码时输入这几个字段
    class Meta:
        model = UserProfile
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

#加或者改用户的web admin显示界面，就是登陆用户的信息
class UserProfileAdmin(UserAdmin):

    # 表单就是函数
    form = UserChangeForm
    add_form = UserCreationForm

    #显示外层，一堆用户
    list_display = ('email', 'is_admin', 'is_active', 'name', 'department')
    #过滤
    list_filter = ('is_admin', 'date_joined', 'department')

    #打开用户编辑时的具体显示
    fieldsets = (
        # ('name', {'fields': ('email', )}),
        # (None, {'fields': ('name', 'password')}),
        ('账户密码管理', {'fields': ('email', )}),
        ('个人信息列表', {'fields': ('name', 'department', 'tel', 'mobile', 'memo')}),
        ('API TOKEN 信息', {'fields': ('token',)}),
        ('可管理的主机', {'fields': ('bind_hosts',)}),
        ('可管理的主机组', {'fields': ('host_groups',)}),
        ('权限信息', {'fields': ('is_active', 'is_admin')}),
        ('账户有效期', {'fields': ('valid_begin_time', 'valid_end_time')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'password1', 'password2', 'is_active', 'is_admin')}
        )
    )

    #搜索
    search_fields = ('email', 'department')

    #排序
    ordering = ('email',)

    #非常帅的选择框
    filter_horizontal = ('bind_hosts', 'host_groups',)
