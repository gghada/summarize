# 🧠 Research Paper Summarizer

A simple desktop application that summarizes academic PDF papers into concise bullet points using DeepSeek's language model API. This project uses Python, Tkinter for the GUI, and integrates AI-powered text summarization via OpenRouter.

---

## ✨ Features

- 📄 Load and parse academic PDFs (up to 3 pages)
- 🤖 Summarize the content into bullet points using an LLM
- 🪄 Clean and modern GUI with styled buttons and scrollbar
- 📦 No browser needed — fully desktop-based and local

---

## 🛠 Tech Stack

- **Python 3.11+**
- **Tkinter** for GUI
- **PyMuPDF (`fitz`)** for PDF parsing
- **Requests** for API integration
- **DeepSeek Prover API** via [OpenRouter.ai](https://openrouter.ai/)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/gghada/summarize.git
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your API key

```bash
DEEPSEEK_API_KEY = 'sk-or-...your-api-key...'
```

### 5. Run the app

```bash
python summarizer.py
```
