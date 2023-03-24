from rest_framework import serializers

from .models import Person


class PersonCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('username', 'first_name', 'last_name', 'age', 'email', 'password', 'photo')

    def create(self, validated_data):
        person = Person.objects.create_user(**validated_data)
        return person


class PersonDetailSerializer(PersonCreateSerializer):

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'age', 'photo', 'sex')


class PersonListSerializer(PersonCreateSerializer):

    class Meta:
        model = Person
        fields = ('username', 'first_name', 'last_name', 'age', 'sex')
