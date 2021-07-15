from rest_framework import viewsets

from .models import Person
from .serializers import PersonSerializer


# ViewSets define the view behavior.
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
