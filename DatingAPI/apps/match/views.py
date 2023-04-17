from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Match
from .serializers import MatchCreateSerializer
from ..person.models import Person
from .services import Matching


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'create':
            return MatchCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        expectant = Person.objects.filter(id=self.kwargs.get('id')).first()
        serializer.save(valuer=user, expectant=expectant)
        return user, expectant

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, expectant = self.perform_create(serializer)
        mark = serializer.validated_data.get('mark')
        headers = self.get_success_headers(serializer.data)
        data = Matching.send_info_if_mutually(user, expectant, mark, serializer.validated_data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

