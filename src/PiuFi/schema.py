# === Python Modules ===
from typing import Literal, List, Optional
from pydantic import BaseModel, Field

# === Rephrased Question ===
class RephrasedQuestion(BaseModel):
    rephrased_question: str = Field(
        description = "The rewritten, clear, context-complete general version of the user's question."
    )
    rag_rephrased_question: str = Field(
        description = "The rewritten question specifically tailored for retrieval-augmented generation (RAG) based document analysis."
    )
    financial_rephrased_question: str = Field(
        description = "The rewritten question specifically tailored for technical indicator analysis."
    )
    technical_rephrased_question: str = Field(
        description = "The rewritten question specifically tailored for general financial question answering, NO ticker."
    )
    tickers: List[Optional[str]] = Field(
        description = "A list of extracted stock tickers in uppercase. Empty if no tickers were found."
    )
    n_days: Optional[int] = Field(
        description = "Number of days user mentioned in the query, if there's nothing mentioned return `none`"
    )
    direction: Optional[Literal["past", "future", "present"]] = Field(
        description = "Whether the user is asking about future, past or present data."
    )

# === Question Classifier ===
class QuestionClassifier(BaseModel):
    models_list: List[Literal[
        "rag_model",
        "normal_financial",
        "indicator_analyst_model",
        "off_topic"
    ]] = Field(
        description = (
            "List of one or more models to use for answering the question.\n"
            "- `rag_model`: Use when the question requires extracting information from financial reports, uploaded documents, or specific metrics in filings.\n"
            "- `normal_financial`: Use for general finance queries not tied to documents. Examples: definitions (ROI, EPS), comparisons, budgeting, investing basics.\n"
            "- `indicator_analyst_model`: Use for advanced technical analysis involving financial indicators.\n"
            "- `off_topic`: Use when the question is unrelated to finance or investing (e.g., jokes, greetings, personal queries, travel, food).\n\n"
            "Rules:\n"
            "1. At least one model must be selected.\n"
            "2. If `off_topic` is chosen, it must be the only item in the list."
        )
    )

# === Error Handling Node ===
class MissingHandler(BaseModel):
    tickers: List[Optional[str]] = Field(description = "A list of tickers extracted from the user's question.")