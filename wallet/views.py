from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from wallet.serializers import TransactionSerializer, SwapSerializer, TransferSerializer
from wallet.models import Transaction, Swap

from core.constants import NGNC_ADDRESS, USDT_ADDRESS
from core.utils import transfer_tokens
from core.models import User, Profile

from spl.token.instructions import get_associated_token_address
from solders.pubkey import Pubkey

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
    
class TransferView(CreateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = TransferSerializer
    queryset = Transaction.objects.all()


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)

        if not serializer.is_valid():
            return Response(data={"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
        currency_address = NGNC_ADDRESS if request.data["currency"] == "NGN" else USDT_ADDRESS
        amount = request.data["amount"]
        destination = request.data["destination"]


        profile_list = list(filter(lambda p:  p.public_key == destination , Profile.objects.all()))
        profile: Profile = request.user.profile

        if not profile_list:
            return Response(data={"message": {"destination": ["could not find user"]}}, status=status.HTTP_400_BAD_REQUEST)

        destination_profile: Profile = profile_list[0]

        source_token_account = get_associated_token_address(owner=profile.keypair.pubkey(), mint=Pubkey.from_string(currency_address))
        dest_token_account = get_associated_token_address(owner=Pubkey.from_string(destination), mint=Pubkey.from_string(currency_address))

        try:
            transfer_tokens(
                amount=amount,
                owner=profile.keypair,
                token_address=currency_address,
                source_token_account=source_token_account,
                dest_token_account=dest_token_account
            )
        except Exception:
            return Response(data={"message": f"Could not complete transfer of {request.data['currency']} to {request.data['destination']}"}, status=status.HTTP_400_BAD_REQUEST)

        transaction = Transaction(transfer_from=profile.user,transfer_to=destination_profile.user,amount=amount,currency=currency_address)
        transaction.save()

        return Response(data={"message": "Transaction successful"}, status=status.HTTP_201_CREATED)