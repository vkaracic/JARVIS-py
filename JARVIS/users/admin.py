from django.contrib import admin

from users.models import ExtendedUser, Team


admin.site.register(ExtendedUser)
admin.site.register(Team)
