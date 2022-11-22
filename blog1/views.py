from django.shortcuts import render,HttpResponse, redirect
from blog1.models import Post ,Category,Tag , BlogComment
from django.contrib import messages
from django.contrib.auth.models import User
from blog1.templatetags import extras
import time
from django.core.paginator import Paginator , EmptyPage

def bloghome(request):
    return HttpResponse('This is  blogs home')

def blogabout(request):
    return HttpResponse('This is blogs about')

# def blogcategory(request,url):
#     # page_title=Category.objects.get(url=url)
#     popular_post=Post.objects.filter(section='Popular',status=1).order_by('-id')[0:4]
#     # main_post=Post.objects.filter(Main_post=True)[0:1]
#     Trending=Post.objects.filter(section='Trending',status=1).order_by('-id')
#     Latest_posts=Post.objects.filter(section='Latest Posts',status=1).order_by('-id')[0:4]
#     Popular=Post.objects.filter(section='Popular',status=1).order_by('-id')[0:4]
    
#     category = Category.objects.all()

#     context={
#         'popular_post':popular_post,
#         # 'recent_post':recent_post,
#         # 'main_post':main_post,
#         # 'Editors_Pick':Editor_Pick,
#         'Trending':Trending,
#         # 'Inspiration':Inspiration,
#         'Latest_posts':Latest_posts,
#         'Popular':Popular,
#         'category':category,

#     }
#     return render(request, 'blog/category1.html',context)
    # return HttpResponse(f'This is blogs contact {slug}')

def blogcontact(request):
    return HttpResponse('This is blogs contact')

def blogPost(request,slug):
    return HttpResponse(f'This is blogs : {slug}')

# tags
def tags(request,name):
    category = Category.objects.all()
    # post_for_tag=Post.objects.all()
    post = Post.objects.filter(status=1)
    # post_for_tag=Post.objects.filter(tag=name)
    tag=Tag.objects.filter(name=name)

    # print(tag)
    # tag.post=Post.objects.filter(status=1)
    popular_post=Post.objects.filter(section='Popular',status=1).order_by('-id')[0:4]
    Popular=Post.objects.filter(section='Popular',status=1).order_by('-id')[0:4]
    all_tags=Tag.objects.values('name').distinct()
    # print(tag.post)
    context={
        # 'tags':tags,
        'tag':tag,
        'category':category,
        'Popular':Popular,
        'popular_post':popular_post,
        'all_tags':all_tags,
        'post':post,
        

    }
    # return HttpResponse(f'This is blogs : {url}')
    return render(request, 'blog/tags.html', context)

# Create your views here.
def post(request, slug):
    post = Post.objects.filter(slug=slug ,status=1).first()
    # comments= BlogComment.objects.filter(post=post)
    popular_post=Post.objects.filter(section='Popular',status=1).order_by('-id')[0:4]
    Popular=Post.objects.filter(section='Popular',status=1).order_by('-id')[0:4]
    all_tags=Tag.objects.values('name').distinct()
    category = Category.objects.all()
    tags=Tag.objects.filter(post=post)
    # print(request.user)
    # print(tags)
    comments= BlogComment.objects.filter(post=post, parent=None)
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    # print(comments)
    # views count 
    blog_view_count=Post.objects.get(slug=slug,status=1)
    blog_view_count.post_views=blog_view_count.post_views + 1
    blog_view_count.save()

    # time.sleep(5)

    context={
        'post':post,
        'popular_post':popular_post,
        # 'recent_post':recent_post,
        # 'main_post':main_post,
        # 'Editors_Pick':Editor_Pick,
        # 'Trending':Trending,
        # 'Inspiration':Inspiration,
        # 'Latest_posts':Latest_posts,
        'comments': comments,
        'Popular':Popular,
        'category':category,
        'tags':tags,
        'user':request.user,
        'replyDict': replyDict,
        'blog_view_count':blog_view_count,
        'all_tags':all_tags

    }

    # print(post)
    return render(request, 'blog/posts.html', context)


def category(request,url):
    category = Category.objects.get(url=url)
    # posts = Post.objects.filter(cat=cat)
    post = Post.objects.filter(category=category ,status=1)
    category_title=Post.objects.filter(category=category).first()
    # recent_post=Post.objects.filter(section='Recent',status=1).order_by('-id')[0:4]
    # main_post=Post.objects.filter(Main_post=True)[0:1]
    # Editor_Pick=Post.objects.filter(section='Editors_Pick',status=1).order_by('-id')
    Trending=Post.objects.filter(section='Trending',status=1).order_by('-id')
    # Inspiration=Post.objects.filter(section='Inspiration',status=1).order_by('-id')[0:2]
    Latest_posts=Post.objects.filter(section='Latest Posts',status=1).order_by('-id')[0:4]
    Popular=Post.objects.filter(section='Popular',status=1).order_by('-id')[0:4]
    
    all_tags=Tag.objects.values('name').distinct()
    category = Category.objects.all()

    # page_n = request.GET.get('page', 1) 
    # p = Paginator(post , 3)
    # try:
    #     page = p.page(page_n)
    # except EmptyPage:
    #     page = p.page(1)

    context={
        'category':category,
        'post':post,
        'category_title':category_title,
        # 'recent_post':recent_post,
        # 'main_post':main_post,
        # 'Editors_Pick':Editor_Pick,
        'Trending':Trending,
        # 'Inspiration':Inspiration,
        'Latest_posts':Latest_posts,
        'Popular':Popular,
        'all_tags':all_tags,
        # 'page':page,

    }
    return render(request, 'blog/category.html',context)

def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        # postSno =request.POST.get('postSno')
        slug =request.POST.get('slug')
        post = Post.objects.filter(slug=slug ,status=1).first()
        
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
        # comment=BlogComment(comment= comment, user=user, post=post)
        # comment.save()
        # # print(post.slug)
        # # print(user)
        # # print(comment)
        # messages.success(request, "Your comment has been posted successfully")
        
    return redirect(f"/blog/{post.slug}")

def common(request):
    category = Category.objects.all()
    # posts = Post.objects.filter(cat=cat)
    post = Post.objects.filter(status=1)
    # category_title=Post.objects.filter(category=category).first()
    # recent_post=Post.objects.filter(section='Recent',status=1).order_by('-id')[0:4]
    # main_post=Post.objects.filter(Main_post=True)[0:1]
    # Editor_Pick=Post.objects.filter(section='Editors_Pick',status=1).order_by('-id')
    Trending=Post.objects.filter(section='Trending',status=1).order_by('-id')
    # Inspiration=Post.objects.filter(section='Inspiration',status=1).order_by('-id')[0:2]
    Latest_posts=Post.objects.filter(section='Latest Posts',status=1).order_by('-id')[0:4]
    Popular=Post.objects.filter(section='Popular',status=1).order_by('-id')[0:4]
    
    all_tags=Tag.objects.values('name').distinct()
    # category = Category.objects.all()

    context={
        'category':category,
        'post':post,
        # 'category_title':category_title,
        # 'recent_post':recent_post,
        # 'main_post':main_post,
        # 'Editors_Pick':Editor_Pick,
        'Trending':Trending,
        # 'Inspiration':Inspiration,
        'Latest_posts':Latest_posts,
        'Popular':Popular,
        'all_tags':all_tags,

    }
    return render(request, 'blog/common.html',context)


def section(request):
    category = Category.objects.all()
    post = Post.objects.filter(status=1)
    Latest_posts=Post.objects.filter(section='Latest Posts',status=1).order_by('-id')[0:4]
    Popular=Post.objects.filter(section='Popular',status=1).order_by('-id')[0:4]
    Pop_post=Post.objects.filter(section='Popular',status=1).order_by('-id')[0:5]
    Trend_post=Post.objects.filter(section='Trending',status=1).order_by('-id')[0:5]
    Lat_posts=Post.objects.filter(section='Latest Posts',status=1).order_by('-id')[0:5]
    
    all_tags=Tag.objects.values('name').distinct()

    # print(Post.section)

    context={
        'category':category,
        'post':post,
        'Latest_posts':Latest_posts,
        'Popular':Popular,
        'all_tags':all_tags,
        'Lat_posts':Lat_posts,
        'Trend_post':Trend_post,
        'Pop_post':Pop_post,

    }
    return render(request, 'blog/section.html',context)