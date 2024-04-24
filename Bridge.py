from typing import Literal
from typing import Final
from pyteal import *
import pyteal as pt
from beaker import *
from beaker.lib.storage import BoxMapping, BoxList

import Target

class MessageInfo(abi.NamedTuple):
    name:         abi.Field[abi.String]
    smgID:        abi.Field[abi.StaticBytes[Literal[32]]]
    tokenPairID:  abi.Field[abi.Uint64]
    fromAccount:  abi.Field[abi.Uint64]
    value:        abi.Field[abi.Uint64]
    contractFee:  abi.Field[abi.Uint64]
    userAccount:  abi.Field[abi.String]
    txid:         abi.Field[abi.StaticBytes[Literal[32]]]



class BridgeState:
    storeValue: Final[GlobalStateValue] = GlobalStateValue(
        TealType.bytes,
    )
    mapStore = BoxMapping(abi.Uint64, abi.DynamicBytes)

    
app = Application(
    "Bridge", 
    descr="Cross chain entry point", 
    state=BridgeState()
)


###
# API Methods
###
# TODO test the limit
@app.external()
def store1(a: abi.DynamicBytes) -> Expr:
    return Approve()
@app.external()
def store2(a: abi.DynamicBytes, b:abi.DynamicBytes) -> Expr:
    return Approve() 
@app.external()
def store3(a: abi.DynamicBytes) -> Expr:
    return app.state.storeValue.set(a.get())
@app.external()
def getStore3(*, output: abi.DynamicBytes) ->Expr:
    return output.set(app.state.storeValue)
@app.external()
def store4(a: abi.Uint64, b: abi.DynamicBytes) -> Expr:
    return app.state.mapStore[a].set(b)

@app.external()
def setEvent(smgID: abi.StaticBytes[Literal[32]],
    tokenPairID:  abi.Uint64,
    fromAccount: abi.Uint64,
    value: abi.Uint64,
    contractFee: abi.Uint64,
    userAccount:  abi.String,
  ) -> Expr:
    name = abi.make(abi.String)
    txid = abi.make(abi.StaticBytes[Literal[32]]) 
    return Seq(
      name.set("userLockLogger"),
      txid.set(Txn.tx_id()),
      (info := MessageInfo()).set(name, smgID, tokenPairID, fromAccount, value, contractFee,  userAccount, txid),
      Log(info.encode())
    )


@app.external()
def callSetCount(app_id: abi.Uint64, a: abi.Uint64) -> Expr:
  return Seq(
    InnerTxnBuilder.ExecuteMethodCall(
        app_id=app_id.get(),
        method_signature=Target.setCount.method_signature(),
        args=[a],
    ),
  )

@app.external()
def callGetCount(app_id: abi.Uint64, *, output: abi.Uint64) -> Expr:
  return Seq(
    InnerTxnBuilder.ExecuteMethodCall(
        app_id=app_id.get(),
        method_signature=Target.getCount.method_signature(),
        args=[],
    ),
    output.set(Btoi(pt.Extract(InnerTxn.last_log(), pt.Int(4), pt.Int(8))))
  )

@app.external()
def callAdd(app_id: abi.Uint64,a: abi.Uint64, *, output: abi.Uint64) -> Expr:
  return Seq(
    InnerTxnBuilder.ExecuteMethodCall(
        app_id=app_id.get(),
        method_signature=Target.add.method_signature(),
        args=[a],
    ),
    output.set(Btoi(pt.Extract(InnerTxn.last_log(), pt.Int(4), pt.Int(8))))
  )


@app.external()
def encodeTupple(*, output: abi.DynamicBytes) -> Expr:
  a = abi.make(abi.Uint64)
  b = abi.make(abi.String)
  return Seq(
    a.set(Int(100)),
    b.set(Bytes("aaa")),
    output.set(pt.ast.abi.tuple._encode_tuple((a, b)))
  )    
@app.external()
def getMessageInfo(*, output: MessageInfo) -> Expr:  
  name = abi.make(abi.String)
  txid = abi.make(abi.StaticBytes[Literal[32]]) 
  a = abi.make(abi.Uint64)
  return Seq(
      name.set("userLockLogger"),
      a.set(Int(100)),
      txid.set(Txn.tx_id()),
      output.set(name, txid, a, a, a, a,  name, txid),
  )