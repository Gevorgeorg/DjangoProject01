from django.db.models import QuerySet, Prefetch
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
import json

from ads.models import Ad, Category
from ads.permissions import IsOwnerOrAdmin
from ads.serializers import AdSerializer, AdCreateSerializer, AdUpdateSerializer

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Selection
from .serializers import SelectionSerializer


@csrf_exempt
def home_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return JsonResponse({"status": "ok"}, status=200)


class AdListView(ListAPIView):
    serializer_class = AdSerializer

    def get_queryset(self) -> QuerySet[Ad]:
        """Фильтры"""

        queryset: QuerySet = Ad.objects.all().select_related('category', 'author').order_by('-price')

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
    permission_classes = [IsAuthenticated]


class AdUpdateView(UpdateAPIView):
    queryset: QuerySet = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    authentication_classes = [JWTAuthentication]


class AdDeleteView(DestroyAPIView):
    queryset: QuerySet = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    authentication_classes = [JWTAuthentication]


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


class SelectionListView(ListAPIView):
    queryset = Selection.objects.all().prefetch_related('items')
    serializer_class = SelectionSerializer
    permission_classes = [AllowAny]


class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.prefetch_related(Prefetch('items',
                                                           queryset=Ad.objects.select_related(
                                                               'category', 'author')))
    serializer_class = SelectionSerializer
    permission_classes = [AllowAny]


class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    authentication_classes = [JWTAuthentication]


class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    authentication_classes = [JWTAuthentication]
