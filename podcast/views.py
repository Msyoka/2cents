from django.shortcuts import render, redirect
from .models import Podcasts, Votes, Comments, Profile
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import PostForm,RateForm,ReviewForm,UpdateForm
from django.contrib.auth import logout as django_logout
from rest_framework.response import Response
from rest_framework.views import APIView
#from .serializer import PodcastSerializer,ProfileSerializer

# Create your views here.
def index(request):
    
    try:
        podcasts = Podcasts.objects.all()
    except Exception as e:
        raise Http404()
    return render(request, "main/index.html", {"podcasts": podcasts})

@login_required(login_url = '/accounts/login/')
def post(request):
    current_user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            post.user = current_user
            post.save()
        return redirect("podcasts")
    else:
        form = PostForm()
    return render(request, "main/post.html", {'form':form})


'''Ratings/Votings'''
@login_required(login_url = '/accounts/login/')
def profile(request):
    current_user = request.user
    try:
        profis = Profile.objects.filter(user = current_user)[0:1]
        user_podcasts = Podcasts.objects.filter(user = current_user)
    except Exception as e:
        raise  Http404()
    if request.method == 'POST':
        form = UpdateForm(request.POST,request.FILES)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.user = request.user
            profile.save() 
        return redirect('profile')
    else:
        form = UpdateForm()
    return render(request, "main/profile.html", {'form':form, 'profile':profis, 'podcasts':user_podcasts})

def podcast_detail(request,podcast_id):
    try:
        podcasts = Podcasts.objects.filter(id = podcast_id)
        all = Votes.objects.filter(podcast = podcast_id)
    except Exception as e:
        raise Http404()
    #user single
    count = 0

    for i in all:
        count += i.usability
        count += i.design
        count += i.content

    if count > 0:
        ave = round(count/3,1)

    else:
        ave = 0


    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit = False)
            rate.user = request.user
            rate.podcast = podcast_id
            #review
            rate.save()
            return redirect('podcasts', podcast_id)
    else:
        form = RateForm()

    #logic
    votes = Votes.objects.filter(podcast = podcast_id)
    usability = []
    design = []
    content = []

    for i in votes:
        usability.append(i.usability)
        design.append(i.design)
        content.append(i.content)

    if len(usability) > 0 or len(design)> 0 or len(content) >0:

        average_usa = round(sum(usability)/len(usability),1)
        average_des = round(sum(design)/len(design),1)
        average_con = round(sum(content)/len(content),1)

        averageRating = round((average_con + average_des + average_usa)/3,1)

    else:
        average_usa = 0.0
        average_des = 0.0
        average_con = 0.0

    '''
    Restricting user to rate only once
    '''
    arr1 = []
    for use in votes:
        arr1.append(use.user_id)

    auth=arr1


    if request.method == 'POST':
        review = ReviewForm(request.POST)

        if review.is_valid():
            comment = review.save(commit=False)
            comment.user = request.user
            comment.pro_id = podcast_id
            comment.save()

            return redirect('details',podcast_id)
    else:
        review = ReviewForm()

    try:
        user_comment = Comments.objects.filter(pro_id=podcast_id)

    except Exception as e:
        raise Http404()

    return render(request, "main/podcast.html", {'podcasts':podcasts, 
                                            'form':form, 
                                            'auth':auth, 
                                            'all':all, 
                                            'ave':ave, 
                                            'review':review, 
                                            'comments':user_comment})

'''Search Function'''
def search(request):
    if 'name' in request.GET and request.GET['name']:
        term = request.GET.get('name')
        results = Podcasts.search_podcast(term)

        return render(request,'main/search.html', {'podcasts':results})
    else:
        message = "You havent searched any podcast"
        return render(request,'main/search.html', {'message':message})

@login_required
def logout(request):
    django_logout(request)
    return  HttpResponseRedirect('/')

class PodcastList(APIView):
    def get(self,request,format=None):
        all_podcasts = Podcasts.objects.all()
        serializers = PodcastSerializer(all_podcasts,many=True)

        return Response(serializers.data)

@login_required(login_url='/registration/login/')
def apiView(request):
    current_user = request.user
    title = "Api"
    profiles = Profile.objects.filter(user = current_user)[0:1]

    return render(request,'api.html',{"title":title, 'profile':profiles})

class ProfileList(APIView):
    def get(self,request,format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)

        return Response(serializers.data)