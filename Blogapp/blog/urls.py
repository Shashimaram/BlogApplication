from . import views
from django.urls import path
from django.urls import include
from .feeds import LatestPostFeed
app_name='blog'

urlpatterns = [
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag_name'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('', views.post_list, name='post_list'),
    path('feed/',LatestPostFeed(),name = 'post_feed'),
    path('search/',views.post_search, name = 'search_url'),
]
