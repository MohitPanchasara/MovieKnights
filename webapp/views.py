from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import profilepic

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        pr=profilepic.objects.all().filter(user=request.user)
        c={"img":pr}
        return render(request,"home.html",context=c)
    else:
        return redirect('/login')

def signin(request):

    if request.user.is_authenticated:
        return redirect('/')
    
    else: 
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return redirect('/login')
            
        else:
            return render(request, 'login.html')
    
            
def signout(request):
    logout(request)
    return redirect('/login')


def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        confpassword=request.POST['confirmpassword']
        if password==confpassword:
            user=User.objects.create_user(username=username,password=password)
            user.save()
            login(request,user)
            return redirect('/')
        else:
            return redirect('/signup')
    else:
        return render(request,"signup.html")

def upload(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            pr=profilepic.objects.all().filter(user=request.user)
            pr.delete()
            pic=request.FILES['pic']
            new=profilepic(user=request.user,pic=pic)
            new.save()
            return redirect('/home')
        else:
            return redirect('/home')
    else:
        return redirect('/home')