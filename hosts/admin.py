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
    list_filter = ('system_type', 'idc')

class HostUserAdmin(admin.ModelAdmin):
    list_display = ('auth_type', 'username', 'password')


admin.site.register(models.UserProfile, auth_admin.UserProfileAdmin) ##自定制admin，增加了auth_admin.UserAdmin

#上面的class想有效，就帮在后面Hos
admin.site.register(models.Host, HostAdmin)
admin.site.register(models.HostGroup)

#上面的class想有效，就帮在后面HostUserAdmin
admin.site.register(models.HostUser, HostUserAdmin)
admin.site.register(models.BindHostToUser)
admin.site.register(models.IDC)