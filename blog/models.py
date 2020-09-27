from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify


# Create your models here.
class UserDetails(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    mobile=models.CharField(max_length= 10,null=True)
    image=models.ImageField(upload_to='profile_pics', null=True, default='p1.jpg')




class Subscribe(models.Model):
    email=models.EmailField()
class Author(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE)
    rate=models.IntegerField(default=0)
    def __str__(self):
        return f'{self.user}'

class Categorie(models.Model):
    title=models.CharField(max_length=20)
    def __str__(self):
        return self.title


class Post(models.Model):
    title=models.CharField(max_length=50)
    overview=models.TextField()
    slug = models.SlugField(null=True, blank=True)
    body_text = RichTextUploadingField(null=True)
    time_uplode=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    thumbnail=models.ImageField(upload_to='thumbnail')
    publish=models.BooleanField()
    categorie=models.ManyToManyField(Categorie)
    read=models.IntegerField(default=0)

    class Meta:
        ordering=['-pk']

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs) 


class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    mob=models.CharField(max_length=12)
    mess=models.TextField()
    time=models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    time=models.DateTimeField(auto_now_add=True)
    comm=models.TextField()  



class Subcomment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    time=models.DateTimeField(auto_now_add=True)
    comm=models.TextField()
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE)      

