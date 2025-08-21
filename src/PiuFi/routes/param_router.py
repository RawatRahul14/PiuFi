# === Python Modules ===
from typing import List

# === Agent State ===
from src.PiuFi.agent_state import AgentState

# === Utils ===
from src.PiuFi.utils.handle_missing import check_missing

# === Main Router Body ===
async def check_missing_param(
        state: AgentState
):
    """
    Checks and routes the graph to a specific Node
    """
    # === Checking if there any parameter missing ===
    missing_list: List = check_missing(state = state)

    state["missing_list"] = missing_list
    state["is_missing"] = bool(missing_list)

    if bool(missing_list):
        return "param_interrupt"

    else:
        return "__end__"