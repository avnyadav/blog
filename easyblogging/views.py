from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import BlogModel,Category
from . forms import Edit_Blog
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.http import HttpResponse
# Create your views here.

def home(request):
    blog = BlogModel.objects.order_by("-created_at")[:6]
    context = {'blogs': blog}
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(BlogModel, id=self.kwargs['pk'])
        lik = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            lik = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = lik
        return data
    return render(request, 'home.html',context)


def user_register(request):
    if request.method == 'POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        passwd  = request.POST.get('password')
        passwd2 = request.POST.get('password2')
        if passwd != passwd2:
            messages.warning(request, 'password does not match')
            return redirect('register')
        elif User.objects.filter(username=uname).exists():
            messages.warning(request, 'username already taken')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.warning(request, 'email already taken')
            return redirect('register')
        else:
            user = User.objects.create_user(first_name=fname, last_name=lname, username=uname, email=email, password=passwd)
            user.save()
            subject = 'About Registration'
            message = f'Hi {uname},You has been registred successfully on EasyBlogging .'
            email_from = 'siwani1.adhikari@gmail.com'
            rec_list = [email,]
            send_mail(subject, message, email_from, rec_list)
            messages.success(request, 'User has been registered successfully')
            return redirect('login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')

        else:
            messages.warning(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')

def post_blog(request):
    if request.method == "POST":
        title = request.POST.get('title')
        con = request.POST.get('Content')
        img = request.FILES['image']
        blog = BlogModel(title=title, content=con, author=request.user, image=img)
        blog.save()
        messages.success(request, 'post has been submitted successfully')
        return redirect('post_blog')

    return render(request,'blog_post.html')

def blog_detail(request,id):
    blog = BlogModel.objects.get(id=id)
    context = {'blog':blog}
    return render(request,'blog_detail.html',context)


def delete(request,id):
    blog = BlogModel.objects.get(id=id)
    blog.delete()
    messages.success(request,'Post has been deleted')
    return redirect('/')

def edit(request,id):
    print(id)
    blog = BlogModel.objects.get(id=id)
    editblog = Edit_Blog(instance=blog)
    if request.method=='POST':
        title = request.POST.get('title')
        con = request.POST.get('content')
        img = request.FILES['image']
        blog.title=title
        print(blog.image,img)
        blog.image=img
        blog.content=con
        blog.save()

        messages.success(request, 'POST has been updated')

        return redirect('/')
    return render(request,'edit_blog.html',{'edit_blog':editblog})


def change_password(request):


        if request.method == 'POST':
            fm = PasswordChangeForm(request.user, request.POST)
            if fm.is_valid():
                fm.save()
                # update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been changed')
                return redirect('/')
            else:
                messages.warning(request, 'Error')
                return redirect('change_password')
        else:
            fm = PasswordChangeForm(user=request.user)
            return render(request,'change_password.html',{'form':fm})

def BlogPostLike(request, pk):
     blog= get_object_or_404(BlogModel, id=request.POST.get('id'))
     if blog.liked.filter(id=request.user.id).exists():
        blog.liked.remove(request.user)
     else:
        post.liked.add(request.user)
     return HttpResponseRedirect(reverse('home', args=[str(pk)]))

def blog_category(request, category):
    posts = BlogModel.objects.filter(categories__name__contains=category)
    context = {"posts":posts}
    return render(request, 'category_detail.html', context)