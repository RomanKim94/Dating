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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, expectant = self.perform_create(serializer)
        mark = serializer.validated_data.get('mark')
        headers = self.get_success_headers(serializer.data)
        new_serializer_data = None
        # Code below: If user likes expectant and expectant likes user, user will see expectant email and will send email to both
        if mark and Matching.is_mutually(user, expectant):
            new_serializer_data = {'expectant_email': expectant.email}
            new_serializer_data.update(serializer.data)
            Matching.send_notification(user, expectant)
        return Response(new_serializer_data or serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = self.request.user
        expectant = Person.objects.filter(id=self.kwargs.get('id'))[0]
        serializer.save(valuer=user, expectant=expectant)
        return user, expectant
