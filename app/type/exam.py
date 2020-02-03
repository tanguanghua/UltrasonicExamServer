from typing import List
from pydantic import BaseModel


class TAnnotation(BaseModel):
    id: int
    bodyPart: str
    annotations: any


class TCheckExamResult(BaseModel):
    user_id: int
    annotations: List[TAnnotation]
