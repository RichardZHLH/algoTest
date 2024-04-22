# File: conftest.py
import os
import math
from algosdk.abi import ABIType
from algosdk.atomic_transaction_composer import TransactionWithSigner, AccountTransactionSigner
from algosdk.encoding import decode_address, encode_address, encode_as_bytes
from algosdk.transaction import AssetOptInTxn, PaymentTxn, AssetCreateTxn,AssetTransferTxn
from algosdk import account, transaction,logic, util, mnemonic, v2client
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    LogicSigTransactionSigner,
    TransactionWithSigner,
)
import beaker
import Bridge
import Target

import pytest



@pytest.fixture
def owner():
    accts = beaker.localnet.get_accounts()
    return accts[0]    

@pytest.fixture
def admin():
    accts = beaker.localnet.get_accounts()
    return accts[1] 

@pytest.fixture
def user():
    accts = beaker.localnet.get_accounts()
    return accts[2] 

@pytest.fixture
def feeProxyAddr():
    accts = beaker.localnet.get_accounts()
    return accts[2].address 


@pytest.fixture
def app_client(owner):
    algod_client = beaker.localnet.get_algod_client()
    app_client = beaker.client.ApplicationClient(
        client=algod_client,
        app=Bridge.app,
        signer=owner.signer,
    ) 
    app_client.create()
    app_client.fund(2000000)

    return app_client



##############
@pytest.fixture
def Target_ID(owner):
    algod_client = beaker.localnet.get_algod_client()
    app_clientT = beaker.client.ApplicationClient(
        client=algod_client,
        app=Target.app,
        signer=owner.signer,
    ) 
    app_clientT.create()
    # print("Target ID:", app_clientT.app_id)
    return app_clientT.app_id 


@pytest.fixture
def app_client_target(owner, Target_ID):
    algod_client = beaker.localnet.get_algod_client()
    app_client_target = beaker.client.ApplicationClient(
        client=algod_client,
        app=Target.app,
        app_id=Target_ID,
        signer=owner.signer,
    ) 
    return app_client_target    