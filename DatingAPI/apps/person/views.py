from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .models import Person
from .serializers import PersonCreateSerializer, PersonDetailSerializer, PersonListSerializer


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
            return PersonListSerializer

