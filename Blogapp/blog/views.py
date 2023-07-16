from itertools import count
from urllib import request
from .models import Post, Comments
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView,TemplateView, DeleteView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm,CommentForm,SearchForm
from django.contrib.postgres.search import SearchVector
from taggit.models import Tag


# Create your views here.

def post_list(request,tag_slug = None):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list,8)
    page = request.GET.get('page')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = posts_list.filter(tags_in = [tag])
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    
    return render(request,'blog/post/list.html',{'post':posts, 
                                                'page':page,
                                                'tag':tag})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    comments = post.comments.filter(active=True)   
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)  # Create an unsaved model instance to further modify the instance before saving to the database
            new_comment.post = post
            new_comment.save()
        else:
            # Handle the case when the form is not valid
            # You can choose to display an error message or handle it in a different way
            print(comment_form.errors)  # Print form errors for debugging purposes
    else:
        comment_form = CommentForm()
    # List of similar posts
    similar_posts = post.tags.similar_objects()
    # post_tags_ids = post.tags.values_list('id', flat=True)
    # similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id = post.id)
    # similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
            "similar_posts": similar_posts,
        },
    )
class PostListView(ListView):
    model = Post
    template_name = 'template.html'
    
def Post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = EmailPostForm(request.POST)  # Update request.Post to request.POST
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})

def post_search(request):
    form=SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data(query)
            results=  Post.objects.annotate(search = SearchVector('title','body'),).filter(search = query)
    return render(request, 'blog/post/search.html',{'query':query,
                                                'results':results,
                                                'form': form})