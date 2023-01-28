import json
import requests

from rest_framework.views import exception_handler

from solders.rpc.requests import GetBalance, RequestAirdrop
from solders.rpc.config import RpcContextConfig, RpcRequestAirdropConfig
from solders.pubkey import Pubkey
from solders.commitment_config import CommitmentLevel



make_request = lambda body: requests.post("https://api.devnet.solana.com/", json=json.loads(body)).json()

def get_balance(pubkey: str):
    config = RpcContextConfig(min_context_slot=1)
    body = GetBalance(Pubkey.from_string(pubkey), config).to_json()
    response = make_request(body)
    value = response["result"]["value"]
    return value

def request_airdrop(pubkey: str):
    config = RpcRequestAirdropConfig(commitment=CommitmentLevel.Confirmed)
    body =  RequestAirdrop(Pubkey.from_string(pubkey), 1000000000, config).to_json()
    signature = make_request(body)["result"]
    return signature

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        if response.data.get("detail"):
            response.data['message'] = response.data.pop('detail')
    return response