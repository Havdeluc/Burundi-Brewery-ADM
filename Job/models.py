from django.db import models
from Blog.models import _
from datetime import datetime


def offer_get_folder_name(instance, file_name):
    return f"Job Offer/{datetime.now().year}/{file_name}"


def eoi_offer_get_folder_name(instance, file_name):
    return f"Expression Of Intesert Offer/{datetime.now().year}/{file_name}"


def application_get_folder_name(instance, file_name):
    return f"Application ( Job Offer )/{datetime.now().year}/{instance.Job.Title}/{file_name}"


def expression_of_intesert_offer_get_folder_name(instance, file_name):
    return f"Expression Of Intesert ( Job Offer )/{datetime.now().year}/{file_name}"


# Create your models here.
class Offer(_):
    Title = models.CharField(max_length=1000)
    Description = models.TextField(blank=False)
    LimitDayToSubmit = models.DateField()
    Document = models.FileField(upload_to=offer_get_folder_name, null=False)
    Actif = models.BooleanField(default=True)

    CheckEmail = models.EmailField(blank=False, null=False)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"( {self.CreatedAt.date().year}/{self.CreatedAt.date().month}/{self.CreatedAt.date().day} ) {self.Title}"

    def Overview(self):
        return self.Json()

    def Json(self):
        data = super().Json()
        data.update({
            "title": self.Title,
            "description": self.Description,
            "limit_day_to_submit": self.LimitDayToSubmit,
            "document": self.Document.url
        })
        return data


class Application(_):
    Name = models.CharField(max_length=1000)
    Email = models.EmailField(max_length=1000)
    Cv = models.FileField(upload_to=application_get_folder_name)
    Job = models.ForeignKey(Offer, on_delete=models.RESTRICT)
    Actif = models.BooleanField(default=True)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.Name} ( {self.Email} )"

    def Overview(self):
        return self.Json()

    def Json(self):
        return {
            **super().Overview(),
            "name": self.Name,
            "email": self.Email,
            "cv": self.Cv.url,
            "actif": self.Actif,
            "created": self.CreatedAt
        }


class ExpressionOfIntesertOffer(_):
    Title = models.CharField(max_length=1000)
    Description = models.TextField(blank=False)
    Document = models.FileField(
        upload_to=eoi_offer_get_folder_name, null=False)
    Actif = models.BooleanField(default=True)

    CheckEmail = models.EmailField(blank=False, null=False)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"( {self.CreatedAt.date().year}/{self.CreatedAt.date().month}/{self.CreatedAt.date().day} ) {self.Title}"

    def Overview(self):
        return self.Json()

    def Json(self):
        data = super().Json()
        data.update({
            "title": self.Title, "description": self.Description, "document": self.Document.url,
            "actif": self.Actif, "created": self.CreatedAt
        })
        return data


class ExpressionOfIntesert(_):
    EOI = models.ForeignKey(ExpressionOfIntesertOffer,
                            on_delete=models.RESTRICT)
    Name = models.CharField(max_length=1000)
    Email = models.EmailField(max_length=1000)
    Document = models.FileField(
        upload_to=expression_of_intesert_offer_get_folder_name)
    Actif = models.BooleanField(default=True)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"( {self.id} ) {self.Name}"

    def Overview(self):
        return self.Json()

    def Json(self):
        return {
            **super().Overview(),
            "name": self.Name,
            "email": self.Email,
            "document": self.Document.url,
            "actif": self.Actif,
            "created": self.CreatedAt
        }


class Email(_):
    Subject = models.CharField(max_length=1000)
    Message = models.TextField()
    # AttachFile = models.FileField()
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def Json(self):
        _ = super().Overview()
        _.update({"subject": self.Subject,
                 "message": self.Message, "created": self.Created})
        return _

    def __str__(self):
        return f"( {self.CreatedAt.date().year}/{self.CreatedAt.date().month}/{self.CreatedAt.date().day} ) {self.Subject}"
