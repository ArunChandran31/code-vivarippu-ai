# backend/utils.py
import json, re

def safe_extract_json(text: str):
    try:
        cleaned = re.sub(r"```[a-zA-Z]*", "", text)
        m = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", cleaned)
        if not m:
            return None
        candidate = m.group(1)
        return json.loads(candidate)
    except Exception:
        # fallback: remove trailing commas
        try:
            cand = re.sub(r",\s*([}\]])", r"\1", candidate)
            return json.loads(cand)
        except Exception:
            return None
