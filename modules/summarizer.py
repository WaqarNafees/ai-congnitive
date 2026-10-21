from modules.api_client import get_client, MODEL

def generate_summary(text):
    client = get_client()
    prompt = f"Summarize this research paper in 5-7 sentences:\n\n{text[:6000]}"
    msg = client.chat.completions.create(model=MODEL, max_tokens=800, messages=[{"role":"user","content":prompt}])
    return msg.choices[0].message.content

def extract_insights(text):
    client = get_client()
    prompt = f"List 5 key insights from this research paper as numbered points:\n\n{text[:6000]}"
    msg = client.chat.completions.create(model=MODEL, max_tokens=800, messages=[{"role":"user","content":prompt}])
    return msg.choices[0].message.content

def detect_gaps(text):
    client = get_client()
    prompt = f"Identify 4-5 research gaps or limitations in this paper as numbered points:\n\n{text[:6000]}"
    msg = client.chat.completions.create(model=MODEL, max_tokens=800, messages=[{"role":"user","content":prompt}])
    return msg.choices[0].message.content

def generate_hypotheses(text):
    client = get_client()
    prompt = f"Suggest 4-5 future research directions based on this paper as numbered points:\n\n{text[:6000]}"
    msg = client.chat.completions.create(model=MODEL, max_tokens=800, messages=[{"role":"user","content":prompt}])
    return msg.choices[0].message.content

generate_insights = extract_insights
detect_research_gaps = detect_gaps
