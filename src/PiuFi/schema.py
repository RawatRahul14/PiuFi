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
    technical_rephrased_question: str =Field(
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