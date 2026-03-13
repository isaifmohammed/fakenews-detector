from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_text(text):
    text = text[:2000]
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"""Analyze this news text and determine if it is FAKE or REAL news.

Text: {text}

Respond in this exact format only:
VERDICT: FAKE or REAL
CONFIDENCE: a percentage like 95%
REASON: one short sentence explaining why

Nothing else."""
            }
        ],
        max_tokens=200
    )
    
    response_text = response.choices[0].message.content.strip()
    lines = response_text.split('\n')
    
    verdict_line = lines[0] if len(lines) > 0 else "VERDICT: REAL"
    confidence_line = lines[1] if len(lines) > 1 else "CONFIDENCE: 50%"
    reason_line = lines[2] if len(lines) > 2 else "REASON: Unable to determine"
    
    verdict = "FAKE" if "FAKE" in verdict_line else "REAL"
    confidence = confidence_line.replace("CONFIDENCE:", "").strip()
    reason = reason_line.replace("REASON:", "").strip()
    
    if verdict == "FAKE":
        return {
            "verdict": "FAKE NEWS ⚠️",
            "confidence": confidence,
            "reason": reason,
            "label": "fake"
        }
    else:
        return {
            "verdict": "REAL NEWS ✅",
            "confidence": confidence,
            "reason": reason,
            "label": "real"
        }