from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json


from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from ads.models import Ad
from users.models import User, Location

from DjangoProject.settings import ITEMS_PER_PAGE
from .serializers import UserSerializer


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



@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):

    def get(self, request: HttpRequest, pk: int = None) -> JsonResponse:
        if pk:
            user: User = get_object_or_404(User, id=pk)
            return JsonResponse(self._add_to_dict(user))
        else:

            page_number: int = int(request.GET.get('page', 1))
            users_list = User.objects.all().select_related('location')
            paginator = Paginator(users_list, ITEMS_PER_PAGE)
            page_obj = paginator.get_page(page_number)

            return JsonResponse({
                "items": [self._add_to_dict(user) for user in page_obj],
                "total": paginator.count,
                "num_pages": paginator.num_pages,
            }, status=200)

    def post(self, request: HttpRequest) -> JsonResponse:

        data: dict = json.loads(request.body)
        user: User = User(**{key: val for key, val in data.items() if
                             key in ['first_name', 'last_name', 'username', 'password', 'role', 'age']})
        user.full_clean()
        user.save()
        return JsonResponse(self._add_to_dict(user), status=201)

    def patch(self, request: HttpRequest, pk: int) -> JsonResponse:

        user: User = get_object_or_404(User, id=pk)
        data: dict = json.loads(request.body)

        for field in ['first_name', 'last_name', 'username', 'password', 'role', 'age']:
            if field in data:
                setattr(user, field, data[field])

        user.full_clean()
        user.save()
        return JsonResponse(self._add_to_dict(user), status=200)

    def delete(self, request: HttpRequest, pk: int) -> JsonResponse:
        user: User = get_object_or_404(User, id=pk)
        user.delete()
        return JsonResponse({"status": "ok"})

    def _add_to_dict(self, user: User) -> dict:
        total_ads: int = Ad.objects.filter(author=user.username, is_published=True).count()
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "locations": user.location.name,
            "total_ads": total_ads,
        }


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
