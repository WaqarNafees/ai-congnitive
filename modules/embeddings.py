import re

class EmbeddingStore:
    def __init__(self):
        self.chunks = []

    def build(self, text):
        words = text.split()
        self.chunks = [" ".join(words[i:i+400]) for i in range(0, len(words), 320)]

    def retrieve(self, query, top_k=5):
        query_words = set(re.findall(r"\w+", query.lower()))
        scored = []
        for chunk in self.chunks:
            chunk_words = set(re.findall(r"\w+", chunk.lower()))
            score = len(query_words & chunk_words)
            scored.append((score, chunk))
        scored.sort(key=lambda x: -x[0])
        return "\n\n".join([c for _, c in scored[:top_k]])
