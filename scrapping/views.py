from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .parsing import result

class HomePage(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        url = request.POST.get('url')
        scrapping_data = result(url)
        page = 1
        paginator = Paginator(scrapping_data, 1)
        data = paginator.page(page).object_list[0]
        return render(request, 'result.html', {'data': data})
        