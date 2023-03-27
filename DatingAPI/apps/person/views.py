from decimal import Decimal

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from django.db.models import F, ExpressionWrapper, DecimalField

from .models import Person
from .serializers import PersonCreateSerializer, PersonDetailSerializer, PersonListSerializer, \
    PersonListByDistanceSerializer
from .services import Radians, Acos, Cos, Sin


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sex', 'first_name', 'last_name']

    def get_serializer_class(self):
        if self.action == 'create':
            return PersonCreateSerializer
        elif self.action == 'retrieve':
            return PersonDetailSerializer
        elif self.action == 'list':
            if self.kwargs.get('max_distance'):
                return PersonListByDistanceSerializer
            return PersonListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action in ['list', 'retrieve']:
            if self.kwargs.get('max_distance'):
                radius_km = 6367.4
                max_distance = Decimal(self.kwargs.get('max_distance'))
                user_lon_rad = Radians(self.request.user.longitude)
                user_lat_rad = Radians(self.request.user.latitude)
                qs = qs.annotate(distance=ExpressionWrapper(radius_km * Acos(
                    Cos(user_lat_rad) * Cos(Radians(F('latitude'))) *
                    Cos(Radians(F('longitude')) - user_lon_rad) +
                    Sin(user_lat_rad) * Sin(Radians(F('latitude')))
                ), output_field=DecimalField()))
                qs = qs.exclude(username=self.request.user.username).filter(distance__lte=max_distance)
        return qs
