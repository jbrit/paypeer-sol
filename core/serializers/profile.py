
from rest_framework import serializers
from core.models import Profile
from core.utils import get_token_balance
from core.constants import NGNC_ADDRESS, USDT_ADDRESS



class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.SerializerMethodField()
    ngnc_balance = serializers.SerializerMethodField()
    usdt_balance = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["public_key", "email", "name", "ngnc_balance", "usdt_balance"]

    def get_email(self, obj):
        return obj.user.email
    
    def get_ngnc_balance(self, obj):
        balance, info = get_token_balance(obj.public_key, NGNC_ADDRESS)
        return balance / (10**info.decimals)
    
    def get_usdt_balance(self, obj):
        balance, info = get_token_balance(obj.public_key, USDT_ADDRESS)
        return balance / (10**info.decimals)