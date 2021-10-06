from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from .parsing import result



class HomePage(View):
    def get(self, request):
        url = request.GET.get('url')
        if url:
            if cache.get('data'):
                page = request.GET.get('page', 1)
                paginator = Paginator(cache.get('data'), 1)
                data = paginator.page(page)
            else:
                scrapping_data = result(url)
                page = request.GET.get('page', 1)
                paginator = Paginator(scrapping_data, 1)
                data = paginator.page(page)
                cache.set('data', scrapping_data, 60 * 15)
            return render(request, 'result.html', {'data': data, 'url': url})
        return render(request, 'index.html')  
        