from typing import Union

from mythril.analysis.ops import VarType, Call, get_variable
from mythril.laser.ethereum.state.global_state import GlobalState


def get_call_from_state(state: GlobalState) -> Union[Call, None]:
    instruction = state.get_current_instruction()

    op = instruction["opcode"]

    stack = state.mstate.stack

    if op in ("CALL", "CALLCODE"):
        gas, to, value, meminstart, meminsz, memoutstart, memoutsz = (
            get_variable(stack[-1]),
            get_variable(stack[-2]),
            get_variable(stack[-3]),
            get_variable(stack[-4]),
            get_variable(stack[-5]),
            get_variable(stack[-6]),
            get_variable(stack[-7]),
        )

        if to.type == VarType.CONCRETE and to.val < 5:
            return None

        if meminstart.type == VarType.CONCRETE and meminsz.type == VarType.CONCRETE:
            return Call(
                state.node,
                state,
                None,
                op,
                to,
                gas,
                value,
                state.mstate.memory[meminstart.val : meminsz.val * 4],
            )
        else:
            return Call(state.node, state, None, op, to, gas, value)

    else:
        gas, to, meminstart, meminsz, memoutstart, memoutsz = (
            get_variable(stack[-1]),
            get_variable(stack[-2]),
            get_variable(stack[-3]),
            get_variable(stack[-4]),
            get_variable(stack[-5]),
            get_variable(stack[-6]),
        )

        return Call(state.node, state, None, op, to, gas)
