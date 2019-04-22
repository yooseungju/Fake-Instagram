from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Post, Image, Comment, Hashtag
from .forms import PostForm, ImageForm, CommentForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def list(request):
    posts = Post.objects.all().order_by('-pk')
    # posts = Post.objects.filter(user__in = request.user.followings.all()).order_by('-pk')
    comment_form = CommentForm()
    context = {
        'posts':posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/list.html', context)

@login_required
def create(request):
    if request.method == "POST":
    
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            # hashtag
            # 1. 게시갈을 순회하면서 띄어쓰기를 잘라야함
            # 2. 자른단어가 #으로 시작하나?
            # 3. 해시태그된 단어가 기존 해시태그단어에 있는건지
            
            list_content = post.content.split()
        
            for word in list_content:
                if word[0]=='#':
                    hashtag = Hashtag.objects.get_or_create(content=word)
                    post.hashtags.add(hashtag[0])
                        
            
            for image in request.FILES.getlist('file'):
                request.FILES['file'] = image
                image_form = ImageForm(files=request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.post = post
                    image.save()
                    
                    
            return redirect('posts:list')
    else:
        post_form = PostForm()
        image_form = ImageForm()
    context = {
        'post_form': post_form,
        'image_form': image_form,
    }
    return render(request, 'posts/form.html', context)
@login_required   
def update(request, post_pk):
    post = get_object_or_404(Post, id=post_pk)
    if request.method == "POST":
        
        post_form = PostForm(instance=post,data=request.POST)
        if post_form.is_valid():
            post_form.save()
            
            post.hashtags.clear()
            list_content = post.content.split()
            for word in list_content:
                if word[0]=='#':
                    hashtag = Hashtag.objects.get_or_create(content=word)
                    post.hashtags.add(hashtag[0])
            
            return redirect('posts:list')
    else:
        post_form = PostForm(instance=post)
        
    context = {'post_form':post_form,'post':post,}
    return render(request, 'posts/form.html', context)
        
    
@login_required      
def delete(request, post_pk):
    
    post = get_object_or_404(Post, pk=post_pk)
    if post.user == request.user:
        if request.method == 'POST':
            post.delete()
        return redirect('posts:list')
    else:
        return redirect('posts:list')
        
        
@login_required
@require_POST    
def comment_create(request, post_pk):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment =  comment_form.save(commit=False)
        comment.post_id = post_pk
        comment.user = request.user
        comment.save()
    return redirect('posts:list')
        
   
@login_required
@require_POST      
def comment_delete(request, comment_pk):
    if request.method == "POST":
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
        return redirect('posts:list')
    else:
        return redirect('posts:list')
        
        
@login_required
def like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
        
    else:
        post.like_users.add(request.user)
    return redirect('posts:list')


def hashtag(request, hash_pk):
    hashtag = get_object_or_404(Hashtag,pk=hash_pk)
    posts = hashtag.post_set.order_by('-pk')
    
    context = {
        'hashtag': hashtag,
        'posts' :posts
    }
    return render(request, 'posts/hashtag.html', context)
    
    
