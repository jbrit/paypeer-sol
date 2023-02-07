import base58
import json
import os
import requests

from rest_framework.views import exception_handler

from solana.rpc.api import Client
from solana.rpc.commitment import Confirmed

from solders.rpc.requests import GetBalance, RequestAirdrop
from solders.rpc.config import RpcContextConfig, RpcRequestAirdropConfig
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.commitment_config import CommitmentLevel

from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.client import Token

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


private_key = os.environ["SOLANA_PRIVATE_KEY"]

client = Client(endpoint="https://api.devnet.solana.com", commitment=Confirmed)
owner = Keypair.from_seed(base58.b58decode(private_key))

def get_token_balance():
    token = Token(
        conn=client,
        pubkey=Pubkey.from_string("BBPQBEAL4uMvyL99Ms6r2vqaVst4RtgZF8Xgnut2x1Lh"),
        payer=owner,
        program_id=TOKEN_PROGRAM_ID,
    )

    amount = token.get_account_info(Pubkey.from_string("BBPQBEAL4uMvyL99Ms6r2vqaVst4RtgZF8Xgnut2x1Lh")).amount

    print(amount)
