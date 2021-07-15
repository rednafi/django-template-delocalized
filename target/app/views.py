import httpx
from django.core.cache import cache
from django.shortcuts import render
from django.views import View


class PersonView(View):
    def get(self, request):
        with httpx.Client(http2=True) as session:
            res = session.get("http://localhost:4000/api/v1/persons_context")
            if res.status_code == 200:
                key = res.json()[0]["key"]

        context = cache.get(key)
        return render(request, "index.html", context)
