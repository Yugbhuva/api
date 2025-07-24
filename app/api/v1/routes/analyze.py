from fastapi import APIRouter
from pydantic import BaseModel
from collections import Counter

router = APIRouter()

class AnalyzeRequest(BaseModel):
    text: str

@router.post("/analyze")
async def analyze_text(data: AnalyzeRequest):
    text = data.text
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    word_freq = dict(Counter(words))

    return {
        "word_count": word_count,
        "char_count": char_count,
        "word_frequency": word_freq
    }