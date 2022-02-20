from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from .models import PostCategory
from .tasks import send_sub_mail_after_post


@receiver(m2m_changed, sender=PostCategory)
def send_sub_mail(sender, instance, action, **kwargs):
    if action == 'post_add':
        # где instance - экземпляр модели, чье отношение м2м обновляется, в нашем случае, Post.
        send_sub_mail_after_post.delay(instance.id)


