from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.utils.timezone import now


# richtexteditor
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=200)
    
    url = models.CharField(max_length=100, default='SOME STRING') 


    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS=(
        ('0','Draft'),
        ('1','Publish'),
    )

    SECTION=(
        ('Popular','Popular'),
        ('Trending','Trending'),
        ('Latest Posts','Latest Posts'),
    )

    # sno=models.AutoField(primary_key=True)
    featured_image=models.ImageField(upload_to='Images')
    title =models.CharField(max_length=200)
    author =models.CharField(max_length=50)
    description = models.CharField(max_length=300,default=" ")
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    # date =models.DateField(auto_now_add=True)
    content =RichTextField()
    # content = models.TextField()
    slug=models.SlugField(max_length=500,null=True,blank=True,unique=True)
    status=models.CharField(choices=STATUS,max_length=100)
    section=models.CharField(choices=SECTION,max_length=200)
    url = models.CharField(max_length=100, default=' ') 
    timeStamp=models.DateTimeField(blank=True)
    Main_post=models.BooleanField(default=False)
    post_views=models.IntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return self.title

def create_slug(instance,new_slug=None):
    slug=slugify(instance.title)
    if new_slug is not None:
        slug =new_slug
    qs=Post.objects.filter(slug=slug).order_by('-id')
    exists=qs.exists()
    if exists:
        new_slug="%s-%s"%(slug,qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug


def pre_save_post_reciver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=create_slug(instance)

    pre_save.connect(pre_save_post_reciver,Post)



class Tag(models.Model):
    name=models.CharField(max_length=100)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# comments
class BlogComment(models.Model):
    sno= models.AutoField(primary_key=True)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)


    def __str__(self):
        return self.comment