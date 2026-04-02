from modules.api_client import get_client, MODEL

def answer_question(question, context):
    try:
        client = get_client()
        prompt = f"Answer based only on this paper context.\n\nCONTEXT:\n{context}\n\nQUESTION: {question}\n\nAnswer:"
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error: {e}]"
