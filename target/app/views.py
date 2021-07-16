from http import HTTPStatus as http_status

import httpx
from django.core.cache import cache
from django.shortcuts import render
from django.views import View


class PersonView(View):
    def get(self, request):
        with httpx.Client(http2=True) as session:
            res = session.get("http://source:4000/api/v1/persons_context")
            if res.status_code == http_status.OK:
                key = res.json()["key"]
            else:
                raise httpx.ConnectError("cannot connect to server")

        context = cache.get(key)
        return render(request, "index.html", context)
