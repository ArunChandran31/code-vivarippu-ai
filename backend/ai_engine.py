# backend/ai_engine.py
import os
import json
import re
import httpx
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("MODEL_PROVIDER", "mock").lower().strip()

# ---------------------------------------------------------
# PROMPT BUILDER (FIXED – now includes the actual code)
# ---------------------------------------------------------
def build_prompt(code: str, language: str) -> str:
    return f"""
You are an expert senior software engineer.

Analyze the following {language} code and return ONLY a JSON object with:
- summary
- issues
- complexity
- suggestions
- style

Code:

Respond ONLY with a JSON object. No explanation outside JSON.
"""


# ---------------------------------------------------------
# JSON Extractor (safe fallback)
# ---------------------------------------------------------
def extract_json(text: str):
    try:
        block = re.search(r"\{[\s\S]*\}", text)
        if not block:
            return {"summary": text}
        return json.loads(block.group(0))
    except Exception:
        return {"summary": text}


# =========================================================
# MOCK MODE (FREE)
# =========================================================
async def review_mock(code, language):
    fake = {
        "summary": f"This is mock analysis for {language}.",
        "issues": ["No issues detected (mock)."],
        "complexity": "O(n) (mock)",
        "suggestions": ["Improve variable naming (mock)."],
        "style": ["Use consistent indentation (mock)."]
    }
    usage = {"provider": "mock", "input_tokens": 0, "output_tokens": 0}
    return fake, usage


# =========================================================
# OPENAI
# =========================================================
async def review_openai(code, language):
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = build_prompt(code, language)

    response = await client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=1200
    )

    text = response.choices[0].message.content
    data = extract_json(text)

    usage = {
        "provider": "openai",
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens
    }
    return data, usage


# =========================================================
# CLAUDE (Anthropic)
# =========================================================
async def review_claude(code, language):
    client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = build_prompt(code, language)

    response = await client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229"),
        max_tokens=1400,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text
    data = extract_json(text)

    usage = {
        "provider": "claude",
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }
    return data, usage


# =========================================================
# GROQ – Llama-3 (FREE)
# =========================================================
async def review_groq(code, language):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": os.getenv("GROQ_MODEL", "llama3-70b-versatile"),
        "messages": [{"role": "user", "content": build_prompt(code, language)}],
        "temperature": 0,
        "max_tokens": 1400
    }

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        res = r.json()

    text = res["choices"][0]["message"]["content"]
    data = extract_json(text)

    usage = {
        "provider": "groq",
        "input_tokens": res.get("usage", {}).get("prompt_tokens", 0),
        "output_tokens": res.get("usage", {}).get("completion_tokens", 0),
    }
    return data, usage


# =========================================================
# MAIN ROUTER FUNCTION
# =========================================================
async def ai_review(code, language):
    # Direct mode selection
    if PROVIDER == "mock":
        return await review_mock(code, language)
    if PROVIDER == "openai":
        return await review_openai(code, language)
    if PROVIDER == "claude":
        return await review_claude(code, language)
    if PROVIDER == "groq":
        return await review_groq(code, language)

    # Fallback chain
    for engine in [review_openai, review_claude, review_groq, review_mock]:
        try:
            return await engine(code, language)
        except Exception:
            continue

    return await review_mock(code, language)
