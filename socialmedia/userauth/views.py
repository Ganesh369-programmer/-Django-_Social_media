from django.shortcuts import render , redirect
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import login , logout , authenticate  
from .models import Profile , Post
# Create your views here.

def home(request):
    post = Post.objects.all().order_by('-created_at')
    # profile = Profile.objects.get(user = request.user)
    context = {
        'post' : post,
        # 'profile' : profile,
    }
    return render(request, 'main.html' , context)
    

def signup(request):
    try:
        if request.method == 'POST':
            fnm = request.POST.get('fnm')
            emailid = request.POST.get('email')
            pwd = request.POST.get('pwd')

            my_user = User.objects.create_user(fnm , emailid , pwd)
            my_user.save()

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
    
    return render(request , 'loginn.html')

def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image-upload')
        caption = request.POST['caption']
        new_post = Post.objects.create(user = user , image = image , caption = caption )
        new_post.save()
        return redirect('/')
    
    else:
        return redirect('/')
    

def logoutt(request):
    logout(request)
    return redirect('/login')


