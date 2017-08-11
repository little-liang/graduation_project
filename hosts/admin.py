from django.contrib import admin
from hosts import auth_admin   #把auth_admin包含进来

# Register your models here.
from hosts import models


'''admin使用的是Django自带的admin,这里导入了auth_admin作为了额外的admin扩展'''


#这里是关于表数据的web界面管理的定制，注意，是定制admin的显示及过滤及搜索之类及选择框之类的
#这里具体是主机表web admin界面
class HostAdmin(admin.ModelAdmin):

    #具体显示admin表的字段，注意多对多不能直接查询出来
    list_display = ('hostname', 'ip_addr', 'port', 'idc', 'system_type', 'enabled',)

    #可供搜索的字段
    search_fields = ('hostname', 'ip_addr',)

    #过滤条件，右边栏，可以多级过滤
    list_filter = ('system_type', 'idc',)

#这里是主机用户表的 web admin 管理界面
class HostUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'auth_type',)

#绑定关心表的web admin定制
class BindHostToUserAdmin(admin.ModelAdmin):

    '''
    这里不能写多对多关系，host_groups就是多对多关系
    list_display = ('host', 'host_user', 'host_groups',)
    对于多对多关系，用专门的函数方法实现,所以在models中应该有这个函数 def get_groups(self):
    '''

    list_display = ('host', 'host_user', 'get_groups')

    #非常帅的前端选择框
    filter_horizontal = ('host_group',)





###真正的使用admin, 用上面的具体定制的类

##自定制admin登陆，就是用auth_admin.UserProfileAdmin这里定义的登陆方式登陆
admin.site.register(models.UserProfile, auth_admin.UserProfileAdmin)

#上面的class想有效，就帮在后面Host --> HostAdmin，意思是主机表放入admin管理，具体的管理方式是HostAdmin类定义的界面
admin.site.register(models.Host, HostAdmin)

admin.site.register(models.HostGroup)

#上面的class想有效，就帮在后面HostUserAdmin，意思是主机用户放入admin管理，具体的管理方式是HostUserAdmin类定义的界面
admin.site.register(models.HostUser, HostUserAdmin)
admin.site.register(models.BindHostToUser, BindHostToUserAdmin)
admin.site.register(models.IDC)

#批量命令记录及相关日志记录
admin.site.register(models.TaskLog)
admin.site.register(models.TaskLogDetail)