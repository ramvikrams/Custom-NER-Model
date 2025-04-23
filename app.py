from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from transformers import pipeline
from pathlib import Path

app = FastAPI()

# Load the trained model
model_checkpoint = "./checkpoint-5268"
token_classifier = pipeline("token-classification", model=model_checkpoint, aggregation_strategy="simple")

# Serve static files (like CSS, JavaScript)
app.mount("/static", StaticFiles(directory="static"), name="static")

class TextRequest(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def serve_homepage():
    html_path = Path("static/index.html").read_text()
    return HTMLResponse(content=html_path)

@app.post("/predict/")
async def predict(request: TextRequest):
    text = request.text
    results = token_classifier(text)

    entities = [
        {"word": entity["word"], "entity": entity["entity_group"]}
        for entity in results
    ]

    return JSONResponse(content={"entities": entities})
