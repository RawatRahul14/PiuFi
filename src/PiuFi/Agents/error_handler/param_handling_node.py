# === Python Modules ===
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.types import Command

# === Agent State ===
from src.PiuFi.agent_state import AgentState

# === Schema ===
from src.PiuFi.schema import MissingHandler

# === Configuration ===
from src.PiuFi.Configuration.config import ModelConfig

# === Utils ===
from src.PiuFi.utils.common import render_prompt

# === Main Agent Body ===
async def missing_handler_agent(
        state: AgentState
):
    """
    Process the user's reply and extract missing information.
    Updates the state with extracted parameters and removes satisfied items from missing_list.
    """

    user_reply = state.get("user_reply")

    # === Get model Configurations ===
    config = ModelConfig()
    model_name: str = config.get_agent_model(agent_name = "missing_handler").get("name")

    # === Prompt ===
    prompt_data = render_prompt(
        prompt_name = "missing_handler",
        user_reply = user_reply
    )

    # === LLM Call ===
    llm = ChatOpenAI(
        model = model_name,
        temperature = 0
    ).with_structured_output(MissingHandler)

    messages = [
        SystemMessage(content = prompt_data["system"]),
        HumanMessage(content = prompt_data["user"])
    ]

    response = await llm.ainvoke(messages)

    # === Use Command to persist updates into the graph state ===
    return Command(update = {
        "tickers": response.tickers,
        "user_reply": None
    })