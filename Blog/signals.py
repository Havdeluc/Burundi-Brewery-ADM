from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Blog, EmailList
from MailerService.App import Mailer
from os import getenv


@receiver(post_save, sender=Blog)
def new_blog_post_published(sender, instance, created, **kwargs):
    if created:
        Mailer.emit(
            "send_mail",
            subject="Un nouvel article a été publié sur notre blog.",
            variables={
                "title": instance.Title, "overview": instance.OverView,
                "image": instance.Cover.url, "link": f"{getenv('BLOG_POST_URL')}{instance.id}"
            },
            emails=[x.Email for x in EmailList.objects.all()],
            template=getenv("TEMPLATE_NEW_BLOG_POST_PUBLISHED")
        )


@receiver(post_save, sender=EmailList)
def new_email_subscribed(sender, instance, created, **kwargs):
    if created:
        Mailer.emit(
            "send_mail",
            subject="Merci de vous etre abonné à notre newsletter.",
            emails=[instance.Email],
            template=getenv("TEMPLATE_EMAIL_SUBSCRIBED")
        )
