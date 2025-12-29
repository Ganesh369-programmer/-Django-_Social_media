from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import login , logout , authenticate  
from .models import Profile , Post , LikePost , Followers
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    #here we try to filter the user who is logged in website
    #and after that we also filter that user who is followed by logged user
    # values_list('user) :- it reterns the value of user who is followed by logged user
    # flat=True :- Without flat: [('alice',), ('bob',), ('carol',)]   ||  With flat=True: ['alice', 'bob', 'carol']

    following_users = Followers.objects.filter(
        follower=request.user.username  #filter all rows from DB according to logged User
    ).values_list('user' , flat=True)    

    
    #__in :- __in is used to filter for any value in a list, not just one value. It’s like saying “give me all posts where the user is in this list of usernames.”
    post = Post.objects.filter(
        Q(user = request.user.username) |  #indicate the who is logged in 
        Q(user__in = following_users)      #it shows and represent all names from followind_users variable
    ).order_by('-created_at')

    # post = Post.objects.all().order_by('-created_at')

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    else:
        profile = None

   
    for p in post:
        try:
            #this line speacially use for fectch the profile image from db according to the login username
            p.profileimg = Profile.objects.get(
                user__username = p.user
            ).profileimg.url   # this is profile image url that is stored in variable

            # it provide the answer in True and False , means if user like the post then True otherwise False
            p.is_liked = LikePost.objects.filter(
                post_id=p.id , username = request.user.username
            ).exists()
            
        except Profile.DoesNotExist:
            p.profileimg = '/media/blank-profile-picture.png' 

    context = {
        'post' : post,
        'profile' : profile,
    }

    return render(request , 'main.html' , context)
    

def signup(request):
    try:
        if request.method == 'POST':
            fnm = request.POST.get('fnm')
            emailid = request.POST.get('email')
            pwd = request.POST.get('pwd')

            my_user = User.objects.create_user(fnm , emailid , pwd)
            my_user.save()


            # Creates a new Profile row
            # Links it to User using ForeignKey / OneToOneField
            # Stores user’s ID separately

            user_model = User.objects.get(username=fnm)
            new_profile = Profile.objects.create(user = user_model , id_user=user_model.id)
            new_profile.save()

            if my_user is not None:
                login(request , my_user)
                return redirect('/')
    except:
        invalid = 'User Already Exists '
        return render(request , 'signup.html' , {'invalid' : invalid})

    return render(request , 'signup.html' )


def loginn(request):
    msg = ""
    if "next" in request.GET:
        msg = "You must be logged in to View that Page."
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')

        userr = authenticate(request , username = fnm , password = pwd )

        if userr is not None:
            login(request , userr)
            return redirect('/')
        else:
            invalid = "Wrong Passward or Username "
            return render(request , 'loginn.html' , {'invalid' : invalid})
    
    return render(request , 'loginn.html' , {'msg' : msg})


@login_required(login_url='/login')
def upload(request):
    if request.method == 'POST':
        user = request.user.username 
        image = request.FILES.get('image-upload')
        caption = request.POST.get('caption')

        new_post = Post.objects.create(user = user , image = image , caption = caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='/login')
def likes(request , id):
    if request.method == 'GET':
        username = request.user.username
        post = get_object_or_404(Post , id=id )
        like_filter = LikePost.objects.filter(post_id=id , username=username).first()
        if like_filter is None:
            new_like = LikePost.objects.create(post_id = id , username = username)
            post.no_of_like = post.no_of_like + 1
            
        else:
            like_filter.delete()
            post.no_of_like = post.no_of_like - 1
            
        
        post.save()

        return redirect('/#'+id)



def home_posts(request , id ):
    post = Post.objects.get(id = id)

    if request.user.is_authenticated:
        profile = profile.objects.get(user = request.user)
    else:
        profile = None

    context = {
        'post':post,
        'profile' : profile,
    } 

    return render (request , 'main.html' , context)


def explore(request):
    post = Post.objects.all().order_by('-created_at')

    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user)
    else:
        profile = None

    for p in post:
        try:
            p.profileimg = Profile.objects.get(user__username=p.user).profileimg.url
        except Profile.DoesNotExist:
            p.profileimg = '/media/blank-profile-picture.png'  # fallback image

    context = {
        'post' : post,
        'profile' : profile,
    }

    return render(request , 'explore.html' , context)


@login_required(login_url='/login')
def profile(request , id_user):
    user_object = User.objects.get(username=id_user)
    profile, created = Profile.objects.get_or_create(user=request.user, defaults={'id_user': request.user.id})

    user_profile = Profile.objects.get(user = user_object)
    user_posts = Post.objects.filter(user = id_user).order_by('-created_at')
    user_post_length = len(user_posts)


    follower = request.user.username
    user = id_user

    if Followers.objects.filter(follower=follower , user=user).first():
        follow_unfollow = 'Unfollow'
    else:
        follow_unfollow = 'Follow'

    user_followers = len(Followers.objects.filter(user = id_user ))
    user_following = len(Followers.objects.filter(follower = id_user))



    context = {
        'user_object':user_object , 
        'user_profile' : user_profile , 
        'user_posts' : user_posts,
        'user_post_length' : user_post_length ,
        'profile' : profile,
        'follow_unfollow' : follow_unfollow,
        'user_following' : user_following,
        "user_followers" : user_followers,
    }

    if request.user.username == id_user:
        if request.method == 'POST':
            if request.FILES.get('image') == None:
                image = user_profile.profileimg
                bio = request.POST['bio']
                location = request.POST['location']

                user_profile.profileimg = image
                user_profile.bio = bio
                user_profile.location = location
                user_profile.save()

            if request.FILES.get('image') != None:
                image = request.FILES.get('image')
                bio = request.POST['bio']
                location = request.POST['location']

                user_profile.profileimg = image
                user_profile.bio = bio
                user_profile.location = location
                user_profile.save()

            return redirect('/profile/'+id_user)
        else:
            return render(request , 'profile.html' , context)

    return render(request , 'profile.html' , context)


@login_required(login_url='/login')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if Followers.objects.filter(follower=follower , user=user).first():
            delete_follower = Followers.objects.get(follower=follower , user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = Followers.objects.create(follower=follower , user=user)
            new_follower.save()
            return redirect('/profile/'+user)
        
    else:
        return redirect('/')

import os


@login_required(login_url='/login')
def delete(request, id):
    post = Post.objects.get(id=id)

    if post.image:
        if os.path.isfile(post.image.path):
            os.remove(post.image.path)

    post.delete()
    return redirect('/profile/' + request.user.username)


def search_result(request):
    query = request.GET.get('q')
    users = Profile.objects.filter(user__username__icontains=query)
    posts = Post.objects.filter(caption__icontains=query)

    context = {
        'query' : query,
        'users' : users,
        'posts' : posts,

    }
    
    return render(request , 'search_user.html' , context)

@login_required(login_url='/login')
def logoutt(request):
    logout(request)
    return redirect('/login')


import uuid

def like_list(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user)
    else:
        profile = None

   # Get liked post IDs (as strings)
    liked_post_ids = LikePost.objects.filter(
        username=request.user.username
    ).values_list('post_id', flat=True)

    # Convert string UUIDs → UUID objects
    liked_post_ids = [uuid.UUID(pid) for pid in liked_post_ids]

    # Fetch liked posts
    liked_posts = Post.objects.filter(
        id__in=liked_post_ids
    ).order_by('-created_at')

     # Get all profiles in ONE query
    for p in liked_posts:
        try:
            #this line speacially use for fectch the profile image from db according to the login username
            p.profileimg = Profile.objects.get(
                user__username = p.user
            ).profileimg.url   # this is profile image url that is stored in variable

            # it provide the answer in True and False , means if user like the post then True otherwise False
            p.is_liked = LikePost.objects.filter(
                post_id=p.id , username = request.user.username
            ).exists()
            
        except Profile.DoesNotExist:
            p.profileimg = '/media/blank-profile-picture.png' 

    return render(request, 'liked_list.html', {
        'view_like': liked_posts , 'profile' : profile
    })
