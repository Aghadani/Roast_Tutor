# Roast Tutor

A Streamlit chatbot that answers student questions correctly — then roasts the
question (not the student) with adjustable intensity.

## Files
- `roast_tutor.py` — the app
- `requirements.txt` — dependencies

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
streamlit run roast_tutor.py
```

This opens the app in your browser (usually http://localhost:8501).

## Usage
1. Paste your Anthropic API key into the sidebar (get one at
   https://console.anthropic.com/). It's only used for your local session —
   nothing is stored or sent anywhere else.
2. Optionally set a subject (e.g. "Calculus") so answers are scoped to it.
3. Pick a roast intensity, 1 (gentle) to 5 (merciless).
4. Ask a question in the chat box.

## Notes
- The model always gives a correct, complete answer first — the roast is
  layered on, not a substitute for the real answer.
- Roasting targets the question/reasoning, never identity, appearance, or
  anything unrelated to the academic content.
- If a student seems genuinely distressed, the bot is instructed to drop the
  act and just help.
- Your API key is billed per Anthropic's standard API pricing — check
  console.anthropic.com for current rates before heavy classroom use.
