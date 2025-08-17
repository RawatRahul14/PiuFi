# === Python Modules ===
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# === Custom Modules ===
from src.PiuFi.agent_state import AgentState
from src.PiuFi.schema import RephrasedQuestion

# === Utils ===
from src.PiuFi.utils.common import render_prompt

# === Configuration ===
from src.PiuFi.Configuration.config import ModelConfig

# === Main Agent Body ===
async def question_rewriter_agent(
        state: AgentState,
        config
):
    """
    ReWrites the user query to make it contextual and also, extracts details from the models

    Args:
        - state (AgentState): Contains all the details of the chat
        - config: Contains details related to PDF file.

    returns:
        - state (AgentState): Returns agentstate but with rephrased_question and other details extracted from the query
    """
    # === Reseting few variables ===

    ## === Rephrased questions ===
    state["rephrased_question"] = None
    state["rag_rephrased_question"] = None
    state["financial_rephrased_question"] = None
    state["technical_rephrased_question"] = None

    ## === Model List ===
    state["models_list"] = []

    ## === Final Answer ===
    state["final_answer"] = None

    # === Loading Chats or creating new instance ===
    if "messages" not in state or state["messages"] is None:
        state["messages"] = {}

    if "n_days" not in state or state["n_days"] is None:
        state["n_days"] = None

    if "direction" not in state or state["direction"] is None:
        state["direction"] = None

    if "tickers" not in state or state["tickers"] is None:
        state["tickers"] = []

    # === If the retriever is available or not ===
    state["is_retriever_available"] = bool(config.get("configurable", {}).get("retriever"))

    # === Variables for the Prompts ===
    current_question = state["question"]

    if len(state["messages"]) < 1:
        conversation = "No Chat History"

    else:
        conversation = "\n".join(
            f"{chat_id}:\n"
            f"User's question: {entry['query']}\n"
            f"Context: {entry['context']}\n"
            f"Keywords: {', '.join(entry['keywords']) or 'None'}\n"
            f"Models used: {', '.join(entry['models_list']) or 'None'}\n"
            f"Final Output: {entry['final_answer'] or 'N/A'}"
            for chat_id, entry in sorted(state["messages"].items())
        )

    # === Prompt ===
    prompt_data = render_prompt(
        prompt_name = "question_rewriter",
        current_question = current_question,
        conversation = conversation
    )

    # === Getting the Model ===
    config = ModelConfig()
    model_name = config.get_agent_model(agent_name = "question_rewriter").get("name")

    # === LLM Call ===
    llm = ChatOpenAI(
        model = model_name,
        temperature = 0
    ).with_structured_output(RephrasedQuestion)

    messages = [
        SystemMessage(content = prompt_data["system"]),
        HumanMessage(content = prompt_data["user"])
    ]

    response = await llm.ainvoke(
        messages
    )

    # === Outputs ===

    ## === Question Recreation ===
    state["rephrased_question"] = response.rephrased_question
    state["rag_rephrased_question"] = response.rag_rephrased_question
    state["financial_rephrased_question"] = response.financial_rephrased_question
    state["technical_rephrased_question"] = response.technical_rephrased_question

    ## === Extraction ===
    state["n_days"] = response.n_days
    state["direction"] = response.direction
    state["tickers"] = response.tickers

    return state