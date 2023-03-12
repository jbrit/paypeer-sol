from rest_framework import serializers
from wallet.models import Transaction, Swap
from django.contrib.auth import get_user_model
from core.utils import is_valid_pubkey

class UserInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='profile.name')
    public_key = serializers.CharField(source='profile.public_key')
    class Meta:
        model = get_user_model()
        fields = "name", "public_key"

class TransactionSerializer(serializers.ModelSerializer):
    transfer_from = UserInfoSerializer()
    transfer_to = UserInfoSerializer()

    currency_name = serializers.CharField()
    class Meta:
        model = Transaction
        fields = '__all__'

class SwapSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    from_currency_name = serializers.CharField()
    to_currency_name = serializers.CharField()
    class Meta:
        model = Swap
        fields = '__all__'

class TransferSerializer(serializers.Serializer):
    currency = serializers.ChoiceField(["NGN", "USD"], write_only=True)
    amount = serializers.IntegerField(write_only=True)
    destination = serializers.CharField(validators=[is_valid_pubkey],write_only=True)