from django.db import models

# Create your models here.

from hosts.myauth import UserProfile

#主机表
class Host(models.Model):
    hostname = models.CharField(max_length=64)
    ip_addr = models.GenericIPAddressField(unique=True)
    port = models.IntegerField(default=22)
    idc = models.ForeignKey('IDC')

    #系统类型选择
    system_type_choices = (
        ('linux', 'Linux'),
        ('windows', 'Windows'),
    )
    #系统类型，拿上面的选择的
    system_type = models.CharField(choices=system_type_choices, max_length=32, default='linux')
    # 是否启用
    enabled = models.BooleanField(default=True)

    #注释
    memo = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "主机列表"
        verbose_name_plural = "主机列表"

    def __str__(self):
        return "%s(%s)" % (self.hostname, self.ip_addr)



class IDC(models.Model):
    name = models.CharField(unique=True, max_length=64)

    class Meta:
        verbose_name = "IDC"
        verbose_name_plural = "IDC"

    def __str__(self):
        return self.name



#主机管理员
class HostUser(models.Model):
    auth_type_choices = (
        ('ssh_password', 'SSH/PASSWORD'),
        ('ssh_key', 'SSH_KEY'),
    )
    auth_type = models.CharField(choices=auth_type_choices, max_length=32, default='ssh_password')
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=128)

    def __str__(self):
        return "%s(%s)" % (self.auth_type, self.username)

    #
    class Meta:
        #联合唯一性 3个加起来唯一
        unique_together = ('auth_type', 'username', 'password')

        #显示名称，定制admin
        verbose_name = "远程主机用户"
        verbose_name_plural = "远程主机用户"


class HostGroup(models.Model):
    name = models.CharField(unique=True, max_length=64)
    memo = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "主机组"
        verbose_name_plural = "主机组"

#这里给绑定关系一张表，我不太明白
class BindHostToUser(models.Model):
    host = models.ForeignKey("Host")

    #这里把用户和 绑定主机关系设置问一对多，一个用户可以绑定多个主机，一个主机只能被一个用户绑定,这里为了防止重复情况出现
    # A用户属于B组，又属于C组，这时，如果B组分配一台主机权限，C组也分配了这个主机，那么A就分配了两次，先用一对多把
    # host_user = models.ManyToManyField("HostUser")
    host_user = models.ForeignKey('HostUser')
    host_group = models.ManyToManyField("HostGroup")

    class Meta:
        unique_together = ('host', 'host_user')
        verbose_name = "主机-用户-绑定关系"
        verbose_name_plural = "主机-用户-绑定关系"

    def __str__(self):
        return "%s:%s" % (self.host.hostname, self.host_user.username)

    #多对多关系不能直接查询出来，给admin使用，做成函数，供给admin
    def get_groups(self):
        return ','.join([g.name for g in self.host_group.select_related()])