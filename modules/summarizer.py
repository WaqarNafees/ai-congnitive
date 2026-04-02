import re
from modules.api_client import get_client, MODEL

def _ask(prompt):
    try:
        client = get_client()
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error: {e}]"

def _cut(text):
    words = text.split()
    return " ".join(words[:3000]) if len(words) > 3000 else text

def _parse(text):
    items = []
    for line in text.strip().splitlines():
        line = re.sub(r"^[\d]+[.)]\s*|^[-*•]\s*", "", line.strip()).strip()
        if line:
            items.append(line)
    return items

def generate_summary(text, max_tokens=600):
    return _ask(f"Summarize this research paper. Include Objective, Methods, Key Findings, Conclusions.\n\n{_cut(text)}")

def extract_insights(text):
    return _parse(_ask(f"Extract 5 to 8 key insights from this paper. Numbered list only.\n\n{_cut(text)}"))

def detect_research_gaps(text):
    return _parse(_ask(f"Identify 4 to 6 research gaps in this paper. Numbered list only.\n\n{_cut(text)}"))

def generate_hypotheses(text, n=3):
    return _parse(_ask(f"Generate {n} novel hypotheses based on this paper. Numbered list only.\n\n{_cut(text)}"))[:n]
