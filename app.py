from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.api_route("/", methods=["GET", "POST", "HEAD"])
async def root():
    return {"message": "Sentiment API is running"}


@app.post("/sentiment")
async def sentiment(data: dict = Body(...)):

    sentences = data.get("sentences", [])

    positive_words = {
        "love", "loved", "like", "liked", "great", "good",
        "excellent", "awesome", "amazing", "happy", "fantastic",
        "wonderful", "best", "nice", "perfect", "enjoy",
        "enjoyed", "brilliant", "outstanding", "delight",
        "delighted", "pleased", "joy", "joyful", "positive",
        "superb", "excited", "satisfied", "success",
        "successful", "recommend", "recommended", "beautiful",
        "favorite", "favourite", "excellent", "glad",
        "cheerful", "smile", "smiling", "pleasant"
    }

    negative_words = {
        "hate", "hated", "bad", "terrible", "awful", "sad",
        "worst", "horrible", "angry", "poor", "disappointed",
        "disappointing", "boring", "annoying", "useless",
        "frustrating", "frustrated", "miserable", "negative",
        "unhappy", "upset", "depressing", "depressed",
        "disaster", "pathetic", "waste", "failure",
        "failed", "broken", "problem", "problems",
        "issue", "issues", "wrong", "hate", "cry",
        "crying", "regret", "regretted", "unfortunate",
        "dreadful", "nasty", "tragic"
    }

    results = []

    for sentence in sentences:

        words = re.findall(r"\b\w+\b", sentence.lower())

        positive_score = sum(
            1 for word in words if word in positive_words
        )

        negative_score = sum(
            1 for word in words if word in negative_words
        )

        if positive_score > negative_score:
            sentiment_label = "happy"

        elif negative_score > positive_score:
            sentiment_label = "sad"

        else:
            sentiment_label = "neutral"

        results.append({
            "sentence": sentence,
            "sentiment": sentiment_label
        })

    return {"results": results}
