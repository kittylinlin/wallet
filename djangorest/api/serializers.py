from rest_framework import serializers
from .models import Bill


class BillSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Bill
        fields = (
            'id',
            'category',
            'description',
            'amount',
            'date',
            'miscellaneous',
            'owner',
            'date_created',
            'date_updated')
        read_only_fields = ('date_created', 'date_updated')
