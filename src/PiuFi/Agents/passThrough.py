# === Agent State ===
from src.PiuFi.agent_state import AgentState

# === Pass Through Node Body ===
async def passthrough_node(
        state: AgentState
) -> AgentState:
    """
    Just a passthrough node
    """
    return state