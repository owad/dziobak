from django.contrib import admin
from product.models import Courier, Product, Comment


class CourierAdmin(admin.ModelAdmin):
    model = Courier

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['name', 'producent', 'serial', 'invoice', 'user']

class CommentAdmin(admin.ModelAdmin):
    model = Comment

admin.site.register(Courier, CourierAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)

