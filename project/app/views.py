from django.core.mail import message
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Contact,Blogs
# below import is done for sending emails
from django.conf import settings
from django.core.mail import send_mail
from django.core import mail
from django.core.mail.message import EmailMessage
# Create your views here.
def index(request):   
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method=="POST":
        fname=request.POST.get("name")
        femail=request.POST.get("email")
        phone=request.POST.get("phone")
        desc=request.POST.get("desc")
        query=Contact(name=fname,email=femail,phoneNumber=phone,description=desc)
        query.save()
        # emails sending starts from here
        from_email=settings.EMAIL_HOST_USER
        connection=mail.get_connection()
        connection.open()
        email_message=mail.EmailMessage(f'Email from {fname}',f'UserEmail : {femail}\nUserPhoneNumber : {phone}\n\n\n QUERY : {desc}',from_email,['aneesurrehman423@gmail.com','aneesrehman95567@gmail.com'],connection=connection)
        email_client=mail.EmailMessage('Arkprocoder Response','Thanks For Reaching us\n\narkprocoder.tech\n9986786453\nanees@arkprocoder.tech',from_email,[femail],connection=connection)

        connection.send_messages([email_message,email_client])
        connection.close()
        messages.info(request,"Thanks For Reaching Us! We will get back you soon....")
        return redirect('/contact')
    return render(request,'contact.html')

def handlelogin(request):
    if request.method=="POST":
        uname=request.POST.get("username")
        pass1=request.POST.get("pass1")
        myuser=authenticate(username=uname,password=pass1)
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentails")
            return redirect('/login')
    return render(request,'login.html')

def handlesignup(request):
    if request.method=="POST":
        uname=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("pass1")
        confirmpassword=request.POST.get("pass2")
        # print(uname,email,password,confirmpassword)
        if password!=confirmpassword:
            messages.warning(request,"Password is Incorrect")
            return redirect('/signup')


        try:
            if User.objects.get(username=uname):
                messages.info(request,"UserName Is Taken")
                return redirect('/signup')
        except:
            pass
        try:
            if User.objects.get(email=email):
                messages.info(request,"Email Is Taken")
                return redirect('/signup')
        except:
            pass
    
        myuser=User.objects.create_user(uname,email,password)
        myuser.save()
        messages.success(request,"Signup Success Please login!")
        return redirect('/login')
              
    return render(request,'signup.html')


def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/login')


def handleBlog(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Hey just login and Use my website")
        return redirect('/login')
    allPosts=Blogs.objects.all()
    context={'allPosts':allPosts}
    print(allPosts)
    return render(request,'blog.html',context)

def search(request):
    query=request.GET['search']
    if len(query)>100:
        allPosts=Blogs.objects.none()
    else:
        allPostsTitle=Blogs.objects.filter(title__icontains=query)
        allPostsDescription=Blogs.objects.filter(description__icontains=query)
        allPosts=allPostsTitle.union(allPostsDescription)
    if allPosts.count()==0:
        messages.warning(request,"No Search Results")
    params={'allPosts':allPosts,'query':query}

    return render(request,'search.html',params)