from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils import timezone
from slugify import slugify
from django.urls import reverse
from django.db import transaction as _
from taggit.managers import TaggableManager
# Create your models here.


class PublishedManager(models.Manager):
    # custom Manager class Post.published.get() can be used to get published posts
    def get_queryset(self) -> QuerySet:
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=50,default=str)
    slug = models.SlugField(
        max_length=50, unique_for_date='publish', blank=True,default=str)
    author = models.ForeignKey(User, on_delete=models.CASCADE,default=str)
    body = models.TextField(max_length=200, blank=True, null=True,default=str)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='published', blank=True)
    tags = TaggableManager()
    # comment this custom manager if you want to display all blogs in admin panel
    published = PublishedManager()  # custom manager
    objects = models.Manager()  # the default manager

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)  # Use the slugify function from python-slugify
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'post'
        verbose_name_plural = "Posts"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])


class Comments(models.Model):  # comments model
    #  each post can contain multiple comments
    # one to many relationship
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    # class Meta:
    #     # db_table = 'Post_Comments'
    #     # managed = True
    #     ordering = ('created',)
    def __str__(self) -> str:
        return 'Comments by {} on {}'.format(self.name, self.post)
