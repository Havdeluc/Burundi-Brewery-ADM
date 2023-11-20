from .models import (
    BlogCategory, Blog, Comment, EmailList,
    GroupImage, Agence, Product, Member,
    CoverImage
)
from rest_framework.decorators import api_view
from .forms import EmailListForm, CommentForm
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.http import JsonResponse
from os import getenv
from .signals import *


# Create your views here.
Table = {
    'blogcategory_namespace': BlogCategory,
    'blog_namespace': Blog,
    'comment_namespace': Comment,
    'newsletter_namespace': EmailList,
    'agence_namespace': Agence
}


Offset = int(getenv('OFFSET'))
Limit = int(getenv('LIMIT'))


def NoSuchTable(request, model):
    return JsonResponse({'no_table': model}, status=400)


def NoSuchObject(request):
    return JsonResponse({'no_object': True}, status=400)


def Home(request):
    return JsonResponse({
        "category_blog": [_.Overview() for _ in BlogCategory.objects.all()],
        "blog": [_.Overview() for _ in Blog.objects.all()[:Limit]],
    })


def HomeWebsite(request):
    return JsonResponse({
        "group_image": [_.Json() for _ in GroupImage.objects.all()],
        "cover": [_.Json() for _ in CoverImage.objects.all()],
        "product": [_.Json() for _ in Product.objects.all()],
        "member": [_.Json() for _ in Member.objects.all()]
    })


def FindOne(request, ModelLabel, pk):
    Model = Table.get(ModelLabel)
    if not Model:
        return redirect('no_such_table', model=ModelLabel)

    if (Object := Model.objects.get(pk=pk)):
        _ = Object.Json() if request.GET.dict().get('more') else Object.Overview()
        return JsonResponse(_)
    return redirect('no_such_object')


def FindMany(request, ModelLabel):
    Model = Table.get(ModelLabel)
    if not Model:
        return redirect('no_such_table', model=ModelLabel)

    # META QUERY
    QueryParams = request.GET.dict().copy()
    QueryParams.pop("limit", 0)
    QueryParams.pop("page", 0)
    QueryParams.pop("more", 0)

    # DATABASE QUERY
    Query = Model.objects.filter(**QueryParams).order_by("-id")
    paginator = Paginator(Query, request.GET.get('limit', Limit))

    # PAGINATION
    CurrentPage = paginator.get_page(request.GET.get('page', 1))

    # FORMAT DATA
    _ = [
        _.Json()
        if request.GET.get('more')
        else _.Overview()
        for _ in CurrentPage.object_list
    ]

    # RESPONSE TO THE USER
    return JsonResponse({
        "page": paginator.num_pages,
        "next": CurrentPage.has_next() and CurrentPage.next_page_number(),
        "previous": CurrentPage.has_previous() and CurrentPage.previous_page_number(),
        "data": _
    })


@api_view(["POST"])
def AddComment(request, pk):
    Obj = CommentForm(request.data)
    if not Obj.is_valid():
        errors = []
        for field_name, field_message in Obj.errors.items():
            errors.append({'name': field_name, 'message': field_message})
        return JsonResponse({'errors': errors}, status=400)

    if (_ := Blog.objects.get(pk=pk)):
        Obj = Obj.save()
        _.Comment.add(Obj)
        return JsonResponse(Obj.Overview())

    return redirect('no_such_object')


@api_view(["GET"])
def Search(request):
    query = request.GET.get("query", "")
    column = "TitleEn" if str(request.GET.get("lang")) == "en" else "TitleFr"

    try:
        Query = Blog.objects.raw(f"""
            SELECT * FROM "Blog_blog" WHERE levenshtein("Blog_blog"."{column}", '{query}') <= 20 ORDER BY id DESC;
        """)
        print(Query[0])
    except Exception as error:
        print(error)
        Query = Blog.objects.all().order_by("-View")

    paginator = Paginator(Query, request.GET.get('limit', Limit))
    CurrentPage = paginator.get_page(request.GET.get('page', 1))
    _ = [
        _.Json()
        if request.GET.get('more')
        else _.Overview()
        for _ in CurrentPage.object_list
    ]
    return JsonResponse({
        "page": paginator.num_pages,
        "next": CurrentPage.has_next() and CurrentPage.next_page_number(),
        "previous": CurrentPage.has_previous() and CurrentPage.previous_page_number(),
        "data": _
    })


@api_view(["POST"])
def SubscribeToNewLetter(request):
    Obj = EmailListForm(request.data)

    if (Obj.is_valid()):
        return JsonResponse(Obj.save().Json())

    errors = []
    for field_name, field_message in Obj.errors.items():
        errors.append({'name': field_name, 'message': field_message})
    return JsonResponse({'errors': errors}, status=400)


@api_view(["GET"])
def UnSubscribeToNewLetter(request, pk, email):
    EmailList.objects.delete(pk=pk, Email=email)
    return JsonResponse({"deleted": True})


@api_view(["POST"])
def ContactUs(request):
    Mailer.emit(
        "send_mail",
        subject=f"Un message Envoyé Par: {request.data.get('Name')}",
        emails=[getenv("COMPANY_EMAIL")],
        variables={
            "name": request.data.get("Name"),
            "email": request.data.get("Email"),
            "message": request.data.get("Message")
        },
        # attach_file=instance.AttachFile.url
        template=getenv("TEMPLATE_CONTACT_US")
    )
    return JsonResponse({'task': True})
