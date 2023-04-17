from rest_framework import serializers

from .models import Match


class MatchCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = ('valuer', 'expectant', 'mark')

