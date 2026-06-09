from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq
import fitz  # PyMuPDF
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("API Key not found. Check your .env file")

client = Groq(api_key=api_key)

TONE_PROMPTS = {
    "professional": "You are a professional assistant. Respond formally and precisely.",
    "casual": "You are a friendly assistant. Respond in a warm, conversational tone.",
    "concise": "You are a concise assistant. Keep every response to 2-3 sentences max.",
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    tone = data.get("tone", "professional")
    history = data.get("history", [])  # list of {role, content} dicts

    if not question:
        return jsonify({"error": "No question provided"}), 400

    system_prompt = TONE_PROMPTS.get(tone, TONE_PROMPTS["professional"])

    messages = [{"role": "system", "content": system_prompt}]
    messages += history  # inject prior turns
    messages.append({"role": "user", "content": question})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7
        )
        answer = response.choices[0].message.content
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    email_text = data.get("email")
    if not email_text:
        return jsonify({"error": "No email text provided"}), 400
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Summarize the email in bullet points. Start each point with •"},
                {"role": "user", "content": email_text}
            ],
            temperature=0.3
        )
        return jsonify({"summary": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/rewrite", methods=["POST"])
def rewrite():
    data = request.get_json()
    text = data.get("text")
    style = data.get("style", "professional")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": f"Rewrite the given text in a {style} tone. Return only the rewritten text."},
                {"role": "user", "content": text}
            ],
            temperature=0.5
        )
        return jsonify({"result": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/extract-todos", methods=["POST"])
def extract_todos():
    data = request.get_json()
    text = data.get("text")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Extract all action items and to-dos from the text. Format as a numbered list. If none found, say 'No action items found.'"},
                {"role": "user", "content": text}
            ],
            temperature=0.2
        )
        return jsonify({"result": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PDF Upload + Q&A
@app.route("/pdf-qa", methods=["POST"])
def pdf_qa():
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF uploaded"}), 400

    file = request.files['pdf']
    question = request.form.get('question', 'Summarize this document.')

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file. Please upload a PDF."}), 400

    try:
        # Read PDF bytes and extract text with PyMuPDF
        pdf_bytes = file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        text_pages = []
        for page in doc:
            text_pages.append(page.get_text())
        
        full_text = "\n\n".join(text_pages)
        page_count = len(doc)
        doc.close()

        # Truncate if too long (Groq context limit safety)
        if len(full_text) > 12000:
            full_text = full_text[:12000] + "\n\n[Document truncated for length...]"

        if not full_text.strip():
            return jsonify({"error": "Could not extract text. The PDF may be scanned/image-based."}), 400

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a document assistant. Answer questions based strictly on "
                        "the provided document content. If the answer isn't in the document, say so."
                    )
                },
                {
                    "role": "user",
                    "content": f"Document content:\n\n{full_text}\n\n---\nQuestion: {question}"
                }
            ],
            temperature=0.3
        )

        answer = response.choices[0].message.content
        return jsonify({"answer": answer, "pages": page_count})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Code Explainer
@app.route("/explain-code", methods=["POST"])
def explain_code():
    data = request.get_json()
    code = data.get("code")
    language = data.get("language", "auto-detect")

    if not code:
        return jsonify({"error": "No code provided"}), 400

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior software engineer and code reviewer. "
                        "When given code, respond ONLY with a JSON object (no markdown, no backticks) with exactly these keys:\n"
                        "- language: detected or provided language name\n"
                        "- explanation: plain-English explanation of what the code does (3-6 sentences)\n"
                        "- bugs: array of strings, each describing a bug or issue found (empty array if none)\n"
                        "- suggestion: one concrete improvement suggestion as a string"
                    )
                },
                {
                    "role": "user",
                    "content": f"Language hint: {language}\n\nCode:\n{code}"
                }
            ],
            temperature=0.2
        )

        raw = response.choices[0].message.content.strip()
        # Strip markdown fences if model adds them
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        
        import json
        result = json.loads(raw)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
