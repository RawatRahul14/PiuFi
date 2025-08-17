# === Python Modules ===
from langgraph.graph.state import StateGraph
from langgraph.graph import END
from langchain_core.runnables import RunnableLambda
from langgraph.checkpoint.memory import MemorySaver

# === Custom Modules ===
from src.PiuFi.agent_state import AgentState

# === Nodes ===

## === Question Rewriter ===
from src.PiuFi.Agents.rewriter.question_rewriter import question_rewriter_agent

## === Question Classifier ===
from src.PiuFi.Agents.classifier.question_classifier import question_classifier_agent

def graph():
    """
    Builds the Graph Flow
    """

    # === Initialising the graph with Agent State ===
    workflow = StateGraph(AgentState)
    checkpointer = MemorySaver()

    # === Nodes ===

    ## === 1. Rewriter ===
    workflow.add_node(
        "question_rewriter",
        RunnableLambda(question_rewriter_agent).with_config(
            {
                "run_async": True
            }
        )
    )

    ## === 2. Classifier ===
    workflow.add_node(
        "question_classifier",
        RunnableLambda(question_classifier_agent).with_config(
            {
                "run_async": True
            }
        )
    )

    # === Edges ===
    workflow.set_entry_point("question_rewriter")
    workflow.add_edge("question_rewriter", "question_classifier")
    workflow.add_edge("question_classifier", END)

    return workflow.compile(checkpointer = checkpointer)