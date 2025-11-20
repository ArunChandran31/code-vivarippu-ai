# backend/app.py
import os
import traceback
import asyncio
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analyzers.analyzer import analyze_code
from ai_engine import ai_review
from db import init_db, get_db
from auth import verify_firebase_token


MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    print("WARNING: MONGO_URI missing in .env")

init_db(MONGO_URI)


app = FastAPI(title="Code Reviewer AI – Stable Edition")

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
origins = [o.strip() for o in origins if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReviewRequest(BaseModel):
    code: str
    language: str | None = None


async def _call_verify_token(token: str):
    try:
        result = verify_firebase_token(token)
        if hasattr(result, "__await__"):
            return await result   # async version
        return result             # sync version
    except:
        return None


def _extract_bearer(auth: str | None):
    if not auth:
        return None
    parts = auth.strip().split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None


async def get_current_user(authorization: str | None = Header(None)):
    token = _extract_bearer(authorization)
    if not token:
        return None
    return await _call_verify_token(token)


@app.post("/api/review")
async def review(req: ReviewRequest, user=Depends(get_current_user)):

    # 1) Static analysis (safe for sync/async)
    static = analyze_code(req.code, req.language)
    if asyncio.iscoroutine(static):
        static = await static

    chosen_language = static.get("language_detected") or req.language

    # 2) AI analysis
    try:
        ai_resp, usage = await ai_review(req.code, chosen_language)
    except Exception as e:
        print("\n--------- AI ENGINE ERROR ---------")
        print(traceback.format_exc())
        print("-----------------------------------\n")
        raise HTTPException(status_code=500, detail=f"AI Engine Error: {str(e)}")

    # compute token usage (fallback for Groq which may not return exact numbers)
    input_tokens = usage.get("input_tokens", 0) if isinstance(usage, dict) else 0
    output_tokens = usage.get("output_tokens", 0) if isinstance(usage, dict) else 0
    token_usage = int(input_tokens) + int(output_tokens)

    # 3) Save to DB
    try:
        db = get_db()
        doc = {
            "user": user.get("uid") if user else None,
            "email": user.get("email") if user else None,
            "code": req.code,
            "language": chosen_language,
            "static": static,
            "ai": ai_resp,
            "usage": usage,
            "token_usage": token_usage,
            "created_at": datetime.utcnow(),
        }
        await db["reviews"].insert_one(doc)
    except Exception as e:
        print("\n--------- DB INSERT ERROR ---------")
        print(traceback.format_exc())
        print("----------------------------------\n")
        raise HTTPException(status_code=500, detail=f"DB insert failed: {str(e)}")

    return {"static": static, "ai": ai_resp, "usage": usage}


@app.get("/api/reviews")
async def list_reviews(user=Depends(get_current_user)):
    db = get_db()
    query = {"user": user.get("uid")} if user else {}
    docs = await db["reviews"].find(query).sort("created_at", -1).to_list(100)
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs


@app.get("/health")
def health():
    return {
        "status": "ok",
        "provider": os.getenv("MODEL_PROVIDER", "mock"),
    }

@app.get("/api/usage")
async def usage():
    db = get_db()
    total_reviews = await db.reviews.count_documents({})

    token_sum = 0
    async for doc in db.reviews.find({}, {"token_usage": 1}):
        token_sum += int(doc.get("token_usage", 0) or 0)

    cost_inr = (token_sum / 1000) * 0.06  #6 paisa per 1K tokens

    return {
        "total_reviews": total_reviews,
        "total_tokens": token_sum,
        "cost_inr": cost_inr,
        "last_updated": "now",
    }
