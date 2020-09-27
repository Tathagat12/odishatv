from django.contrib import admin
from .models import Post,Author,Categorie,Subscribe,Contact,Comment,Subcomment,UserDetails

# Register your models here.
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Categorie)
admin.site.register(Subscribe)
admin.site.register(Contact)
admin.site.register(Comment)
admin.site.register(Subcomment)
admin.site.register(UserDetails)

