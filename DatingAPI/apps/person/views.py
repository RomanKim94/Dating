from django.shortcuts import render
from rest_framework import viewsets, mixins

from .models import Person
from .serializers import PersonCreateSerializer


class PersonCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonCreateSerializer
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.action == 'create':
            return PersonCreateSerializer
        return super().get_serializer_class()
