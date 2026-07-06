# Roast Tutor (Free / Local Version)

A Streamlit chatbot that answers student questions correctly — then roasts the
question (not the student) with adjustable intensity. Runs entirely on your
own machine via [Ollama](https://ollama.com) — no API key, no cost.

## Files
- `roast_tutor.py` — the app
- `requirements.txt` — Python dependencies

## Setup

### 1. Install Ollama (one-time)
Download from https://ollama.com/download (Mac, Windows, Linux all supported).

### 2. Pull a model (one-time, downloads to your disk)
```bash
ollama pull llama3.1
```
Smaller/faster alternatives if your machine is limited: `llama3.2`, `phi3`, `mistral`.

### 3. Make sure Ollama is running
It usually starts automatically after install. If not:
```bash
ollama serve
```

### 4. Install Python dependencies
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Run the app
```bash
streamlit run roast_tutor.py
```
Opens at http://localhost:8501.

## Usage
1. Confirm the model name in the sidebar matches what you pulled (e.g. `llama3.1`).
2. Optionally set a subject so answers are scoped to it.
3. Pick a roast intensity, 1 (gentle) to 5 (merciless).
4. Ask a question in the chat box.

## Notes / trade-offs vs. paid API
- **Cost:** $0, runs entirely offline once the model is downloaded.
- **Quality:** noticeably below Claude/GPT-4-class models, especially on harder
  academic questions — verify accuracy before trusting it for real coursework.
- **Speed:** depends entirely on your hardware (CPU/GPU/RAM); can be slow on
  low-end machines.
- **Roasting always targets the question/reasoning**, never identity or
  anything unrelated to the academic content — but a local small model is less
  reliable at following that instruction consistently than a larger hosted
  model, so keep an eye on outputs, especially at intensity 4-5.
