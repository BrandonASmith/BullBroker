from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai_engine import generate_stock_pick_rationale
import uvicorn

app = FastAPI()

# CORS setup to allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "ok"}

from ai_engine import generate_stock_pick_rationale

@app.get("/daily-pick")
def daily_pick():
    result = generate_stock_pick_rationale()
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
