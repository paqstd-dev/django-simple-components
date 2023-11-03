from django.shortcuts import get_object_or_404, render

from .models import Category, Post


def home_view(request):
    return render(request, 'blog/home.html')


def posts_view(request):
    categories = Category.objects.all()
    posts = Post.objects.all()

    if selected_category := request.GET.get('category'):
        posts = posts.filter(categories__title=selected_category)

    return render(
        request, 'blog/posts.html', {'categories': categories, 'posts': posts}
    )


def post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    return render(request, 'blog/post.html', {'post': post})
