from rest_framework import serializers
from .models import TruckModel


class TruckModelSerializer(serializers.ModelField):
    class Meta:
        model = TruckModel
        field = fields = ['id', 'name', 'type', 'locationx',
                          'locationy', 'status', 'rel_distance']
