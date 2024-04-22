from typing import Final
from pyteal import *
from beaker import *
from beaker.lib.storage import BoxMapping



class TargetState:
    count: Final[GlobalStateValue] = GlobalStateValue(
        TealType.uint64,
    )
        

app = Application(
    "Target", 
    descr="target", 
    state=TargetState()
)


@app.external
def getCount(*, output: abi.Uint64)-> Expr:
    # Log(Itob(app.state.count)) # Not need
    return output.set(app.state.count)

@app.external
def setCount(a: abi.Uint64)->Expr:
    return app.state.count.set(a.get())

@app.external
def add(a: abi.Uint64, *, output: abi.Uint64) ->Expr:
    return Seq(
        app.state.count.set(a.get() + app.state.count),
        output.set(app.state.count)
    )
