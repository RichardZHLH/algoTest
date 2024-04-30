import os
import math
from algosdk.abi import ABIType
from algosdk.atomic_transaction_composer import TransactionWithSigner, AccountTransactionSigner
from algosdk.encoding import decode_address, encode_address, encode_as_bytes, _correct_padding
from algosdk.transaction import AssetOptInTxn, PaymentTxn, AssetCreateTxn,AssetTransferTxn
from algosdk import account, transaction,logic, util, mnemonic, v2client, encoding,abi
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    LogicSigTransactionSigner,
    TransactionWithSigner,
)
import beaker
import base64

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

@pytest.mark.abi2
def test_encode_base32():
    txidhex = '5df5236b7bf7cd284cbb67f9108261a00ba37f11f2a5394898d685660adffe3d'
    txidh = bytes.fromhex(txidhex)
    txid = encoding._undo_padding(base64.b32encode(txidh).decode())
    
    print("txid--------------------:", txid)
    r = base64.b32decode(_correct_padding(txid))
    print("r:", r.hex())
    assert r.hex() == txidhex

@pytest.mark.abi
def test_abi(app_client):
  # abi.StaticBytes[Literal[64]]

  # print("xxx:", record_codec)
  tx = app_client.call(
      Bridge.setEvent,
      smgID=bytes.fromhex('000000000000000000000000000000000000000000746573746e65745f303633'),
      tokenPairID=666, 
      fromAccount=2233887,
      value=2000,
      contractFee=300,
      userAccount="0x8260fca590c675be800bbcde4a9ed067ead46612e25b33bc9b6f027ef12326e6",
  )  
  logs = tx.tx_info['logs'][0]
  print("logs:",  logs)
  print("type_spec:", str(Bridge.MessageInfo().type_spec()))
  codec = ABIType.from_string(str(Bridge.MessageInfo().type_spec()))  #(uint64, string, uing64)
  logb = base64.b64decode(logs)
  loga = codec.decode(logb)
  print("logs:", loga)
  smgIDn =  bytes(bytearray(loga[1])).hex()
  print("smgIDn:", smgIDn)
  txida = loga[7]
  txhdb =   bytes(bytearray(txida))
  txid = encoding._undo_padding(base64.b32encode(txhdb).decode())
  print("txid:", txid)

@pytest.mark.encode
def test_encode(app_client):
  codec = abi.ABIType.from_string("(uint64,string)")

  info = app_client.call( Bridge.encodeTupple)  
  print("info:", info.return_value)
  bret = ''.join(format(x, '02x') for x in info.return_value)
  decoded = codec.decode(bytes.fromhex(bret))    
  print("decoded:", decoded)

  encoded = codec.encode([100, "aaa"])
  print("python encoded:", encoded.hex())

  info = app_client.call( Bridge.getMessageInfo)  
  print("getMessageInfo:", info.return_value)

  