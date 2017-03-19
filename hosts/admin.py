from django.contrib import admin
from hosts import auth_admin   #把auth_admin包含进来

# Register your models here.
from hosts import models

class HostAdmin(admin.ModelAdmin):

    #显示admin表结构
    list_display = ('hostname', 'ip_addr', 'port', 'idc', 'system_type', 'enabled',)
    #搜索表
    search_fields = ('hostname', 'ip_addr',)

    #过滤机制
    list_filter = ('system_type', 'idc',)

class HostUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'auth_type',)

class BindHostToUserAdmin(admin.ModelAdmin):

    #这里不能写多对多关系，host_groups就是多对多关系
    # list_display = ('host', 'host_user', 'host_groups',)

    ##对于多对多关系，用专门的函数方法实现,所以在models中应该有这个函数 def get_groups(self):

    list_display = ('host', 'host_user', 'get_groups')
    filter_horizontal = ('host_group',)





admin.site.register(models.UserProfile, auth_admin.UserProfileAdmin) ##自定制admin，增加了auth_admin.UserAdmin

#上面的class想有效，就帮在后面Host --> HostAmin
admin.site.register(models.Host, HostAdmin)
admin.site.register(models.HostGroup)

#上面的class想有效，就帮在后面HostUserAdmin
admin.site.register(models.HostUser, HostUserAdmin)
admin.site.register(models.BindHostToUser, BindHostToUserAdmin)
admin.site.register(models.IDC)