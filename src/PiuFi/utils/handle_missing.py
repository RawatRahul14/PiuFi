# === Python Modules ===
from typing import List, Optional
from src.PiuFi.agent_state import AgentState

def check_missing(
        state: AgentState
) -> List[Optional[str]]:
    """
    Check which parameters are missing based on the models_list in state.
    """
    models: List = state.get("models_list")
    missing: List = []

    # === Indicator Analyst Model ===
    if "indicator_analyst_model" in models:
        if not state.get("tickers"):
            missing.append("tickers")   # 👈 keep lowercase for consistency

    # Save into state before returning
    return missing