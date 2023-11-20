from django.contrib import admin
from django.forms import ModelForm, CharField
from .models import Offer, Application, ExpressionOfIntesert, ExpressionOfIntesertOffer, Email as Message
from ckeditor.widgets import CKEditorWidget


# Register your models here.


class OfferAdminForm(ModelForm):
    Description = CharField(widget=CKEditorWidget())

    class Meta:
        model = Offer
        fields = '__all__'


class OfferAdmin(admin.ModelAdmin):
    form = OfferAdminForm


admin.site.register(Offer, OfferAdmin)
admin.site.register(ExpressionOfIntesertOffer)
admin.site.register(ExpressionOfIntesert)
admin.site.register(Message)
admin.site.register(Application)
