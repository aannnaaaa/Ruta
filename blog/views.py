from django.shortcuts import render, get_object_or_404
from .models import Post

def blog_page(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/blog_page.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.views += 1  # Увеличиваем счётчик просмотров
    post.save()
    return render(request, 'blog/post_detail.html', {'post': post})