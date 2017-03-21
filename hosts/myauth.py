from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import django

'''
    这里一劳永逸的用户登陆表 这家伙 导入的模块有点牛掰

'''


#继承了Django的BaseUserManager，与createsuperuser有关，创建用户
class UserManager(BaseUserManager):

    #创建用户，用email方式
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # 创建超级用户，其实就是调用的BaseUserManager的create_user
    def create_superuser(self, email, name, password):
        user = self.create_user(email, password=password, name=name,)
        user.is_admin = True
        user.save(using=self._db)
        return user


#继承的是Django官方的AbstractBaseUser，这个是真正的用户表
class UserProfile(AbstractBaseUser):

    # 邮箱地址
    email = models.EmailField(
        verbose_name='email address',
        max_length=64,
        unique=True,
    )

    #是否启用
    is_active = models.BooleanField(default=True)
    #是否是admin
    is_admin = models.BooleanField(default=False)

    name = models.CharField(max_length=32)

    #目前不知道这个token有啥用
    token = models.CharField('token', max_length=128, default=None, blank=True, null=True)
    department = models.CharField('部门', max_length=32, default=None,blank=True, null=True)
    tel = models.CharField('座机', max_length=32, default=None, blank=True, null=True)
    mobile = models.CharField('手机', max_length=32, default=None, blank=True, null=True)

    #备注
    memo = models.TextField('备注', blank=True, null=True, default=None)
    #用户创建时间
    date_joined = models.DateTimeField(blank=True, auto_now_add=True)

    #字段 用户所在的主机组， 多对多
    host_groups = models.ManyToManyField("HostGroup", blank=True)

    # 字段 用户所绑定的主机， 多对多
    bind_hosts = models.ManyToManyField('BindHostToUser', blank=True)

    #用户生效日期 开始结束 时间
    valid_begin_time = models.DateTimeField(default=django.utils.timezone.now)
    valid_end_time = models.DateTimeField(blank=True,  null=True)


    '''以下的不太懂，目前没用到除了最后两个'''

    #email当作用户名
    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['name','token','department','tel','mobile','memo']
    REQUIRED_FIELDS = ['name']

    #获取名字方法
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin



    #最后两个
    class Meta:
        verbose_name = '登录用户信息'
        verbose_name_plural = "登录用户信息"

    #这个在Userprofile类下，引用了UserManager类
    objects = UserManager()