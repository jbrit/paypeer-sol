from django.urls import path
from wallet.views import MySwapsView, MyTransactionsView, TransferView

app_name = "wallet"

urlpatterns = [
    path('my-transactions/', MyTransactionsView.as_view()),
    path('my-swaps/', MySwapsView.as_view()),
    path('transfer/', TransferView.as_view()),
]