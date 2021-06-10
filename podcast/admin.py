from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Profile, Comments, Votes, Projects

# Register your models here.
admin.site.register(Projects)
admin.site.register(Profile)
admin.site.register(Comments)
admin.site.register(Votes)