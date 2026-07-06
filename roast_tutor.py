import json
import requests
import streamlit as st

st.set_page_config(page_title="Roast Tutor", page_icon="🔥", layout="centered")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

#Sidebar: config 
st.sidebar.title("⚙️ Settings")

api_key = st.sidebar.text_input(
    "Groq API key",
    type="password",
    help="Free get one at https://console.groq.com/keys (no credit card required).",
)
model_name = st.sidebar.selectbox(
    "Model",
    ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "gemma2-9b-it"],
    help="All free on Groq's free tier. 70b is smarter but slower/more rate-limited.",
)
roast_level = st.sidebar.slider(
    "Roast intensity", 1, 5, 3,
    help="1 = gentle teasing, 5 = merciless. The answer is always correct regardless of setting."
)
subject = st.sidebar.text_input("Subject (optional)", placeholder="e.g. Calculus, Python, History")

if st.sidebar.button("Clear chat"):
    st.session_state.messages = []

st.sidebar.divider()
# st.sidebar.caption(
#     "Runs on [Groq](https://groq.com)'s free hosted API no local install needed."
# )

st.title("🔥 Roast Tutor")
st.caption("Get your question answered. Get your ego lightly (or heavily) destroyed. Free, cloud-hosted.")

#System prompt scales with roast_level
ROAST_DESCRIPTIONS = {
    1: "Add one light, friendly tease. Keep it warm — this should feel like a fun nudge, not an insult.",
    2: "Add mild sarcasm or a gentle jab about the question, but stay encouraging overall.",
    3: "Roast the question or the student's approach with witty, sharp humor. Be funny, not cruel.",
    4: "Roast harder sarcastic, blunt, comedic-insult style, like a strict but hilarious professor.",
    5: "Go full savage roast comedian mode. Merciless, exaggerated insults about the question "
       "but never about the student's identity, intelligence in a demeaning clinical sense, or anything "
       "that isn't about the question/reasoning itself.",
}

SYSTEM_PROMPT = f"""You are Roast Tutor, an educational chatbot for students{f" studying {subject}" if subject else ""}.

Rules, in order of priority:
1. ALWAYS give a fully correct, clear, complete answer to the student's academic question first. 
   Accuracy is never sacrificed for comedy.
2. After (or woven into) the correct answer, roast the student's question, mistake, or approach 
   with humor. Roast intensity level: {roast_level}/5 {ROAST_DESCRIPTIONS[roast_level]}
3. Never roast protected characteristics, appearance, family, or anything unrelated to the academic 
   content of the question. Keep it about the work, not the person.
4. If the student seems genuinely upset, confused to the point of distress, or asks you to stop 
   roasting, drop the act immediately and just help normally.
5. Keep responses focused a real answer wrapped in comedy, not comedy that buries the answer.
"""


def stream_groq_response(api_key: str, model: str, messages: list):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        "stream": True,
        "max_tokens": 800,
    }
    with requests.post(GROQ_URL, headers=headers, json=payload, stream=True, timeout=60) as resp:
        if resp.status_code != 200:
            raise RuntimeError(f"Groq API error {resp.status_code}: {resp.text[:300]}")
        for line in resp.iter_lines():
            if not line:
                continue
            line = line.decode("utf-8")
            if not line.startswith("data: "):
                continue
            data = line[len("data: "):]
            if data.strip() == "[DONE]":
                break
            chunk = json.loads(data)
            delta = chunk["choices"][0]["delta"]
            if "content" in delta and delta["content"]:
                yield delta["content"]


#Chat state
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask your question...")

if prompt:
    if not api_key:
        st.error("Add your free Groq API key in the sidebar first (console.groq.com/keys).")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""
        try:
            for chunk in stream_groq_response(api_key, model_name, st.session_state.messages):
                full_text += chunk
                placeholder.markdown(full_text + "▌")
            placeholder.markdown(full_text)
        except Exception as e:
            full_text = f"Error calling Groq API: {e}"
            placeholder.error(full_text)

    st.session_state.messages.append({"role": "assistant", "content": full_text})
