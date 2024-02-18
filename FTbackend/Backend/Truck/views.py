from django.core.paginator import Paginator
from django.db.models import ExpressionWrapper, F, FloatField
from django.http import JsonResponse
from django.views import View
import json
from .utils import calculate_distance
from .models import TruckModel
from django.core.serializers import serialize


class TruckModelCreateView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        x_coordinates = float(data.get('x'))
        y_coordinates = float(data.get('y'))
        radius = float(data.get('radius')) if data.get('radius') else 100
        # Get the current page number from request
        page = int(request.GET.get('page', 1))

        radius_required = calculate_distance(x_coordinates, y_coordinates)

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

            radius += 100

        print(f"Found food trucks at {radius}")

        per_page = 10
        paginator = Paginator(trucks, per_page)
        page_objects = paginator.get_page(page)

        serialized_trucks = serialize('json', page_objects)

        return JsonResponse({
            'trucks': serialized_trucks,
            'has_next': page_objects.has_next(),
            'has_previous': page_objects.has_previous(),
            'total_pages': paginator.num_pages,
            'current_page': page_objects.number
        }, safe=False)
