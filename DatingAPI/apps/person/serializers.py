from rest_framework import serializers

from .models import Person
from .services import PersonService


class PersonCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('username', 'first_name', 'last_name', 'birthday', 'email', 'password', 'photo', 'latitude', 'longitude')

    def create(self, validated_data):
        person = Person.objects.create_user(**validated_data)
        return person


class PersonSelfSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('username', 'first_name', 'last_name', 'birthday', 'email', 'photo', 'latitude', 'longitude')


class PersonDetailSerializer(PersonSelfSerializer):
    distance = serializers.SerializerMethodField(method_name='distance_to_person')

    class Meta:
        model = Person
        fields = ('username', 'first_name', 'last_name', 'birthday', 'photo', 'distance')

    def distance_to_person(self, person):
        user = self.context.get('request').user
        distance = PersonService.get_distance(user, person)
        return distance


class PersonListSerializer(PersonSelfSerializer):
    distance = serializers.DecimalField(max_digits=14, decimal_places=6, read_only=True, label='Distance to person')

    class Meta:
        model = Person
        fields = ('username', 'first_name', 'last_name', 'birthday', 'sex', 'distance')

