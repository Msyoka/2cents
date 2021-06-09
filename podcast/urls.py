from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.index, name = 'home'),
    path("posts/", views.post, name = "post"),
    path("profile/", views.profile, name = "profile"),
    path("logout/", views.logout, name = "logout"),
    path("token/", obtain_auth_token, name = "token"),
    path("developer/api/", views.apiView, name = "api"),
]