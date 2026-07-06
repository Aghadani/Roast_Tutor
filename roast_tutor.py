"""
Roast Tutor — a Streamlit chatbot that answers student questions correctly,
but roasts the student a little (or a lot) while doing it.

Backend: Ollama (free, runs locally, no API key, no per-token cost).

Setup:
    1. Install Ollama: https://ollama.com/download
    2. Pull a model:     ollama pull llama3.1
    3. Make sure Ollama is running (it starts automatically after install,
       or run `ollama serve`)
    4. pip install -r requirements.txt
    5. streamlit run roast_tutor.py
"""

import json
import requests
import streamlit as st

st.set_page_config(page_title="Roast Tutor", page_icon="🔥", layout="centered")

OLLAMA_URL = "http://localhost:11434"

# ---------- Sidebar: config ----------
st.sidebar.title("⚙️ Settings")

model_name = st.sidebar.text_input(
    "Ollama model",
    value="llama3.1",
    help="Must match a model you've pulled with `ollama pull <model>`. "
         "Smaller/faster options: llama3.2, phi3, mistral.",
)
roast_level = st.sidebar.slider(
    "Roast intensity", 1, 5, 3,
    help="1 = gentle teasing, 5 = merciless. The answer is always correct regardless of setting."
)
subject = st.sidebar.text_input("Subject (optional)", placeholder="e.g. Calculus, Python, History")

if st.sidebar.button("Clear chat"):
    st.session_state.messages = []

st.sidebar.divider()
st.sidebar.caption(
    "Free & local via [Ollama](https://ollama.com) — no API key, no cost. "
    "Ollama must be running on this machine."
)

st.title("🔥 Roast Tutor")
st.caption("Get your question answered. Get your ego lightly (or heavily) destroyed. 100% free, runs locally.")

# ---------- System prompt scales with roast_level ----------
ROAST_DESCRIPTIONS = {
    1: "Add one light, friendly tease. Keep it warm — this should feel like a fun nudge, not an insult.",
    2: "Add mild sarcasm or a gentle jab about the question, but stay encouraging overall.",
    3: "Roast the question or the student's approach with witty, sharp humor. Be funny, not cruel.",
    4: "Roast harder — sarcastic, blunt, comedic-insult style, like a strict but hilarious professor.",
    5: "Go full savage roast comedian mode. Merciless, exaggerated insults about the question — "
       "but never about the student's identity, intelligence in a demeaning clinical sense, or anything "
       "that isn't about the question/reasoning itself.",
}

SYSTEM_PROMPT = f"""You are Roast Tutor, an educational chatbot for students{f" studying {subject}" if subject else ""}.

Rules, in order of priority:
1. ALWAYS give a fully correct, clear, complete answer to the student's academic question first. 
   Accuracy is never sacrificed for comedy.
2. After (or woven into) the correct answer, roast the student's question, mistake, or approach 
   with humor. Roast intensity level: {roast_level}/5 — {ROAST_DESCRIPTIONS[roast_level]}
3. Never roast protected characteristics, appearance, family, or anything unrelated to the academic 
   content of the question. Keep it about the work, not the person.
4. If the student seems genuinely upset, confused to the point of distress, or asks you to stop 
   roasting, drop the act immediately and just help normally.
5. Keep responses focused — a real answer wrapped in comedy, not comedy that buries the answer.
"""


def check_ollama_running() -> bool:
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        return r.status_code == 200
    except requests.exceptions.RequestException:
        return False


def stream_ollama_response(model: str, messages: list):
    """Yields text chunks from Ollama's streaming chat endpoint."""
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        "stream": True,
    }
    with requests.post(f"{OLLAMA_URL}/api/chat", json=payload, stream=True, timeout=120) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line:
                continue
            chunk = json.loads(line)
            if "message" in chunk and "content" in chunk["message"]:
                yield chunk["message"]["content"]
            if chunk.get("done"):
                break


# ---------- Chat state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

if not check_ollama_running():
    st.error(
        "Can't reach Ollama at localhost:11434. Install it from "
        "https://ollama.com/download, then run `ollama pull llama3.1` and make "
        "sure Ollama is running before asking a question."
    )

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask your question...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""
        try:
            for chunk in stream_ollama_response(model_name, st.session_state.messages):
                full_text += chunk
                placeholder.markdown(full_text + "▌")
            placeholder.markdown(full_text)
        except requests.exceptions.RequestException as e:
            full_text = (
                f"Couldn't reach Ollama ({e}). Make sure it's running and that "
                f"`{model_name}` has been pulled with `ollama pull {model_name}`."
            )
            placeholder.error(full_text)

    st.session_state.messages.append({"role": "assistant", "content": full_text})
