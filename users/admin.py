from django.contrib import admin
from django.contrib.auth.models import User
from users.models import UserProfile,EmailVerification
from django.contrib.auth.admin import UserAdmin


#取消关联注册User
admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile



class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]


#注册关联
admin.site.register(User, UserProfileAdmin)


@admin.register(EmailVerification)
class Admin(admin.ModelAdmin):

    list_display = ('code',)



