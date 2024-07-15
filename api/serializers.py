from rest_framework import serializers
from .models import BondPost


class BondPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BondPost
        fields = [
            "id",
            "bond_name",
            "isin",
            "bond_value",
            "interest_rate",
            "purchase_date",
            "due_date",
            "yields_freq"
        ]
