from modules.api_client import get_client, MODEL

def generate_summary(text):
    client = get_client()
    prompt = f"Read this research paper and write a clear summary in 5-7 sentences covering the main topic, methodology, and findings:\n\n{text[:6000]}"
  msg = client.chat.completions.create(model=MODEL, max_tokens=800, messages=[{"role":"user","content":prompt}])
   return msg.choices[0].message.content

def extract_insights(text):
    client = get_client()
    prompt = f"List the 5 most important insights from this research paper as numbered points:\n\n{text[:6000]}"
    msg = client.messages.create(model=MODEL, max_tokens=800, messages=[{"role":"user","content":prompt}])
    return msg.content[0].text

def detect_gaps(text):
    client = get_client()
    prompt = f"Identify 4-5 research gaps or limitations mentioned or implied in this paper as numbered points:\n\n{text[:6000]}"
    msg = client.messages.create(model=MODEL, max_tokens=800, messages=[{"role":"user","content":prompt}])
    return msg.content[0].text

def generate_hypotheses(text):
    client = get_client()
    prompt = f"Based on this research paper, suggest 4-5 new hypotheses or future research directions as numbered points:\n\n{text[:6000]}"
    msg = client.messages.create(model=MODEL, max_tokens=800, messages=[{"role":"user","content":prompt}])
    return msg.content[0].text

# Aliases for compatibility
generate_insights = extract_insights
detect_research_gaps = detect_gaps
