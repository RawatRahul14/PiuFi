# === Python Modules ===
from langgraph.types import interrupt

# === Custom Modules ===
from src.PiuFi.agent_state import AgentState

# === Utils ===
from src.PiuFi.utils.handle_missing import check_missing

# === Checking if there's any missing value not available ===
async def param_interrupt(
        state: AgentState
):
    """
    Function to check the missing value.
    """
    # If user already replied, don’t raise interrupt again
    if state.get("user_reply"):
        return state

    # === Getting the missing values ===
    missing_list = check_missing(state)

    # === Updating the state ===
    state["missing_list"] = missing_list

    # === Using interrupt ===
    return interrupt(
        {
        "message": f"There are missing inputs required to go through: {', '.join(missing_list)}. Please provide them.",
        "missing_params": missing_list
        }
    )