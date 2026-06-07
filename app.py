from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from textblob import TextBlob

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

    results = []

    positive_keywords = {
        "love", "great", "excellent", "amazing", "wonderful",
        "fantastic", "awesome", "happy", "delighted", "pleased",
        "best", "good", "brilliant", "outstanding", "perfect",
        "enjoy", "enjoyed", "nice", "superb", "recommend"
    }

    negative_keywords = {
        "hate", "terrible", "awful", "horrible", "worst",
        "sad", "angry", "disappointed", "frustrating",
        "miserable", "bad", "poor", "annoying", "boring",
        "useless", "upset", "depressed", "disaster", "failure"
    }

    for sentence in sentences:
        text = sentence.lower()

        # Keyword override
        if any(word in text for word in positive_keywords):
            label = "happy"

        elif any(word in text for word in negative_keywords):
            label = "sad"

        else:
            polarity = TextBlob(sentence).sentiment.polarity

            if polarity > 0:
                label = "happy"
            elif polarity < 0:
                label = "sad"
            else:
                label = "neutral"

        results.append({
            "sentence": sentence,
            "sentiment": label
        })

    return {"results": results}
