from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

class LatestPostFeed(Feed):
     title = 'my blog'
     link = '/blog/'
     description = 'New post of by blog'
     
     def items(self):
         return Post.published.all()[:5]
     
     def item_title(self, item):
         return item.title
     
     def item_description(self, item):
         return truncatewords(item.body , 30)
         