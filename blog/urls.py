from django.contrib import admin
from django.urls import path, include

from blog.views import ArticleList, ArticleUser, ArticleDetail, SubscribeBlog, ReadArticleView

urlpatterns = [
    path('article-list/', ArticleList.as_view(), name='article-list'),
    path('article-list/<int:pk>/', ArticleDetail.as_view(), name='article-detail'),
    path('article-user/', ArticleUser.as_view(), name='article-user'),
    path('subscribe/<int:pk>/', SubscribeBlog.as_view(), name='subscribe_blog'),
    path('read/<int:pk>/', ReadArticleView.as_view(), name='read_article_view'),
]