from django.shortcuts import render,HttpResponse , redirect
from home1.models import Contact
from blog1.models import Post ,Category,Tag
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
# import time

def home(request):
    # return HttpResponse('This is home')
    popular_post=Post.objects.filter(section='Popular',status=1).order_by('-id')[0:4]
    main_post=Post.objects.filter(Main_post=True ,status=1)[0:1]
    Trending=Post.objects.filter(section='Trending',status=1).order_by('-id')
    Latest_posts=Post.objects.filter(section='Latest Posts',status=1).order_by('-id')[0:4]
    Popular=Post.objects.filter(section='Popular',status=1).order_by('-id')[0:4]
    category = Category.objects.all()
    # category_post=Post.objects.filter(category=category)
    # print(category_post)
    tags=Tag.objects.values('name').distinct()

    context={
        'popular_post':popular_post,
        'main_post':main_post,
        'Trending':Trending,
        'Latest_posts':Latest_posts,
        'Popular':Popular,
        'category':category,
        'tags':tags,

    }
    # return render(request,'Main/index.html',context)

    return render(request ,'home/index.html',context)

def about(request):
    category = Category.objects.all()
    Popular=Post.objects.filter(section='Popular',status=1).order_by('-id')[0:4]
    tags=Tag.objects.values('name').distinct()
    post = Post.objects.filter(status=1)
    # for i in post:

    #     print(i.author)

    context={
        'category':category,
        'Popular':Popular,
        'tags':tags,
        'post':post,
    }
    return render(request ,'home/about.html' , context)

def write_and_earn(request):
    if request.method=="POST":
        featured_image=request.FILES['featured_image']
        title=request.POST['title']
        author=request.POST['author']
        category=request.POST['category']
        content =request.POST['content']
        slug=request.POST['slug']
        status='0'
        section=request.POST['section']
        url=request.POST['url']
        timeStamp_0=request.POST['timeStamp_0']
        timeStamp_1=request.POST['timeStamp_1']
        ts=timeStamp_0 +" "+ timeStamp_1
        timeStamp=ts
        Main_post=False
        post_views=request.POST['post_views']

        # want some more condition
        if len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            post=Post(featured_image=featured_image,title=title, author=author, category=Category.objects.get(name=category), content=content,slug=slug,status=status,section=section,url=url,timeStamp=timeStamp,Main_post=Main_post,post_views=post_views)
            post.save()
            messages.success(request, "Your message has been successfully sent")
    
    category = Category.objects.all()
    context={
        'category':category,
    }
    return render(request ,'blog/write_and_earn.html',context)
    
    
# def contact(request):
#     # return HttpResponse('This is contact')
#     return render(request ,'home/contact.html')

# Create your views here.


def post(request, section):
    post = Post.objects.get(section=section ,status=1)
    popular_post=Post.objects.filter(section='Popular',status=1).order_by('-id')[0:4]
    # recent_post=Post.objects.filter(section='Recent',status=1).order_by('-id')[0:4]
    main_post=Post.objects.filter(Main_post=True)[0:1]
    Editor_Pick=Post.objects.filter(section='Editors_Pick',status=1).order_by('-id')
    Trending=Post.objects.filter(section='Trending',status=1).order_by('-id')
    Inspiration=Post.objects.filter(section='Inspiration',status=1).order_by('-id')[0:2]
    Latest_posts=Post.objects.filter(section='Latest Posts',status=1).order_by('-id')[0:4]
    Popular=Post.objects.filter(section='Popular',status=1).order_by('-id')[0:4]
    category = Category.objects.all()
    
    context={
        'post':post,
        'popular_post':popular_post,
        # 'recent_post':recent_post,
        'main_post':main_post,
        # 'Editors_Pick':Editor_Pick,
        'Trending':Trending,
        # 'Inspiration':Inspiration,
        'Latest_posts':Latest_posts,
        'Popular':Popular,
        'category':category,

    }

    # print(post)
    return render(request, 'blog/posts.html', context)


def category(request,url):
    category = Category.objects.get(url=url)
    # posts = Post.objects.filter(cat=cat)
    post = Post.objects.filter(status=1,category=category)
    # recent_post=Post.objects.filter(section='Recent',status=1).order_by('-id')[0:4]
    # main_post=Post.objects.filter(Main_post=True)[0:1]
    # Editor_Pick=Post.objects.filter(section='Editors_Pick',status=1).order_by('-id')
    Trending=Post.objects.filter(section='Trending',status=1).order_by('-id')
    # Inspiration=Post.objects.filter(section='Inspiration',status=1).order_by('-id')[0:2]
    Latest_posts=Post.objects.filter(section='Latest Posts',status=1).order_by('-id')[0:4]
    Popular=Post.objects.filter(section='Popular',status=1).order_by('-id')[0:4]
    
    category = Category.objects.all()

    context={
        'category':category,
        'post':post,
        # 'recent_post':recent_post,
        # 'main_post':main_post,
        # 'Editors_Pick':Editor_Pick,
        'Trending':Trending,
        # 'Inspiration':Inspiration,
        'Latest_posts':Latest_posts,
        'Popular':Popular,

    }
    return render(request, 'blog/category.html',context)


def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content =request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    
    category = Category.objects.all()

    context={
        'category':category,

    }
    return render(request, "home/contact.html",context)


# def blogcategoryhome(request):
#     return render(request ,'home/index.html')

def search(request):
    category = Category.objects.all()
    Popular=Post.objects.filter(section='Popular',status=1).order_by('-id')[0:4]
    all_tags=Tag.objects.values('name').distinct()
    query=request.GET['query']
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=query ,status=1)
        allPostsAuthor= Post.objects.filter(author__icontains=query ,status=1)
        allPostsContent =Post.objects.filter(content__icontains=query ,status=1)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={
    'allPosts': allPosts,
    'category':category,
    'Popular':Popular,
    'query':query,
    'all_tags':all_tags,
    }
    return render(request, 'home/search.html', params)


# signup
def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if len(username)<5:
            messages.error(request, " Your user name must be under 5 characters")
            return redirect('home')

        # username must be only letters and numbers 
        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')

        # password should match 
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('home')
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your account has been successfully created")
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    else:
        return HttpResponse("404 - Not found")

# login
def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")

    return HttpResponse("404- Not found")

# logout
def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect(request.META.get('HTTP_REFERER', 'home'))
