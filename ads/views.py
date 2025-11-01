from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json
from ads.models import Ads, Category
from django.views.generic import ListView, DetailView, CreateView


@csrf_exempt
def home_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        ads = Ads.objects.all()
        response: list[dict] = []
        for ad in ads:
            response.append({
                'id': ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
            })

        return JsonResponse(response, safe=False)

    def post(self, request: HttpRequest) -> JsonResponse:
        ad_data: dict = json.loads(request.body)
        ad: Ads = Ads.objects.create(
            name=ad_data["name"],
            author=ad_data["author"],
            price=ad_data["price"],
            description=ad_data["description"],
            address=ad_data["address"],
            is_published=ad_data["is_published"]
        )

        try:
            ad.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdEntityView(View):
    def get(self, request: HttpRequest, pk: int) -> JsonResponse:
        ad: Ads = get_object_or_404(Ads, id=pk)

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
        })


class CategoryListView(ListView):
    model: Category = Category

    def render_to_response(self, context: dict) -> JsonResponse:
        categories: QuerySet[Category] = self.get_queryset()
        response: [dict] = []
        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name,
            })
        return JsonResponse(response, safe=False)


class CategoryDetailView(DetailView):
    model: Category = Category

    def render_to_response(self, context):
        category: Category = self.object
        return JsonResponse({
            "id": category.id,
            "name": category.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model: Category = Category
    fields: list[str] = ['name']

    def get_form_kwargs(self) -> dict:
        kwargs: dict = super().get_form_kwargs()
        if self.request.content_type == 'application/json':
            data: dict = json.loads(self.request.body)
            kwargs['data'] = data
        return kwargs

    def form_valid(self, form) -> JsonResponse:
        self.object: Category = form.save()
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name
        }, status=201)

    def form_invalid(self, form) -> JsonResponse:
        return JsonResponse(form.errors, status=400)
