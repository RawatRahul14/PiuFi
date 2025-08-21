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
    # === If user already replied, don’t raise interrupt again ===
    if state.get("user_reply"):
        return state

    # === Getting the missing values ===
    missing_list = check_missing(state)

    # === Updating the state ===
    state["missing_list"] = missing_list

    # === Using interrupt ===
    return interrupt(
        {
        "message": (
            "⚠️ I'm missing some details before I can continue.\n\n"
            f"👉 Specifically, I still need: {', '.join(missing_list)}.\n\n"
            "Please provide this information so I can give you the right analysis."
        ),
        "missing_params": missing_list
        }
    )