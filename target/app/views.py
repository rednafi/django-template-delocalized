from django.core.cache import cache
from django.shortcuts import render
from django.views import View


class PersonView(View):
    def get(self, request):
        context = cache.get("09d4a324-7bb3-44f4-b989-902fdb0a11dc")
        print(context)
        return render(request, "index.html", context)
