from urllib import request
from .models import Post, Comments
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView,TemplateView, DeleteView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm,CommentForm
# Create your views here.

def post_list(request, *args, **kwargs):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list,8)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    
    return render(request,'blog/post/list.html',{'post':posts, 'page':page})

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
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        else:
            # Handle the case when the form is not valid
            # You can choose to display an error message or handle it in a different way
            print(comment_form.errors)  # Print form errors for debugging purposes
    else:
        comment_form = CommentForm()

    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
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


