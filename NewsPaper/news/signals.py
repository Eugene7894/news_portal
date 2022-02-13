from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.template.loader import render_to_string
from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def send_sub_mail(sender, instance, action, **kwargs):
    if action == 'post_add':
        # print(instance)
        current_cats = instance.postCategory.all()
        # print(Category.objects.filter(post__pk=instance.id))
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
                subject=f'Здравствуй, Новая статья из категории(-ий){cat_mess}',
                from_email='projects-mail-sf@yandex.ru',
                to=[sub_user.email]
            )

            msg.attach_alternative(html_content, 'text/html')
            msg.send()

