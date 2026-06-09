# 🤖 AI Personal Assistant

An AI-powered web application built with Flask and the Groq API that provides intelligent conversations, document-based question answering, code explanation, email summarization, text rewriting, and productivity tools through a modern web interface.

---

## 🚀 Features

### 💬 AI Chat Assistant

* Multi-turn conversational chat
* Full conversation history sent to the AI model
* Context-aware responses
* Fast inference using Groq LLMs

### 📧 Email Summarizer

* Converts lengthy emails into concise bullet-point summaries
* Extracts key information instantly

### ✍️ Text Rewriter

* Rewrite text professionally
* Simplify complex content
* Improve grammar and readability

### ✅ To-Do Extractor

* Automatically extracts actionable tasks from text
* Organizes information into clear task lists

### 📄 PDF Question & Answer

* Upload PDF documents
* Ask questions based on document content
* Uses document context for accurate answers

### 💻 Code Explainer

* Explains uploaded code step-by-step
* Returns structured explanations
* Automatic syntax highlighting using Highlight.js

### 🎛️ Response Modes

Choose how the AI responds:

* Professional
* Casual
* Concise

### 🎨 User Experience Enhancements

* Copy response button
* Text-to-Speech support
* Retry / Regenerate response
* Character counter
* Recent chat history sidebar
* Typing animation while waiting for responses

---

## 🏗️ Architecture

### PDF Q&A Pipeline

1. User uploads a PDF document.
2. File is sent using FormData.
3. PyMuPDF extracts document text.
4. Text is truncated to approximately 12,000 characters to remain within context limits.
5. Extracted content is injected as document context.
6. Groq generates answers grounded in the uploaded document.

### Code Explainer Pipeline

1. User submits source code.
2. System prompt enforces strict JSON output.
3. Groq returns structured JSON.
4. Backend parses the JSON response.
5. UI renders each section separately.
6. Highlight.js automatically applies syntax highlighting using `hljs.highlightAuto()`.

---

## 🛠️ Technologies Used

### Backend

* Python
* Flask
* Groq API
* python-dotenv
* PyMuPDF

### Frontend

* HTML5
* CSS3
* JavaScript
* Highlight.js

### AI & NLP

* Large Language Models (Groq)
* Prompt Engineering
* Context Injection
* Structured JSON Outputs

---

## 📂 Project Structure

```text
AI_Personal_Assistant/
│
├── app.py
├── .env
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/AI_Personal_Assistant.git
cd AI_Personal_Assistant
```

### 2. Install Dependencies

```bash
pip install flask groq python-dotenv pymupdf
```

### 3. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

### 4. Run Application

```bash
python app.py
```

### 5. Open Browser

```text
http://127.0.0.1:5000/
```

---

## 📈 Key Concepts Demonstrated

* Generative AI Integration
* LLM API Consumption
* Prompt Engineering
* Multi-turn Conversation Handling
* PDF Processing
* Context-Aware Question Answering
* Structured JSON Parsing
* Syntax Highlighting
* Text-to-Speech Integration
* Frontend-Backend Communication
* Flask Web Development

---
## 🌐 Live Demo

[🔗 Open AI Personal Assistant](https://ai-personal-assistant-nlpg.onrender.com/)

## 🎯 Future Improvements

* User Authentication
* Persistent Chat Storage
* RAG-based PDF Search
* Multi-PDF Support
* Voice Input
* Conversation Export
* Dark/Light Theme Toggle

---

## 📄 Conclusion

AI Personal Assistant demonstrates the practical integration of Generative AI into a full-stack web application. The project combines conversational AI, document understanding, code analysis, text transformation, and productivity automation while showcasing modern AI engineering concepts such as prompt engineering, context injection, structured outputs, and LLM-powered workflows.
