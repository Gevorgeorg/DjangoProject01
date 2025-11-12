from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from ads.models import Ad, Category
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from settings.settings import ITEMS_PER_PAGE
from ads.serializers import AdSerializer, AdCreateSerializer, AdUpdateSerializer


@csrf_exempt
def home_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return JsonResponse({"status": "ok"}, status=200)


class AdListView(ListAPIView):
    serializer_class = AdSerializer

    def get_queryset(self) -> QuerySet[Ad]:
        """Фильтры"""

        queryset: QuerySet = Ad.objects.all().select_related('category').order_by('-price')

        category_ids: str = self.request.GET.get('cat', None)
        if category_ids:
            category_list: list = [int(cat_id) for cat_id in category_ids.split(',')]
            queryset: QuerySet = queryset.filter(category_id__in=category_list)

        search_text: str = self.request.GET.get('text')
        if search_text:
            queryset: QuerySet = queryset.filter(name__icontains=search_text)

        price_min: str = self.request.GET.get('price_min')
        if price_min:
            queryset: QuerySet = queryset.filter(price__gte=float(price_min))
        price_max: str = self.request.GET.get('price_max')
        if price_max:
            queryset: QuerySet = queryset.filter(price__lte=float(price_max))

        location_name: str = self.request.GET.get('location')
        if location_name:
            queryset: QuerySet = queryset.filter(author__location__name__icontains=location_name)

        return queryset


class AdDetailView(RetrieveAPIView):
    queryset: QuerySet = Ad.objects.all().select_related('category', 'author', 'author__location')
    serializer_class = AdSerializer


class AdCreateView(CreateAPIView):
    queryset: QuerySet = Ad.objects.all()
    serializer_class = AdCreateSerializer


class AdUpdateView(UpdateAPIView):
    queryset: QuerySet = Ad.objects.all()
    serializer_class = AdUpdateSerializer


class AdDeleteView(DestroyAPIView):
    queryset: QuerySet = Ad.objects.all()
    serializer_class = AdSerializer



@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(View):
    def post(self, request: HttpRequest, pk: int) -> JsonResponse:
        ad: Ad = get_object_or_404(Ad, id=pk)
        image_file = request.FILES['image']
        ad.image = image_file
        ad.save()

        return JsonResponse(self._ad_to_dict(ad))

    def _ad_to_dict(self, ad: Ad) -> dict:
        return {
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
            "image": ad.image.url if ad.image else None
        }


class CategoryListView(ListView):
    model: Category = Category

    def render_to_response(self, *args, **kwargs) -> JsonResponse:
        categories: QuerySet[Category] = self.get_queryset().order_by('name')
        response: list = []
        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name,
            })
        return JsonResponse(response, safe=False)


class CategoryDetailView(DetailView):
    model: Category = Category

    def render_to_response(self, *args, **kwargs):
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


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model: Category = Category
    fields: list[str] = ['name']

    def get_form_kwargs(self) -> dict:
        kwargs: dict = super().get_form_kwargs()
        if self.request.content_type == 'application/json':
            data: dict = json.loads(self.request.body)
            kwargs['data'] = data
        return kwargs

    def form_valid(self, form) -> JsonResponse:
        self.object = form.save()
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name
        })

    def form_invalid(self, form) -> JsonResponse:
        return JsonResponse(form.errors, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model: Category = Category

    def delete(self, request, *args, **kwargs) -> JsonResponse:
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"status": "ok"}, status=201)
