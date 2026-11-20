# Put the chatbot online (free) with Render

Same project: Python + NLTK + TF-IDF + Flask. Nothing is rewritten.

1. Create a free account at https://github.com and make a new repository (e.g. `nlp-chatbot`).
2. Upload ALL files of this folder to it (drag and drop in "Add file > Upload files").
   Keep the `templates` folder. Do not upload a `.venv` folder.
3. Create a free account at https://render.com (sign in with GitHub).
4. Click New > Web Service and pick your `nlp-chatbot` repository.
5. Use these settings:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Instance type: Free
   - Environment variable: `PYTHON_VERSION` = `3.12.7`
6. Click Create Web Service and wait 3-5 minutes. Render shows your link,
   for example https://nlp-chatbot.onrender.com

Notes
- The free plan sleeps after ~15 minutes without visitors; the first open
  after that takes about a minute. Open it before your presentation.
- Locally, nothing changes: double-click Run_Chatbot.bat.
