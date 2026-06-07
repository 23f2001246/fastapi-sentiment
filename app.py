from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: List[str]


@app.get("/")
async def root():
    return {"message": "Sentiment API is running"}


@app.post("/sentiment")
async def sentiment(request: SentimentRequest):

    positive_words = {
        "love", "great", "good", "excellent", "awesome",
        "amazing", "happy", "fantastic", "wonderful",
        "best", "nice", "perfect", "liked", "enjoy",
        "enjoyed", "brilliant", "outstanding"
    }

    negative_words = {
        "hate", "bad", "terrible", "awful", "sad",
        "worst", "horrible", "angry", "poor",
        "disappointed", "disappointing", "boring",
        "annoying", "useless", "frustrating"
    }

    results = []

    for sentence in request.sentences:

        text = sentence.lower()

        positive_score = sum(
            word in text for word in positive_words
        )

        negative_score = sum(
            word in text for word in negative_words
        )

        if positive_score > negative_score:
            label = "happy"
        elif negative_score > positive_score:
            label = "sad"
        else:
            label = "neutral"

        results.append({
            "sentence": sentence,
            "sentiment": label
        })

    return {"results": results}