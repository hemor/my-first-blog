from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm


def post_list(request):
	posts = Post.objects.filter(published_date__lte = 
		timezone.now()).order_by('-published_date')
	context = {
		'posts': posts,
	}
	return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	context = {
		'post': post,
	}
	return render(request, 'blog/post_detail.html', context)


@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('blog:post_detail', pk=post.pk)
	else:
		form = PostForm()
	context = {
		'form': form,
	}
	return render(request, 'blog/post_edit.html', context)


@login_required
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('blog:post_detail', pk=post.pk)
	else:
		form = PostForm(instance = post)
	context = {
		'form': form,
	}
	return render(request, 'blog/post_edit.html', context)


@login_required
def post_draft_list(request):
	posts = Post.objects.filter(published_date__isnull = True).order_by('-created_date')
	context = {
		'posts': posts,
	}
	return render(request, 'blog/post_draft_list.html', context)


@login_required
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('blog:post_detail', pk=pk)


@login_required
def post_delete(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('blog:post_list')