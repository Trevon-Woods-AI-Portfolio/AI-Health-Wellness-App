from pydantic import BaseModel
from langchain_core.documents import Document
from typing import List, Dict, Optional

class UserState(BaseModel):
    query: str
    heart_rate: str
    mood: str
    did_exercise: str
    sleep_description: str
    synopsis: Optional[str] = None
    retrieved_docs: Optional[List[Document]] = None
    docs_dict: Optional[Dict[str, List[Document]]] = None
    advice: Optional[str] = None