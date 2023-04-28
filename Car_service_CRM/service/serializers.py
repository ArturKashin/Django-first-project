from .models import Orders, WorksOrder
from rest_framework import serializers


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Orders
        fields = ['id',
                  'client',
                  'vin_number',
                  'registration_number',
                  'notes',
                  'date_start',
                  'date_completed',
                  'final_price']


class WorksOrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorksOrder
        fields = ['id',
                  'name',
                  'standard',
                  'price',
                  'order_status',
                  'final_price',
                  'order',
                  'completed',
                  'executor']