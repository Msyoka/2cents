from django.contrib import admin
from .models import Profile, Comments, Votes, Podcasts

# Register your models here.
admin.site.register(Podcasts)
admin.site.register(Profile)
admin.site.register(Comments)
admin.site.register(Votes)