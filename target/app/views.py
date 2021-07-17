from __future__ import annotations

import typing
from dataclasses import dataclass
from http import HTTPStatus as http_status

import httpx
from django.core.cache import cache
from django.shortcuts import render
from django.views import View

if typing.TYPE_CHECKING:
    from django.db.models import QuerySet

    from target.app import models as target_models


@dataclass
class MusicContextShape:
    """This is going to be the shape of the retrieved context."""

    musicians: QuerySet[target_models.Musician]
    albums: QuerySet[target_models.Album]


class MusicView(View):
    def get(self, request):
        with httpx.Client(http2=True) as session:
            res = session.get("http://source:4000/api/v1/music_context")
            if res.status_code == http_status.OK:
                key = res.json()["key"]
            else:
                raise httpx.ConnectError("cannot connect to server")

        context = cache.get(key)
        print(context["albums"][0].artist)
        if context.keys() == MusicContextShape.__dataclass_fields__.keys():

            return render(request, "index.html", context)
        else:
            raise ValueError("unexpected context shape")
