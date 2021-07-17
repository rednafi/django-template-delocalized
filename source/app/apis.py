from uuid import uuid4

from django.core.cache import cache
from rest_framework import serializers, views
from rest_framework.response import Response

from .models import Album, Musician


class MusicContextSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""

    key = serializers.CharField()


class MusicContextAPIView(views.APIView):
    """Returns the cache record key that contains the music context object."""

    def get(self, request):
        # Getting the object querysets.
        musicians = Musician.objects.all()
        albums = Album.objects.all()

        # Generating key to store the context against.
        music_context_key = str(uuid4())

        # Building the context required to render the html.
        music_context_val = {
            "musicians": musicians,
            "albums": albums,
        }

        # Storing the context in the shared cache.
        cache.set(music_context_key, music_context_val)

        # Returning the key to get the context from the other app.
        data = {"key": music_context_key}
        results = MusicContextSerializer(data).data

        return Response(results)
