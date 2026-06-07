from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Sentiment API is running"}

@app.post("/sentiment")
async def sentiment(data: dict = Body(...)):

    sentences = data.get("sentences", [])

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

    for sentence in sentences:
        text = sentence.lower()

        pos = sum(word in text for word in positive_words)
        neg = sum(word in text for word in negative_words)

        if pos > neg:
            label = "happy"
        elif neg > pos:
            label = "sad"
        else:
            label = "neutral"

        results.append({
            "sentence": sentence,
            "sentiment": label
        })

    return {"results": results}
