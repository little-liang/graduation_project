from django.db import models

# Create your models here.
from hosts.myauth import UserProfile
'''
    这里的用户登陆信息，分成了两块，一个是myauth.py 负责用户登陆认证的，据说可以一劳永逸
    另一个是当前的这个文件，负责的是hosts这个app的具体内容的表设计

    表里的数据可以用python manage.py shell
    from hosts import models
    models.Host.objects.all()
'''


#主机表
class Host(models.Model):
    hostname = models.CharField(max_length=64)
    ip_addr = models.GenericIPAddressField(unique=True)
    port = models.IntegerField(default=22)
    #机房名
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

    #备注
    memo = models.TextField(blank=True, null=True)

    #这个是日期可以弄个创建日期之类的
    date = models.DateTimeField(auto_now_add=True)

    #models的表的扩展属性，verbose_name verbose_name_plural是admin.py中表的字段的显示名称
    class Meta:
        verbose_name = "主机列表"
        verbose_name_plural = "主机列表"

    #表的admin的显示名称
    def __str__(self):
        return "%s(%s)" % (self.hostname, self.ip_addr)


#机房表
class IDC(models.Model):
    name = models.CharField(unique=True, max_length=64)

    class Meta:
        verbose_name = "IDC"
        verbose_name_plural = "IDC"

    def __str__(self):
        return self.name



#主机用户名密码，与登陆用户是分开的
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
        #联合唯一性 3个加起来唯一主键，这个比较厉害，话说设计表结构不容易。
        # 认证类型 用户名 密码 三个字段联合唯一
        unique_together = ('auth_type', 'username', 'password')


        verbose_name = "远程主机用户"
        verbose_name_plural = "远程主机用户"

#主机组表
class HostGroup(models.Model):
    name = models.CharField(unique=True, max_length=64)

    #备注
    memo = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "主机组"
        verbose_name_plural = "主机组"

    def __str__(self):
        return self.name

#主机用户 主机组 绑定关系表
#这个是为了处理 主机用户如 root mysql用户用ssh之类的方式操纵 主机 或者 主机组的主机
class BindHostToUser(models.Model):

    #主机 用户 关系 感觉像 多对多才对
    host = models.ForeignKey("Host")

    #这里把用户和 绑定主机关系设置问一对多，一个用户可以绑定多个主机，一个主机只能被一个用户绑定,这里为了防止重复情况出现
    # A用户属于B组，又属于C组，这时，如果B组分配一台主机权限，C组也分配了这个主机，那么A就分配了两次，先用一对多把
    # host_user = models.ManyToManyField("HostUser")
    host_user = models.ForeignKey('HostUser')

    # 主机组 用户 关系 多对多
    host_group = models.ManyToManyField("HostGroup")

    class Meta:

        #host 主机 host_user 用户名密码 联合唯一
        unique_together = ('host', 'host_user')
        verbose_name = "主机-用户-绑定关系"
        verbose_name_plural = "主机-用户-绑定关系"

    def __str__(self):
        return "%s:%s" % (self.host.hostname, self.host_user.username)

    #多对多关系不能直接查询出来，给admin使用，做成函数，供给admin定制显示使用，
    def get_groups(self):
        return ','.join([g.name for g in self.host_group.select_related()])

class TaskLog(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    task_type_choices = (('mutli_cmd', "CMD"), ('file_send', "批量发送文件"), ('file_get', "批量下载文件"))
    task_type = models.CharField(choices=task_type_choices, max_length=50)
    files_dir = models.CharField("文件上传临时目录", blank=True, null=True, max_length=32)
    user = models.ForeignKey('UserProfile')
    hosts = models.ManyToManyField('BindHostToUser')
    cmd = models.TextField()
    expire_time = models.IntegerField(default=30)
    task_pid = models.IntegerField(default=0)
    note = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "taskid:%s cmd:%s" % (self.id, self.cmd)

    class Meta:
        verbose_name = '批量任务'
        verbose_name_plural = '批量任务'

class TaskLogDetail(models.Model):
    child_of_task = models.ForeignKey('TaskLog')
    bind_host = models.ForeignKey('BindHostToUser')
    date = models.DateTimeField(auto_now_add=True)  # finished date
    event_log = models.TextField()
    result_choices = (('success', 'Success'), ('failed', 'Failed'), ('unknown', 'Unknown'))
    result = models.CharField(choices=result_choices, max_length=30, default='unknown')
    note = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "child of:%s result:%s" % (self.child_of_task.id, self.result)

    class Meta:
        verbose_name = '批量任务日志'
        verbose_name_plural = '批量任务日志'