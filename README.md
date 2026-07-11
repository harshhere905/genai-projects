<div align="center">

# 🎬 GenAI Projects

### A growing collection of mini projects exploring LangChain & Generative AI

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-🦜🔗-1C3C3C)
![Gemini](https://img.shields.io/badge/Gemini-2.5--Flash-8E75B2?logo=googlegemini&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success)

</div>

---

## 📂 Projects

### 🤖 ChatBot
A simple CLI + Streamlit chatbot built with LangChain and Gemini that role-plays a chosen personality throughout the conversation.

- Pick a personality at the start — **Angry, Happy, Sad, or Rude**
- The personality is injected as a `SystemMessage`, so the AI stays in character for every reply
- Full conversation history is maintained using `HumanMessage` / `AIMessage`, so the bot remembers context across turns
- Streamlit version adds a chat-style UI with message bubbles, a sidebar to pick/reset personality, and a "Start Chat" flow

**Files**
| File | Description |
|---|---|
| `core.py` | CLI version |
| `ui.py` | Streamlit UI |

**Run**
```bash
streamlit run ChatBot/ui.py
```

---

### 🍿 CineParse
An information-extraction tool that reads a free-text paragraph about one or more movies and pulls out the key details — title, release year, genre, director, cast, rating, plot summary, language, box office, and awards.

- Handles paragraphs describing **multiple movies at once**, extracting each one separately
- Skips fields that aren't mentioned instead of guessing or hallucinating (`null` / empty list instead of made-up data)
- **Two extraction modes:**
  - **Text mode** — uses a `ChatPromptTemplate` to return a clean, human-readable Markdown summary
  - **Structured mode** — uses a `Pydantic` schema + `PydanticOutputParser` to return a validated JSON object, ideal for feeding into other apps/APIs
- Streamlit UI includes a "Load Sample Paragraph" button for quick testing and a toggle to view raw JSON output

**Files**
| File | Description |
|---|---|
| `text_extractor.py` | CLI — Markdown output |
| `text_extractor_ui.py` | Streamlit UI |
| `structured_extractor.py` | CLI — JSON (Pydantic) |
| `structured_extractor_ui.py` | Streamlit UI |

**Run**
```bash
streamlit run CineParse/structured_extractor_ui.py
```

---

## ⚙️ Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/harshhere905/genai-projects-.git
cd genai-projects-
```

**2. Create a virtual environment** *(optional but recommended)*
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your API key**

Create a `.env` file in the root folder:
```env
GOOGLE_API_KEY=your_api_key_here
```
> Get a free key from [Google AI Studio](https://aistudio.google.com/apikey)

**5. Run any project** using the commands above 🚀

---

## 🛠️ Built With

| Tool | Purpose |
|---|---|
| 🦜🔗 **LangChain** | LLM orchestration |
| ✨ **Google Gemini** | Language model (gemini-2.5-flash) |
| 🎈 **Streamlit** | Interactive UI |
| 📦 **Pydantic** | Structured output validation |

---

<div align="center">

### 📌 More mini projects coming soon as the learning continues!

⭐ *If you find this useful, consider giving it a star!*

</div>
