# Simple Chatbot using NLP and NLTK Intent Recognition

A small web chatbot built with **Python, NLTK, TF-IDF and Flask**.

## How it works
1. `intents.json` holds intents, each with example patterns and responses.
2. User text is cleaned with NLTK: lowercase, tokenize, remove stop words, Porter-stem.
3. Patterns are converted to TF-IDF vectors (`TfidfVectorizer`, 1-2 grams).
4. The user message is vectorized and compared to every pattern with cosine similarity.
5. The best-matching intent is used if its score is above a threshold (0.65), otherwise a fallback reply is sent.

## Run it (one click)
Install Python 3.9+ once from https://www.python.org/downloads/ (on Windows tick "Add Python to PATH"), then double-click:

- **Windows:** `Run_Chatbot.bat`
- **Mac:** `Run_Chatbot.command` (first time: right-click > Open)
- **Linux:** `run.sh`

The first run sets up a private environment and installs the requirements automatically (needs internet, about a minute). After that it starts instantly and opens the chat in your browser. Press Ctrl+C or close the window to stop.

Manual way: `pip install -r requirements.txt` then `python app.py`.
Terminal-only mode: `python chatbot.py`
Repeat the evaluation from the report: `python evaluate.py` (uses `test_sentences.json`)

No NLTK data downloads are needed (regex tokenizer + Porter stemmer).

## Extend it
Add a new object to `intents.json` with a `tag`, `patterns` and `responses`. No code changes needed. Use `{time}` and `{date}` placeholders in responses for live values.

## Structure
```
app.py            Flask server (/ and /chat)
chatbot.py        NLTK preprocessing + TF-IDF intent recognition
intents.json      Training data
templates/index.html   Chat UI
evaluate.py       Accuracy and threshold evaluation (see report, Chapter 6)
test_sentences.json  Unseen test sentences for evaluate.py
launcher.py       One-click setup and start script
Run_Chatbot.bat / .command / run.sh   Double-click launchers
```


## Put it online
See `DEPLOY.md` for free hosting on Render (same Python/Flask project).
