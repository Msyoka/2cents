from rest_framework import serializers
from .models import Podcasts,Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=('profile','bio','user')

class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model=Podcasts
        fields=('name','link','description','date')