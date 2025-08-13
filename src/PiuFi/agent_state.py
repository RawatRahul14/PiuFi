# === Python Modules ===
from typing import TypedDict, Dict, Optional, List, Literal

## === Chat Entry ===
class ChatEntry(TypedDict):

    # === User's rephrased question ===
    query: str

    # === What the question is about ===
    context: str

    # === Contextual based Keywords ===
    keywords: List[str]

    # === Time of the query ===
    timestamp: str

    # === Models Used ===
    models_list: List[str]

    # === Each Model's output ===
    rephrased_question: Optional[str]
    rag_rephrased_question: Optional[str]
    financial_rephrased_question: Optional[str]
    technical_rephrased_question: Optional[str]

    final_answer: Optional[str]


# === Agent State ===
class AgentState(TypedDict):
    # === User's query ===
    question: str
    
    # === Information Extracted ===
    n_days: Optional[int]
    direction: Optional[Literal["past", "future", "present"]]
    tickers: List[Optional[str]]

    # === Models Used ===
    models_list: List[str]

    # === Chat History ===
    messages: Dict[str, ChatEntry]

    # === Rephrased Questions ===
    rephrased_question: Optional[str]
    rag_rephrased_question: Optional[str]
    financial_rephrased_question: Optional[str]
    technical_rephrased_question: Optional[str]

    # === Final Answer ===
    final_answer: Optional[str]