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

@pytest.mark.cross
def test_cross(app_client, app_client_target, Target_ID):
    tx = app_client.call(
        Bridge.callSetCount,
        app_id=Target_ID,
        a=14,
        foreign_apps=[Target_ID]
    )



    ret = app_client_target.call(
        Target.getCount,
    )  
    print("app_client_target ret:", ret.return_value)  
    



    ret = app_client.call(
        Bridge.callGetCount,
        app_id=Target_ID,
        foreign_apps=[Target_ID]
    )  
    print("ret:",  ret.return_value)




    ret = app_client.call(
        Bridge.callGetCount,
        app_id=Target_ID,
        foreign_apps=[Target_ID]
    )  
    print("ret:",  ret.return_value)



    tx = app_client.call(
        Bridge.callAdd,
        app_id=Target_ID,
        a=100,
        foreign_apps=[Target_ID]
    )  
    print("callAdd  tx:",  tx.return_value)
    ret = app_client.call(
        Bridge.callGetCount,
        app_id=Target_ID,
        foreign_apps=[Target_ID]
    )  
    print("ret:",  ret.return_value)