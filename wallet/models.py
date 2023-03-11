from django.db import models
from core.utils import is_valid_pubkey, get_currency_name
from typing import Literal
class Transaction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    transfer_from = models.ForeignKey("core.User", on_delete=models.CASCADE, related_name="transactions_out")
    transfer_to = models.ForeignKey("core.User", on_delete=models.CASCADE, related_name="transactions_in")
    amount = models.IntegerField()
    currency = models.CharField(max_length=44, validators=[is_valid_pubkey])

    @property
    def currency_name(self):
        return get_currency_name(self.currency)
    
    
class Swap(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("core.User", on_delete=models.CASCADE)
    from_currency = models.CharField(max_length=44, validators=[is_valid_pubkey])
    from_amount = models.IntegerField()
    to_currency = models.CharField(max_length=44, validators=[is_valid_pubkey])
    to_amount = models.IntegerField()

    @property
    def from_currency_name(self):
        return get_currency_name(self.from_currency)
    
    @property
    def to_currency_name(self):
        return get_currency_name(self.to_currency)
