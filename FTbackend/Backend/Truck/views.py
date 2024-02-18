from django.core.paginator import Paginator
from django.db.models import ExpressionWrapper, F, FloatField
from django.http import JsonResponse
from django.views import View
import json
from .utils import calculate_distance
from .models import TruckModel
from django.core.serializers import serialize


class TruckModelCreateView(View):
    def calculate_required_radius(self, x, y):
        return calculate_distance(x, y)

    def truck_extraction_query(self, radius_required, radius, interval=100):
        trucks = []

        while len(trucks) <= 5:

            trucks = TruckModel.objects.filter(
                rel_distance__gte=radius_required - radius,
                rel_distance__lte=radius_required + radius,
            ).annotate(
                shortest_distance=ExpressionWrapper(
                    F('rel_distance') - radius_required,
                    output_field=FloatField()
                )
            ).order_by('shortest_distance')

            radius += interval

        return trucks

    def pagination_setter(self, page_size=10):
        per_page = page_size
        if self.trucks:
            self.paginator = Paginator(self.trucks, per_page)
            page_objects = self.paginator.get_page(self.page)
            return page_objects
        return None

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        self.x_coordinates = float(data.get('x'))
        self.y_coordinates = float(data.get('y'))
        self.radius = float(data.get('radius')) if data.get('radius') else 100
        # Get the current page number from request
        self.page = int(request.GET.get('page', 1))

        radius_required = self.calculate_required_radius(
            self.x_coordinates, self.y_coordinates)

        self.trucks = self.truck_extraction_query(radius_required, self.radius)
        page_objects = self.pagination_setter()

        serialized_trucks = serialize('json', page_objects)

        return JsonResponse({
            'trucks': serialized_trucks,
            'has_next': page_objects.has_next(),
            'has_previous': page_objects.has_previous(),
            'total_pages': self.paginator.num_pages,
            'current_page': page_objects.number
        }, safe=False)
