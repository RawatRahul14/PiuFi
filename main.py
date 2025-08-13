# === Python Modules ===
from langgraph.graph.state import StateGraph
from langgraph.graph import END
from langchain_core.runnables import RunnableLambda
from langgraph.checkpoint.memory import MemorySaver

# === Custom Modules ===
from src.PiuFi.agent_state import AgentState

# === Nodes ===

## === Question Rewriter ===
from src.PiuFi.Agents.question_rewriter import question_rewriter_agent

def graph():
    """
    Builds the Graph Flow
    """

    # === Initialising the graph with Agent State ===
    workflow = StateGraph(AgentState)
    checkpointer = MemorySaver()

    # === Nodes ===
    workflow.add_node(
        "question_rewriter",
        RunnableLambda(question_rewriter_agent).with_config(
            {
                "run_async": True
            }
        )
    )

    # === Edges ===
    workflow.set_entry_point("question_rewriter")
    workflow.add_edge("question_rewriter", END)

    return workflow.compile(checkpointer = checkpointer)