# === Python Modules ===
from langgraph.graph.state import StateGraph
from langgraph.graph import END
from langchain_core.runnables import RunnableLambda
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

# === Custom Modules ===
from src.PiuFi.agent_state import AgentState

# === Routers ===

## === Missing Params Router ===
from src.PiuFi.routes.param_router import check_missing_param

# === Nodes ===

## === Question Rewriter ===
from src.PiuFi.Agents.rewriter.question_rewriter import question_rewriter_agent

## === Question Classifier ===
from src.PiuFi.Agents.classifier.question_classifier import question_classifier_agent

## === Passthrough Node ===
from src.PiuFi.Agents.passThrough import passthrough_node

## === Missing Value Checker ===
from src.PiuFi.Agents.error_handler.param_interrupter import param_interrupt

## === Missing Value Handler ===
from src.PiuFi.Agents.error_handler.param_handling_node import missing_handler_agent

load_dotenv()

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

    ## === 2.1 Pass Through Node (does nothing) ===
    workflow.add_node(
        "passthrough_node",
        RunnableLambda(passthrough_node).with_config(
            {
                "run_async": True
            }
        )
    )

    workflow.add_node(
        "passthrough_node_2",
        RunnableLambda(passthrough_node).with_config(
            {
                "run_async": True
            }
        )
    )

    ## === 3. Param Interrupter ===
    workflow.add_node(
        "param_interrupt_node",
        RunnableLambda(param_interrupt).with_config(
            {
                "run_async": True
            }
        )
    )

    ## === 4. Param Extracter ===
    workflow.add_node(
        "missing_handler",
        RunnableLambda(missing_handler_agent).with_config(
            {
                "run_async": True
            }
        )
    )

    # === Edges ===
    workflow.set_entry_point("question_rewriter")
    workflow.add_edge("question_rewriter", "question_classifier")
    workflow.add_edge("question_classifier", "passthrough_node")

    workflow.add_conditional_edges(
        "passthrough_node",
        check_missing_param,
        {
            "param_interrupt": "param_interrupt_node",
            "__end__": "passthrough_node_2"
        }
    )

    workflow.add_edge("param_interrupt_node", "missing_handler")
    workflow.add_edge("missing_handler", "passthrough_node_2")

    workflow.add_edge("passthrough_node_2", "__end__")

    return workflow.compile(checkpointer = checkpointer)