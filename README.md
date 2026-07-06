# Roast Tutor (Free, Cloud-Hosted via Groq)

A Streamlit chatbot that answers student questions correctly — then roasts the
question (not the student) with adjustable intensity. Uses
[Groq](https://groq.com)'s free hosted API — no local install, no cost for
normal use.

## Files
- `roast_tutor.py` — the app
- `requirements.txt` — Python dependencies

## Setup

### 1. Get a free Groq API key
Sign up at https://console.groq.com/keys — free tier, no credit card required.
Copy the key.

### 2. Install Python dependencies
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run roast_tutor.py
```
Opens at http://localhost:8501.

## Usage
1. Paste your Groq API key into the sidebar.
2. Pick a model — `llama-3.1-8b-instant` is fast and fine for most questions;
   `llama-3.3-70b-versatile` is smarter but slower and hits rate limits sooner.
3. Optionally set a subject so answers are scoped to it.
4. Pick a roast intensity, 1 (gentle) to 5 (merciless).
5. Ask a question in the chat box.

## Notes / trade-offs
- **Cost:** $0 on Groq's free tier for normal personal/small-class use.
- **Rate limits:** free tier has per-minute and per-day request/token caps —
  fine for one person or a small group, not for hundreds of concurrent students.
  Check current limits at https://console.groq.com/settings/limits since they
  change over time.
- **Quality:** open Llama/Gemma models — solid for most schoolwork, but verify
  answers on harder or more specialized material before trusting them fully.
- **Your API key is entered locally in the sidebar each session** — it isn't
  stored anywhere by this app.
