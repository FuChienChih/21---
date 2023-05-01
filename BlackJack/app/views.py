from django.shortcuts import render
from django.views.generic import View

# Create your views here.


class Index(View):
    def get(self, request):
        data = {"name": "Adam", "age": 18}
        return render(request, "index.html", data)
