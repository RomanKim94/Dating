from rest_framework import serializers

from .models import Person


class PersonCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('username', 'first_name', 'last_name', 'age', 'email', 'password', 'photo', 'latitude', 'longitude')

    def create(self, validated_data):
        person = Person.objects.create_user(**validated_data)
        return person


class PersonDetailSerializer(PersonCreateSerializer):

    class Meta:
        model = Person
        fields = ('username', 'first_name', 'last_name', 'age', 'photo')


class PersonListSerializer(PersonCreateSerializer):
    distance = serializers.DecimalField(max_digits=14, decimal_places=6, read_only=True, label='Distance to person')

    class Meta:
        model = Person
        fields = ('username', 'first_name', 'last_name', 'age', 'sex', 'distance')

