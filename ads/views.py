from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json
from ads.models import Ad, Category
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from DjangoProject.settings import ITEMS_PER_PAGE


@csrf_exempt
def home_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdView(View):

    def get(self, request: HttpRequest, pk: int = None) -> JsonResponse:
        if pk:
            ad: Ad = get_object_or_404(Ad, id=pk)
            return JsonResponse(self._add_to_dict(ad))

        else:
            page_number: int = int(request.GET.get('page', 1))
            ads_list = Ad.objects.all().order_by('-price')
            paginator = Paginator(ads_list, ITEMS_PER_PAGE)
            page_obj = paginator.get_page(page_number)

            return JsonResponse({
                "items": [self._add_to_dict(ad) for ad in page_obj],
                "total": paginator.count,
                "num_pages": paginator.num_pages,
            }, status=200)

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            data: dict = json.loads(request.body)
            ad: Ad = Ad(**{k: v for k, v in data.items() if
                           k in ['name', 'author', 'price', 'description', 'address', 'is_published']})
            ad.full_clean()
            ad.save()
            return JsonResponse(self._add_to_dict(ad), status=201)
        except (ValidationError, KeyError) as e:
            return JsonResponse({"error": str(e)}, status=422)

    def patch(self, request: HttpRequest, pk: int) -> JsonResponse:
        try:
            ad: Ad = get_object_or_404(Ad, id=pk)
            data: dict = json.loads(request.body)

            for field in ['name', 'author', 'price', 'description', 'address', 'is_published']:
                if field in data:
                    setattr(ad, field, data[field])

            ad.full_clean()
            ad.save()
            return JsonResponse(self._add_to_dict(ad))
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=422)

    def delete(self, request: HttpRequest, pk: int) -> JsonResponse:
        ad: Ad = get_object_or_404(Ad, id=pk)
        ad.delete()
        return JsonResponse({"status": "ok"})

    def _add_to_dict(self, ad: Ad) -> dict:
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
            "image": ad.image.url if ad.image else None  # URL изображения
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
