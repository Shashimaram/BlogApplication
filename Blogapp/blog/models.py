from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils import timezone
from slugify import slugify
# Create your models here.


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )
    
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length = 50,unique_for_date= 'publish',blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=200, blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES, default='draft')
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post,self).save()
        
        
    class Meta:
        ordering = ('-publish',)
    def __str__(self) -> str:
        return self.title
    
    
    
    
    


