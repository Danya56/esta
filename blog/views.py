from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views.generic import DetailView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpRequest
from .models import Article, Tag

def index(request: HttpRequest) -> HttpResponse:
    article_list = Article.objects.filter(is_active=True).order_by('-id')

    paginator = Paginator(article_list, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context= {
        "page_obj": page_obj
    }
    return render(request, 'blog/index.html', context)

def article_search_view(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('q')
    results = Article.objects.all()

    if query:
        results = results.filter(
            Q(title__iregex=query) | Q(description__iregex=query)
        ).distinct()

    context = {
        'page_obj': results,
        'query': query
    }

    return render(request, 'blog/search_result.html', context)

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'

def ArticleByTags(request: HttpRequest, tag_slug: str) -> HttpResponse:
    tag = get_object_or_404(Tag, slug=tag_slug)
    article_list = Article.objects.filter(is_active=True, tags__slug=tag_slug).distinct()

    paginator = Paginator(article_list, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context= {
        "page_obj": page_obj,
        'current_tag': tag
    }
    return render(request, 'blog/index.html', context)