from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post
from django.conf import settings


# Паджинация
def pagination(queryset, request):
    paginator = Paginator(queryset, settings.PAGE_LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {'paginator': paginator,
            'page_number': page_number,
            'page_obj': page_obj,
            }


# Главная страница
def index(request):
    context = pagination(Post.objects.all(), request)
    return render(request, 'posts/index.html', context)


# Страница группы
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    context = pagination(group.posts.all(), request)
    context['group'] = group
    return render(request, 'posts/group_list.html', context)


# Страница профиля пользователя
def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts_count = author.posts.count()
    username = author.username
    context = pagination(author.posts.all(), request)
    context['author'] = author
    context['posts_count'] = posts_count
    context['username'] = username
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post_card = get_object_or_404(Post, pk=post_id)
    posts_count = post_card.author.posts.count()
    context = {
        'post_card': post_card,
        'posts_count': posts_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            user = request.user
            post = form.save(commit=False)
            post.author = user
            post.save()
            return redirect('posts:profile', username=request.user.username)
    context = {'form': form, }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id: int):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post)
    user = request.user

    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)

    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)

    context = {
        'form': form,
        'post': post,
        'user': user,
    }
    return render(request, 'posts/create_post.html', context)
