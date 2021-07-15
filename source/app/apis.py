from uuid import uuid4

from django.core.cache import cache
from rest_framework import serializers, views
from rest_framework.response import Response

from .models import Person


class PersonContextSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""

    key = serializers.CharField()


class PersonContextAPIView(views.APIView):
    def get(self, request):
        persons = Person.objects.all()
        persons_context_key = str(uuid4())
        persons_context_val = {"persons": persons}
        cache.set(persons_context_key, persons_context_val, 10000)
        data = [{"key": persons_context_key}]
        results = PersonContextSerializer(data, many=True).data
        print(cache.get(persons_context_key))
        return Response(results)
