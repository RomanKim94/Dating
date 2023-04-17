import os
from decimal import Decimal

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Person
from .permissions import IsAuthenticatedOrCreate
from .serializers import PersonCreateSerializer, PersonDetailSerializer, PersonListSerializer, PersonSelfSerializer
from .services import PersonService


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['first_name', 'last_name']  # example: <host>/api/clients/list/?first_name=Yanna
    permission_classes = [IsAuthenticatedOrCreate, ]
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'create':
            return PersonCreateSerializer
        elif self.action == 'retrieve':
            if self.kwargs.get('id') == self.request.user.id:
                return PersonSelfSerializer
            else:
                return PersonDetailSerializer
        elif self.action == 'list':
            return PersonListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action in ['list', ]:
            qs = qs.exclude(username=self.request.user.username)
            qs = PersonService.add_distance_to_queryset(user=self.request.user, qs=qs)
            qs = PersonService.queryset_filter(params=self.request.query_params, qs=qs)
        return qs
