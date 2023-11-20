from django.forms import ModelForm
from .models import Comment, EmailList


class _(ModelForm):
    ...


class CommentForm(_):
    class Meta:
        model = Comment
        fields = "__all__"
        # exclude = ("id", )


class EmailListForm(_):
    class Meta:
        model = EmailList
        fields = ("Email", )
