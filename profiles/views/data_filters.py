from django.http  import JsonResponse
from django.views import View

from positions.models import Position, Subcategory


class FilterCities(View):
    def get(self, request, *args, **kwargs):
        state = request.GET.get('state')
        cities = [city for city in Position.CITY_CHOICES if state in ['SP', 'RJ']]
        return JsonResponse(cities, safe=False)


class FilterSubcategories(View):
    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        subcategories = list(Subcategory.objects.filter(category_id=category_id).values('id', 'name'))
        return JsonResponse(subcategories, safe=False)