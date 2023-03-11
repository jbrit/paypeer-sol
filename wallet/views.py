from rest_framework.generics import ListAPIView
from wallet.serializers import TransactionSerializer, SwapSerializer
from rest_framework import permissions
from wallet.models import Transaction, Swap

class MyTransactionsView(ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return Transaction.objects.filter(transfer_from_id=user_id) | Transaction.objects.filter(transfer_to_id=user_id)

class MySwapsView(ListAPIView):
    serializer_class = SwapSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return Swap.objects.filter(user_id=user_id)