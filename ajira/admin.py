from django.contrib import admin

from .models import User, Post
# Register your models here.


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['first_name', 'middle_initial', 'last_name', 'email']}),
    ]
    inlines = [PostInline]

#admin.site.register(User)
admin.site.register(User, UserAdmin)
