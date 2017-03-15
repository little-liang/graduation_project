from django.contrib import admin
from hosts import auth_admin   #把auth_admin包含进来

# Register your models here.
from hosts import models

admin.site.register(models.UserProfile, auth_admin.UserProfileAdmin) ##自定制admin，增加了auth_admin.UserAdmin