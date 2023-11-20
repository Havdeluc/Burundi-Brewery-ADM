from django.views.decorators.http import require_http_methods
from .models import Offer, Email as Message, Application, ExpressionOfIntesertOffer
from .forms import ExpressionOfIntesertForm
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.http import JsonResponse
from .signals import *
from os import getenv
from rest_framework.decorators import api_view
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
Table = {
    'offer_namespace': Offer,
    'application_namespace': Application,
    'message_namespace': Message,
    'eoi_offer': ExpressionOfIntesertOffer
}


Offset = int(getenv('OFFSET'))
Limit = int(getenv('LIMIT'))


def Home(request):
    return JsonResponse({
        "offers": [_.Overview() for _ in Offer.objects.all()[:Limit]],
        "messages": [_.Overview() for _ in Message.objects.all()[:Limit]]
    })


@csrf_exempt
@api_view(["POST"])
def WriteOne(request, ModelLabel):
    Model = Table.get(ModelLabel)
    if not Model:
        return redirect('no_such_table', model=ModelLabel)

    _ = {}
    for key, value in request.data.items():
        _[key] = value

    Obj = Model.objects.create(**_)
    return JsonResponse(Obj.Overview())


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


@csrf_exempt
@require_http_methods(["POST"])
def EOInterest(request):
    Obj = ExpressionOfIntesertForm(data=request.POST, files=request.FILES)
    if Obj.is_valid():
        Obj.save()
        return JsonResponse({'saved': True})

    print(Obj.errors)
    print(request.POST)
    print(request.FILES)
    return JsonResponse({'saved': False, "error": Obj.errors}, status=404)
