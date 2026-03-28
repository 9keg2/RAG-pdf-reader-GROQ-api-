# To run this project you have to get a API key.

Get it here - https://console.groq.com/keys

# 🌌 Astral AI — Intelligent Document Chat System

> Ask anything. Understand everything. Powered by AI.

---

## 🚀 Overview

**Astral AI** is a modern Retrieval-Augmented Generation (RAG) application that allows users to interact with documents like a conversation.

Upload any file — PDF, TXT, or Markdown — and Astral AI will **understand, retrieve, and answer** your questions with high accuracy using advanced language models.

---

## ✨ Features

* 📂 Multi-format support (PDF, TXT, MD)
* 💬 Chat with your documents in real-time
* ⚡ Ultra-fast responses powered by Groq LLMs
* 🧠 Context-aware answers using RAG pipeline
* 🔍 Semantic search with vector embeddings
* 🎨 Modern glassmorphism UI (Streamlit-based)
* 🔐 Secure API handling using `.env`

---

## 🧠 How It Works (Architecture)

Astral AI uses a **Retrieval-Augmented Generation (RAG)** pipeline:

```
User Query
    ↓
Convert to Embedding
    ↓
Vector Search (FAISS)
    ↓
Relevant Chunks Retrieved
    ↓
Groq LLM (LLaMA 3)
    ↓
Final Answer
```

---

## ⚙️ Tech Stack

| Layer           | Technology               |
| --------------- | ------------------------ |
| UI              | Streamlit                |
| LLM             | Groq API (LLaMA 3.3 70B) |
| Embeddings      | HuggingFace (MiniLM)     |
| Vector DB       | FAISS                    |
| Backend         | LangChain                |
| File Processing | PyPDFLoader, TextLoader  |

---

## 🔌 APIs Used

### 🧠 Groq API

* Model: `llama-3.3-70b-versatile`
* Purpose: Fast and accurate response generation

### 📦 HuggingFace Embeddings

* Model: `all-MiniLM-L6-v2`
* Purpose: Convert text into vector embeddings for semantic search

---

## 📁 Supported File Types

| File Type      | Supported |
| -------------- | --------- |
| PDF            | ✅         |
| TXT            | ✅         |
| Markdown (.md) | ✅         |

---

## 🛠️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/RAG-pdf-reader-GROQ-api-.git
cd RAG-pdf-reader-GROQ-api-
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Setup Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

---

### 4. Run the app

```bash
streamlit run app.py
```

---

## 🎯 Usage

1. Upload a document (PDF/TXT/MD)
2. Click **Process**
3. Ask questions in chat
4. Get accurate answers instantly

---

## 🧪 Example Queries

* "What is this document about?"
* "Summarize chapter 2"
* "Explain key concepts"
* "How many pages are there?"

---

## 🔐 Security

* API keys are stored securely using `.env`
* `.env` is excluded via `.gitignore`
* No sensitive data is exposed

---

## 📈 Future Improvements

* 📊 Source highlighting (exact text reference)
* ⚡ Streaming responses (real-time typing)
* 🧠 Better embeddings (BGE / Instructor models)
* 📂 Multi-file simultaneous querying
* 🌐 Deployment (Cloud / Docker)

---

## 💡 Why Astral AI?

Unlike traditional document readers, Astral AI:

* Understands context, not just keywords
* Provides conversational answers
* Works across multiple file formats
* Uses state-of-the-art AI models

---

## 🧑‍💻 Author

Built with passion for AI and real-world problem solving.

---

## 📜 License

This project is licensed under the MIT License.

---

## ⭐ Support

If you like this project:

* ⭐ Star the repository
* 🍴 Fork it
* 📢 Share it

---

> 🌌 Astral AI — Turning documents into conversations.
