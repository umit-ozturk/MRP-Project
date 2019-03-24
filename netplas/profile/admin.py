from django.contrib import admin
from profile.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'id', 'name', 'surname',)
    search_fields = ('email',)


admin.site.register(UserProfile, UserProfileAdmin)