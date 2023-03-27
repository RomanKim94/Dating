from decimal import Decimal

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from django.db.models import F, ExpressionWrapper, FloatField, DecimalField

from .models import Person
from .serializers import PersonCreateSerializer, PersonDetailSerializer, PersonListSerializer, \
    PersonListByDistanceSerializer


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
                sqrt_max_distance = Decimal(self.kwargs.get('max_distance')) ** 2
                user_longitude = self.request.user.longitude
                user_latitude = self.request.user.latitude
                qs = qs.annotate(sqrt_distance=ExpressionWrapper(((F('longitude') - user_longitude)**2) + ((F('latitude') - user_latitude) ** 2), output_field=DecimalField()))
                qs = qs.filter(sqrt_distance__lte=sqrt_max_distance)
        return qs
