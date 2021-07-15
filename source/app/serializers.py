from rest_framework import serializers

from .models import Person


# Serializers define the API representation.
class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ["name", "age", "height"]
