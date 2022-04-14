from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.utils.translation import gettext as _

from .models import Post, Category


@shared_task
def send_sub_mail_after_post(instance_id):
    instance = Post.objects.get(pk=instance_id)
    # print(instance)
    current_cats = instance.postCategory.all()
    # print(Category.objects.filter(post__pk=instance_id))
    subs_list = []
    cat_list = []
    for cat in current_cats:
        cat_list.append(cat.categoryName)
        subs_list.extend([user for user in cat.subscribers.all()])
    # рассылка на все категории из новости
    cat_mess = ",".join(cat_list)
    for sub_user in subs_list:
        html_content = render_to_string(
            'news/news_update_mail.html', {'user': sub_user, 'cat_mess': cat_mess, 'post': instance})
        # instance - только созданный экземпляр класса post
        msg = EmailMultiAlternatives(
            subject=_('Hi, New post category(-es){}').format(cat_mess),
            from_email='projects-mail-sf@yandex.ru',
            to=[sub_user.email]
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def send_mail_every_monday():
    for category in Category.objects.all():
        url = ''
        cat_subscribers = category.subscribers.all()
        week_news = Post.objects.filter(
            creationDate__range=[datetime.now(tz=None) - timedelta(days=7), datetime.now(tz=None)],
            postCategory=category
        )

        if week_news.exists():
            for week_new in week_news:
                url += f'{week_new.title} http://127.0.0.1:8000{week_new.get_absolute_url()}, \n'

            for subscriber in cat_subscribers:
                send_mail(
                    subject=_('Weekly news digest by category {}!').format(category.categoryName),
                    message=_('Hi {}, weekly news digest {}').format(subscriber.username, url),
                    from_email='projects-mail-sf@yandex.ru',
                    recipient_list=[subscriber.email]
                )

