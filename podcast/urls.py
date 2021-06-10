from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.index, name = 'home'),
    path("podcasts/<int:podcast_id>", views.podcast_detail, name = "podcasts"),
    path("posts/", views.post, name = "post"),
    path("profile/", views.profile, name = "profile"),
    path("logout/", views.logout, name = "logout"),
    path("token/", obtain_auth_token, name = "token"),
    path("developer/api/", views.apiView, name = "api"),
    path("search/podcast/results/", views.search, name = "search"),
]