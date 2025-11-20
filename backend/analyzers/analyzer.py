# backend/analyzers/analyzer.py
import ast
from radon.complexity import cc_visit
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound
import os
from openai import AsyncOpenAI

def analyze_code(code: str, language_hint: str | None = None):
    info = {"lines": len(code.splitlines()), "language_detected": None}
    # language detection
    detected = language_hint or None
    if not detected:
        try:
            lexer = guess_lexer(code)
            detected = lexer.name.lower()
        except ClassNotFound:
            detected = None
    info["language_detected"] = detected

    # python deep checks
    if detected and "python" in detected:
        try:
            ast.parse(code)
            blocks = cc_visit(code)
            complexities = [{"name": b.name, "complexity": b.complexity, "lineno": b.lineno} for b in blocks]
            avg = sum(b["complexity"] for b in complexities) / len(complexities) if complexities else 0
            info.update({"syntax_valid": True, "complexities": complexities, "avg_complexity": avg})
        except Exception as e:
            info.update({"syntax_valid": False, "error": str(e)})
    else:
        info.update({"syntax_valid": None, "message": "Shallow/static checks for this language not implemented yet."})
    return info

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def analyze_code(code: str, language: str):
    prompt = f"""
    You are an AI code reviewer. Analyze the following {language} code and give:
    - issues
    - bugs
    - security risks
    - improvements
    - optimized version

    CODE:
    {code}
    """

    response = await client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content