from django.urls import path
from . import views
from .views import ArticleDetailView

urlpatterns = [
    path('', views.index, name='blog_index'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('search/', views.article_search_view, name='article_search'),
    path('articles/tag/<slug:tag_slug>/', views.ArticleByTags, name='articles_by_tag')
]