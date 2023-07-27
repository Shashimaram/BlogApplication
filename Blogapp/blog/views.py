from itertools import count
from django.contrib.auth.models import User
from urllib import request
from .models import Post, Comments
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView, DeleteView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, SearchForm, Postform
from django.contrib.postgres.search import SearchVector
from taggit.models import Tag
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required

# Create your views here.

# lists all the posts in the db at the limit of 8 pages per page
def post_list(request, tag_slug=None):
    posts_list = Post.published.all()
    paginator = Paginator(posts_list, 8)
    page = request.GET.get('page')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = posts_list.filter(tags_in=[tag])
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'post': posts,
                                                   'page': page,
                                                   'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    comments = post.comments.filter(active=True)
    # Pagination
    page = request.GET.get('page')
    paginator = Paginator(comments, 1)  # Show 10 comments per page
    try:
        comments_paginated = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comments_paginated = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comments_paginated = paginator.page(paginator.num_pages)
    new_comment = None

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        body = request.POST['body']

        new_comment = Comments(name=name, email=email, body=body)
        new_comment.post = post
        new_comment.save()

        response_data = {
            'message': 'Comment saved successfully.',
            'comment_id': new_comment.id,  # Include any relevant data
            'total_comments': comments.count()  # Include any relevant data
        }
        return JsonResponse(response_data)

        # mentForm(data=request.POST)
        # if comment_form.is_valid():
        #     new_comment = comment_form.save(commit=False)  # Create an unsaved model instance to further modify the instance before saving to the database
        #     new_comment.post = post
        #     new_comment.save()
        # else:
        #     # Handle the case when the form is not valid
        #     # You can choose to display an error message or handle it in a different way
        #     print(comment_form.errors)  # Print form errors for debugging purposes
    # else:
    #     # comment_form = CommentForm()
    # List of similar posts
    try:
        similar_posts = post.tags.similar_objects()

        return render(
            request,
            'blog/post/detail.html',
            {
                'post': post,
                'comments': comments_paginated,
                'new_comment': new_comment,
                # 'comment_form': comment_form,
                "similar_posts": similar_posts,
            },
        )
    except Exception:

        return render(
            request,
            'blog/post/detail.html',
            {
                'post': post,
                'comments': comments_paginated,
                'new_comment': new_comment,
                # 'comment_form': comment_form,
                # "similar_posts": similar_posts,
            },
        )
    # post_tags_ids = post.tags.values_list('id', flat=True)
    # similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id = post.id)
    # similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags','-publish')[:4]


class PostListView(ListView):
    model = Post
    template_name = 'template.html'


def Post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        # Update request.Post to request.POST
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data(query)
            results = Post.objects.annotate(search=SearchVector(
                'title', 'body'),).filter(search=query)
    return render(request, 'blog/post/search.html', {'query': query,
                                                     'results': results,
                                                     'form': form})


# def add_new_post(request):
#     form = Postform()
#     if request.method == 'POST':
#         author_ = request.user
#         body = request.POST.get('body', '')
#         tags = request.POST.get('tags', '')
#         title = request.POST.get('title', '')
        
#         new_post = Post(author=author_, body=body, tags=tags, title=title)
#         new_post.save()
#         return JsonResponse({'message': 'True'})

#     else:
#         return render(request, 'blog/post/01new_post.html')



@login_required
def add_new_post(request):
    if request.method == 'POST':
        form = Postform(request.POST)
        if form.is_valid():
            # Set the author field to the current logged-in user
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return JsonResponse({'message': 'True'})
        else:
            return JsonResponse({'message': 'False'})
    else:
        form = Postform()
    return render(request, 'blog/post/01new_post.html', {'form': form})

def checkingUserExists(request):

    users = User.objects.all()

    username = [u.username for u in users]

    if request.method == 'POST':
        name = request.POST['name']

        if name in username:
            return JsonResponse({'message': 'True'})
        else:
            return JsonResponse({'message': 'False'})
    else:
        return render(request, 'blog/post/01new_post.html')
