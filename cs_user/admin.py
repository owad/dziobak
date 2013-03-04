from django.contrib import admin
from cs_user.models import User, Company

class UserAdmin(admin.ModelAdmin):
    model = User

class CompanyAdmin(admin.ModelAdmin):
    model = Company

admin.site.register(User, UserAdmin)
admin.site.register(Company, CompanyAdmin)

