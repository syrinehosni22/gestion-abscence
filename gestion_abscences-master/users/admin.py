from django.contrib import admin

from users.models import User, UserImage

admin.site.register(User)
admin.site.register(UserImage)
