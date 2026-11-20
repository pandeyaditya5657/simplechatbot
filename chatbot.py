"""NLP engine: NLTK preprocessing + TF-IDF intent recognition."""
import json
import random
import re
from datetime import datetime
from pathlib import Path

from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).parent

# These NLTK components need no downloaded corpora, so the bot works offline.
_tokenizer = RegexpTokenizer(r"[a-z0-9]+")
_stemmer = PorterStemmer()

# Small stop-word list. Question words (what, how, who, you, me...) are
# deliberately kept because they carry intent.
_stop = {
    "a", "an", "the", "and", "or", "but", "of", "to", "in", "on", "at", "for",
    "with", "about", "it", "its", "this", "that", "these", "those", "be", "am",
    "are", "was", "were", "been", "my", "your", "i", "so", "very", "just",
    "some", "any", "please", "s", "t", "should", "would", "could", "good", "there",
    "going", "like", "want", "need", "way", "thing", "something", "into", "from",
    "when", "where", "ever", "also", "really",
}


# Generic words that appear in almost every question. A message must share at
# least one NON-generic word with the known patterns, otherwise "what is
# photosynthesis" would match any "what is ..." pattern.
_generic = {
    "what", "is", "explain", "tell", "me", "define", "meaning", "how", "does",
    "do", "can", "difference", "between", "vs", "example", "give", "show",
    "which", "why", "mean", "doe", "ha", "stand", "use", "you", "who",
}


def preprocess(text: str) -> str:
    # "hiii", "heyyy", "helloooo" -> squeeze 3+ repeated letters to one
    text = re.sub(r"([a-z])\1{2,}", r"\1", text.lower())
    tokens = _tokenizer.tokenize(text)
    tokens = [_stemmer.stem(t) for t in tokens if t not in _stop]
    content = [t for t in tokens if t not in _generic]
    return " ".join(content or tokens)


class Chatbot:
    def __init__(self, intents_path=BASE_DIR / "intents.json", threshold=0.4):
        with open(intents_path, encoding="utf-8") as f:
            data = json.load(f)
        self.intents = {i["tag"]: i for i in data["intents"]}
        self.fallback = data["fallback"]
        self.threshold = threshold

        self.patterns, self.tags = [], []
        for intent in data["intents"]:
            for p in intent["patterns"]:
                self.patterns.append(preprocess(p))
                self.tags.append(intent["tag"])

        # word 1-2 grams help short phrases like "tf idf"
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform(self.patterns)
        self.vocab = {w for p in self.patterns for w in p.split()}

    def predict_intent(self, message: str):
        cleaned = preprocess(message)
        if not cleaned:
            return None, 0.0
        words = cleaned.split()
        known = [w for w in words if w in self.vocab]
        # every word is unknown -> nothing to match on
        if not known:
            return None, 0.0
        # penalise unknown words so "translate hello into french" is not a greeting
        ratio = len(known) / len(words)
        vec = self.vectorizer.transform([cleaned])
        scores = cosine_similarity(vec, self.matrix)[0]
        best = int(scores.argmax())
        return self.tags[best], float(scores[best]) * ratio

    def respond(self, message: str, client_time: str = "", client_date: str = "") -> dict:
        """client_time / client_date come from the user's browser so answers
        show the USER's local time, not the (often UTC) server clock."""
        tag, score = self.predict_intent(message)
        if tag is None or score < self.threshold:
            return {"reply": random.choice(self.fallback), "intent": "fallback", "confidence": round(score, 2)}
        reply = random.choice(self.intents[tag]["responses"])
        now = datetime.now()
        time_text = client_time or now.strftime("%I:%M %p")
        date_text = client_date or now.strftime("%A, %d %B %Y")
        reply = reply.replace("{time}", time_text).replace("{date}", date_text)
        return {"reply": reply, "intent": tag, "confidence": round(score, 2)}


if __name__ == "__main__":
    bot = Chatbot()
    print("Chatbot ready. Type 'quit' to exit.")
    while True:
        msg = input("You: ").strip()
        if msg.lower() in {"quit", "exit"}:
            break
        r = bot.respond(msg)
        print(f"Bot [{r['intent']} {r['confidence']}]: {r['reply']}")
