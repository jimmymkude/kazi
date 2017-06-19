from django.contrib import admin

from .models import AjiraUser, Post, JobTitle, Location, CareerInterests
# Register your models here.


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['first_name', 'middle_initial', 'last_name', 'email', 'username']}),
    ]
    inlines = [PostInline]

#admin.site.register(User)
admin.site.register(AjiraUser, UserAdmin)
admin.site.register(JobTitle)
