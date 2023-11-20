from django.forms import ModelForm
from .models import ExpressionOfIntesert


class _(ModelForm):
    ...


class ExpressionOfIntesertForm(_):
    class Meta:
        model = ExpressionOfIntesert
        fields = "__all__"
