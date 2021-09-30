from django.shortcuts import render
from django.views import View

# Create your views here.


class HomePage(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        url = request.POST.get('url')
        return render(request, 'result.html')
        