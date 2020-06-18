from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

def redirect_view(request):
    return redirect('post_list')

def post_list(request):
    meta = {"is_logged_in":request.user.is_authenticated}
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts':posts, 'meta':meta})

def post_detail(request, pk):
    meta = {"is_logged_in":request.user.is_authenticated}
    user = request.user
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post, 'meta':meta, 'user':user})

def post_new(request):
    meta = {"is_logged_in":request.user.is_authenticated}
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form':form, 'meta':meta})

def post_edit(request, pk):
    meta = {"is_logged_in":request.user.is_authenticated}
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('post_detail', pk=post.pk)
    elif request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form, 'meta':meta})
