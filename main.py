from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq

app = Flask(__name__)

# Load .env file
load_dotenv()

# 
api_key = os.getenv("GROQ_API_KEY")

# Debug check (optional)
if not api_key:
    raise ValueError("API Key not found. Check your .env file")

client = Groq(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  
            messages=[
                {"role": "system", "content": "Act like a helpful personal assistant"},
                {"role": "user", "content": question}
            ],
            temperature=0.7   
        )

        answer = response.choices[0].message.content

        return jsonify({"response": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Email Summarization Endpoint
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
                {"role": "system", "content": "Summarize emails in bullet points"},
                {"role": "user", "content": email_text}
            ],
            temperature=0.3
        )

        summary = response.choices[0].message.content

        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)