import os
from decimal import Decimal

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Person
from .permissions import IsAuthenticatedOrCreate
from .serializers import PersonCreateSerializer, PersonDetailSerializer, PersonListSerializer
from .services import PersonService


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['sex', 'first_name', 'last_name']  # example: <host>/api/clients/list/?first_name=Yanna
    permission_classes = [IsAuthenticatedOrCreate, ]

    def get_serializer_class(self):
        if self.action == 'create':
            return PersonCreateSerializer
        elif self.action == 'retrieve':
            return PersonDetailSerializer
        elif self.action == 'list':
            return PersonListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action in ['list', ]:
            qs = qs.exclude(username=self.request.user.username)
            qs = PersonService.add_distance(user=self.request.user, qs=qs)
            max_distance = self.request.query_params.get('max_distance')
            min_distance = self.request.query_params.get('min_distance')
            if max_distance is not None:
                max_distance = Decimal(max_distance)
                qs = qs.filter(distance__lte=max_distance)
            if min_distance is not None:
                min_distance = Decimal(min_distance)
                qs = qs.filter(distance__gte=min_distance)
        return qs

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, username__icontains=self.kwargs.get('username'))
        serializer = PersonDetailSerializer(user)
        return Response(serializer.data)
