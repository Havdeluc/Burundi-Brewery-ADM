from django.contrib import admin
from django import forms
from Blog.models import (
    BlogCategory, Blog, Comment, EmailList,
    GroupImage, Image, Agence,
    Product, ProductImage, Member,
    CoverImage

)
from ckeditor.widgets import CKEditorWidget


# Register your models here.


class BlogAdminForm(forms.ModelForm):
    Description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blog
        fields = '__all__'


class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm


admin.site.register(BlogCategory)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)
admin.site.register(EmailList)

admin.site.register(GroupImage)
admin.site.register(Image)
admin.site.register(Agence)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Member)
admin.site.register(CoverImage)
