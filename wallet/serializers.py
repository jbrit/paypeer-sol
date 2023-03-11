from rest_framework import serializers
from wallet.models import Transaction, Swap

class TransactionSerializer(serializers.ModelSerializer):
    currency_name = serializers.CharField()
    class Meta:
        model = Transaction
        fields = '__all__'

class SwapSerializer(serializers.ModelSerializer):
    from_currency_name = serializers.CharField()
    to_currency_name = serializers.CharField()
    class Meta:
        model = Swap
        fields = '__all__'