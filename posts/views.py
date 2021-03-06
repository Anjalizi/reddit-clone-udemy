from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Post

@login_required
def create(request):
	if request.method=='POST':
		# title, url required, author, pub_date taken care of, vote by default
		if request.POST['title'] and request.POST['url']:
			post = Post()
			post.title = request.POST['title']
			if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
				post.url = request.POST['url']
			else:
				post.url = 'http://' + request.POST['url']
			post.pub_date = timezone.datetime.now()
			post.author = request.user #to get current logged in user
			post.save()
			return redirect('home') # home is the name of the page (as specified in urls.py)
		else:
			return render(request, 'posts/create.html', {'error': 'ERROR: must include a title and url both'})	
	else:
		return render(request, 'posts/create.html')

def home(request):
	# for decreasing order put '-' sign
	posts = Post.objects.order_by('-votes_total')
	return render(request, 'posts/home.html', {'posts':posts})

def userposts(request, fk):
	posts = Post.objects.filter(author__id=fk).order_by('-votes_total')
	author = User.objects.get(pk=fk)
	return render(request, 'posts/userposts.html', {'posts':posts, 'author':author})

def upvote(request, pk):
	# if the method is GET, changes occur as soon as the url is typed, not even entered
	if request.method == 'POST':
		post = Post.objects.get(pk=pk)
		post.votes_total += 1
		post.save()
		return redirect('home')

def downvote(request, pk):
	if request.method == 'POST':
		post = Post.objects.get(pk=pk)
		post.votes_total -= 1
		post.save()
		return redirect('home')
