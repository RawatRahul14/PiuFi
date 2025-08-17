# === Python Modules ===
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# === Custom Modules ===
from src.PiuFi.agent_state import AgentState
from src.PiuFi.schema import QuestionClassifier

# === Utils ===
from src.PiuFi.utils.common import render_prompt

# === Configuration ===
from src.PiuFi.Configuration.config import ModelConfig

# === Main Agent Body ===
async def question_classifier_agent(
        state: AgentState
):
    """
    Agent to classify the model(s) required to answer the user's question.
    """
    # === Variables needed ===
    rephrased_question = state["rephrased_question"]
    is_retriever_available = state["is_retriever_available"]
    tickers_available = True if state.get("tickers") else False

    # === Classifier Prompt ===
    prompt_data = render_prompt(
        prompt_name = "question_classifier",
        rephrased_question = rephrased_question,
        is_retriever_available = is_retriever_available,
        tickers_available = tickers_available
    )

    # === Getting the Model ===
    config = ModelConfig()
    model_name = config.get_agent_model(agent_name = "question_classifier").get("name")

    # === LLM Call ===
    llm = ChatOpenAI(
        model = model_name,
        temperature = 0
    ).with_structured_output(QuestionClassifier)

    messages = [
        SystemMessage(content = prompt_data["system"]),
        HumanMessage(content = prompt_data["user"])
    ]

    response = await llm.ainvoke(
        messages
    )

    # === Output ===

    ## === Models List ===
    state["models_list"] = response.models_list

    return state