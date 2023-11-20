from django.db.models.signals import post_save
from .models import Offer, Application, ExpressionOfIntesertOffer, ExpressionOfIntesert, Email
from MailerService.App import Mailer
from django.dispatch import receiver
from Blog.models import EmailList
from os import getenv


@receiver(post_save, sender=Offer)
def new_offer_published(sender, instance, created, **kwargs):
    if created:
        Mailer.emit(
            "send_mail",
            subject="La brasserie burundaise ( Brewery ) lance une offre d'emploi.",
            attach_file=instance.Document.url,
            variables={
                "title": instance.Title,
                "description": instance.Description
            },
            emails=[x.Email for x in EmailList.objects.all()],
            template=getenv('TEMPLATE_NEW_OFFER_PUBLISHED')
        )


@receiver(post_save, sender=Application)
def new_application(sender, instance, created, **kwargs):
    if created:
        # SEND MAIL TO THE APPLICANT
        Mailer.emit(
            "send_mail",
            subject="Candidature reçu.",
            variables={"name": instance.Name},
            emails=[instance.Email],
            template=getenv("TEMPLATE_NEW_APPLICATION")
        )

        # SEND MAIL TO THE REVIEWER
        Mailer.emit(
            "send_mail",
            subject=f"Candidature Envoyé par {instance.Name}.",
            variables={
                "id": instance.id,
                "applicant": instance.Name,
                "title": instance.Job.Title,
                "offer_created": instance.Job.CreatedAt,
                "application_created": instance.CreatedAt
            },
            emails=[instance.Job.CheckEmail],
            template=getenv("TEMPLATE_APPLICATION_CHECKER")
        )


@receiver(post_save, sender=ExpressionOfIntesertOffer)
def new_eoi_offer(sender, instance, created, **kwargs):
    if created:
        Mailer.emit(
            "send_mail",
            subject="Appel d'offre public.",
            variables={"title": instance.Title,
                       "description": instance.Description},
            emails=[x.Email for x in EmailList.objects.all()],
            attach_file=instance.Document.url,
            template=getenv("TEMPLATE_NEW_EOI_PUBLISHED")
        )


@receiver(post_save, sender=ExpressionOfIntesert)
def new_eoi(sender, instance, created, **kwargs):
    if created:
        Mailer.emit(
            "send_mail",
            subject="Merci pour votre manifestation d'intérêt.",
            variables={"Name": instance.Name},
            emails=[instance.Email],
            attach_file=instance.Document.url,
            template=getenv("TEMPLATE_NEW_EOI")
        )

        Mailer.emit(
            "send_mail",
            subject=f"Réception d'une manifestation d'intérêt ( {instance.Name} )",
            emails=[instance.EOI.CheckEmail],
            attach_file=instance.Document.url,
            message="Pour plus d'informations, veuillez ouvrir le document qui vous a été envoyé en pièce jointe."
        )


@receiver(post_save, sender=Email)
def new_message_email(sender, instance, created, **kwargs):
    if created:
        Mailer.emit(
            "send_mail",
            subject=instance.Subject,
            emails=[x.Email for x in EmailList.objects.all()],
            message=instance.Message,
            # attach_file=instance.AttachFile.url
            # template=getenv("TEMPLATE_NEW_MESSAGE_BROADCAST")
        )
