from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator

from .parsing import result

class HomePage(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        url = request.POST.get('url')
        data = result(url)
        paginate = Paginator(data, 1)
        return render(request, 'result.html', {'data': paginate})
        