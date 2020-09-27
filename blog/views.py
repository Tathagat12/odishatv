from django.shortcuts import render,redirect
from .models import Post,Author,Subscribe,Contact,Comment,Subcomment,UserDetails
import datetime
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    if request.method =='GET':
        email=request.GET.get('email')
        if email:
            Subscribe(email=email).save()

            
    week_ago=datetime.date.today() - datetime.timedelta(days=7)
    tends=Post.objects.filter(time_uplode__gte= week_ago).order_by('-read')
    TopAuthor=Author.objects.order_by('-rate')[:4]
    AuthorsPost=[Post.objects.filter(author=author).first() for author in TopAuthor]
    all_post =Paginator(Post.objects.filter(publish=True),3)
    page=request.GET.get('page')
    try:
        posts=all_post.page(page)
    except PageNotAnInteger:
        posts=all_post.page(1)
    except EmptyPage:
        posts=all_post.page(all_post.num_pages)   
        
    parms={
        'posts':posts,
        'trends':tends[:5],
        'author_post':AuthorsPost,
        'pop_post':Post.objects.order_by('-read')[:7],
    }

    return render(request,'index.html',parms)

@login_required
def profile(request):
    return render(request,'profile.html')  


def about(request):
    week_ago=datetime.date.today() - datetime.timedelta(days=7)
    tends=Post.objects.filter(time_uplode__gte= week_ago).order_by('-read')
    TopAuthor=Author.objects.order_by('-rate')[:4]
    AuthorsPost=[Post.objects.filter(author=author).first() for author in TopAuthor]
    parms ={
        'trends':tends[:5],
        'author_post':AuthorsPost,
        'title': 'About | Odisha Television Ltd'
    }
    return render(request, 'about.html',parms) 

def contact(request):
	if request.method =='POST':
		name = f"{request.POST.get('fname')} {request.POST.get('lname')}"
		email = request.POST.get('email')
		mob = request.POST.get('mob')
		mess = request.POST.get('mess','default')
		Contact(name=name,email=email,mob=mob,mess=mess).save()
	return render(request, 'contact.html')
        


def categories(request):
    if request.method =='GET':
        email=request.GET.get('email')
        if email:
            Subscribe(email=email).save()
    
    parms ={
        'title':  'Post in | Odisha Television Ltd'
    }
    return render(request, 'categories.html',parms)

def post(request, id, slug):
	try:
		post = Post.objects.get(pk=id, slug=slug)
	except:
		raise Http404("Post Does Not Exist")	

	post.read+=1
	post.save()

	if request.method == 'POST':
		comm = request.POST.get('comm')
		comm_id = request.POST.get('comm_id') #None

		if comm_id:
			Subcomment(post=post,
					user = request.user,
					comm = comm,
					comment = Comment.objects.get(id=int(comm_id))
				).save()
		else:
			Comment(post=post, user=request.user, comm=comm).save()


	comments = []
	for c in Comment.objects.filter(post=post):
		comments.append([c, Subcomment.objects.filter(comment=c)])
	parms = {
		'comments':comments,
		'post':post,
		'pop_post': Post.objects.order_by('-read')[:7],
		}
	return render(request, 'blog-single.html', parms)

def search(request):
    if request.method =='GET':
        email=request.GET.get('email')
        if email:
            Subscribe(email=email).save()
    
    q=request.GET.get('q')
    posts=Post.objects.filter(Q(title__icontains= q)|Q(overview__icontains= q)).distinct()
    parms={
        'posts':posts,
        'title':f'Search Results for {q}',
        'pop_post':Post.objects.order_by('-read')[:7],
        }    
        
    return render(request,'categories.html',parms)   

def view_all(request,query):
    if request.method =='GET':
        email=request.GET.get('email')
        if email:
            Subscribe(email=email).save()
            
    week_ago=datetime.date.today() - datetime.timedelta(days=7)
    acpt=['trending','popular']
    q=query.lower() 
    if q in acpt:
        if q== acpt[0]:
            all_post =Paginator(Post.objects.filter(time_uplode__gte= week_ago),4)
            page=request.GET.get('page')
            try:
                posts=all_post.page(page)
            except PageNotAnInteger:
                posts=all_post.page(1)
            except EmptyPage:
                posts=all_post.page(all_post.num_pages).order_by('-read') 
            
            parms={
            'posts':posts,
            'title':"Trending News",
            'pop_post':Post.objects.order_by('-read')[:7],
            } 
        elif q==acpt[1]:
            all_post =Paginator(Post.objects.order_by('-read'),4)
            page=request.GET.get('page')
            try:
                posts=all_post.page(page)
            except PageNotAnInteger:
                posts=all_post.page(1)
            except EmptyPage:
                posts=all_post.page(all_post.num_pages)
            parms={
            'posts':posts,
            'title':"Popular News",
            'pop_post':Post.objects.order_by('-read')[:7],
            }
        else:
            pass   

    return render(request,'categories.html',parms)      
                  



      

