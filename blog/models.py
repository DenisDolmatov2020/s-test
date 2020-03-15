from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_blog(sender, instance=None, created=False, **kwargs):
    if created:
        Blog.objects.create(user=instance)


class Blog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='is_following', blank=True)

    def __str__(self):
        return self.user.username


class Article(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    text = models.TextField(max_length=160)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title


@receiver(post_save, sender=Article)
def send_remind(sender, instance=None, created=False, **kwargs):
    if created:
        blog = Blog.objects.get(id=instance.blog.id)
        followers_mail = list()
        for follower in blog.followers.all():
            print(follower.email)
            if follower.email != '':
                followers_mail.append(follower.email)
        title_email = "В блоге %s новая статья на тему %s" % (blog.user.username, instance.title)
        body_email = 'ссылка на статью http://127.0.0.1:8000/article-list/%s' % instance.id
        send_mail(title_email, body_email, 'denisdolmatov2020@yandex.ru', followers_mail, fail_silently=False)


class ReadArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, db_index=False)

    class Meta:
        unique_together = ('user', 'article')

    def __str__(self):
        return self.article.title
