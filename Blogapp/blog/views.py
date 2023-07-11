from urllib import request
from .models import Post 
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView,TemplateView, DeleteView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm,Comment_Form
# Create your views here.

def post_list(request, *args, **kwargs):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list,4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    
    return render(request,'blog/post/list.html',{'post':posts, 'page':page})


def post_detail(request, year, month,day, post):
    post = get_object_or_404(Post,slug = post,
                            #  status = 'published',
                             publish__year = year,
                             publish__month = month,
                             publish__day = day,)
    
    # list all the comments for this post
    comments = post.comments.filter(active = True)
    
    new_comments = None
    
    # if new comment posted
    if request.method == 'POST':
        
        form = Comment_Form(request.POST)
        # create an objetc to store the form
        new_comments = Comment_Form.save(form)
        # add post to the comment
        new_comments.post  = post
        #save the comment to db
        new_comments.save()
    
    else:
        form = Comment_Form()
    
    
    return render(request,'blog/post/detail.html',{'post':post,
                                                   'comments':comments,
                                                   'new_comments':new_comments,
                                                   'comment_form':form})

class PostListView(ListView):
    model = Post
    template_name = 'template.html'
    
def Post_share(request, post_id):
    post = get_object_or_404(Post,id = post_id)
    if request.method == 'POST':
        form = EmailPostForm(request.Post)
        if form.is_valid():
            cd=form.cleaned_data
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html' ,{'post':post,'form':form})

