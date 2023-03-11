from django.urls import path
from wallet.views import MySwapsView, MyTransactionsView

app_name = "wallet"

urlpatterns = [
    path('my-transactions/', MyTransactionsView.as_view(), name='token_obtain_pair'),
    path('my-swaps/', MySwapsView.as_view(), name='token_obtain_pair'),
]