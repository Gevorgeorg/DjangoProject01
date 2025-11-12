from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json


from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad
from users.models import User, Location

from DjangoProject.settings import ITEMS_PER_PAGE
from .serializers import UserSerializer, LocationSerializer


class UserListView(ListAPIView):
    queryset = User.objects.all().select_related('location')
    serializer_class = UserSerializer




class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


@method_decorator(csrf_exempt, name='dispatch')
class LocationView(View):
    def get(self, request: HttpRequest, pk: int = None) -> JsonResponse:
        if pk:
            location = get_object_or_404(Location, id=pk)
            return JsonResponse(self._add_to_dict(location))
        else:
            locations_list = Location.objects.all()
            locations_data = [self._add_to_dict(location) for location in locations_list]
            return JsonResponse(locations_data, safe=False)

    def post(self, request: HttpRequest) -> JsonResponse:

        data: dict = json.loads(request.body)
        location: Location = Location(**{key: val for key, val in data.items() if
                                         key in ['name', 'lat', 'lng']})
        location.full_clean()
        location.save()

        return JsonResponse(self._add_to_dict(location), status=201)

    def patch(self, request: HttpRequest, pk: int) -> JsonResponse:

        location: Location = get_object_or_404(Location, id=pk)
        data: dict = json.loads(request.body)

        for field in ['name', 'lat', 'lng']:
            if field in data:
                setattr(location, field, data[field])

        location.full_clean()
        location.save()
        return JsonResponse(self._add_to_dict(location))

    def delete(self, request: HttpRequest, pk: int) -> JsonResponse:
        location: Location = get_object_or_404(Location, id=pk)
        location.delete()
        return JsonResponse({"status": "ok"})

    def _add_to_dict(self, location: Location) -> dict:
        return {
            "id": location.id,
            "name": location.name,
            "lat": location.lat,
            "lng": location.lng,
        }
