from django.contrib.auth.models import User
from django.db.models import F
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from blog.models import Blog, Article, ReadArticle


class ArticleList(ListView):
    model = Article


class ArticleDetail(DetailView):
    model = Article


class ArticleUser(ListView):
    template_name = 'blog/article_user.html'

    def get_queryset(self):
        articles = Article.objects.filter(blog__followers__id=self.request.user.id).order_by('-date')
        return articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        read_articles = ReadArticle.objects.select_related('article').filter(user=self.request.user)
        r_articles = list()
        for r in read_articles:
            r_articles.append(r.article.id)
        context['read_articles'] = r_articles
        return context


class SubscribeBlog(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        blog = Blog.objects.get(id=kwargs['pk'])
        follower = User.objects.get(id=request.user.id)
        if follower in blog.followers.all():
            blog.followers.remove(follower)
            r = ReadArticle.objects.filter(article__blog__id=kwargs['pk'], user=follower).delete()
            print(r)
        else:
            blog.followers.add(follower)
        return HttpResponseRedirect(reverse('article-user'))


class ReadArticleView(View):
    def get(self, request, *args, **kwargs):
        ReadArticle.objects.get_or_create(article_id=kwargs['pk'], user=self.request.user)
        return HttpResponseRedirect(reverse('article-user'))
'''
    class ArticleUser(ListView):
        template_name = 'blog/article_user.html'

        def get_queryset(self):
            articles = Article.objects.filter(blog__followers__id=self.request.user.id).order_by('-date')
            read_articles = list(ReadArticle.objects.filter(user=self.request.user).values_list('article'))
            print(read_articles)
            r = list()
            for a in read_articles:
                r.append(a[0])
            print(r)
            # print(read_art) .annotate(read_article_id=F('article__id'))
            for a in articles:
                # print(type(a.read_article_id))
                print(a.id in read_articles)

            return articles'''