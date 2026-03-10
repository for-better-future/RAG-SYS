import os
import requests
import numpy as np
import faiss
from pypdf import PdfReader
import docx
from sentence_transformers import SentenceTransformer

# ------------------------------
# HuggingFace API setup
# ------------------------------

API_URL = "https://router.huggingface.co/hf-inference/models/deepset/roberta-base-squad2"

HF_TOKEN = "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"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# ------------------------------
# Load embedding model
# ------------------------------

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ------------------------------
# FILE READER
# ------------------------------

def extract_text(file_path):

    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

        return text

    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    else:
        raise ValueError("Unsupported file type")

# ------------------------------
# TEXT CHUNKING
# ------------------------------

def split_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks

# ------------------------------
# BUILD VECTOR DATABASE
# ------------------------------

def build_vector_store(chunks):

    embeddings = embedding_model.encode(chunks)

    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    return index, embeddings

# ------------------------------
# QUESTION ANSWERING
# ------------------------------

def ask_question(chunks, index, question):

    question_embedding = embedding_model.encode([question])

    distances, indices = index.search(np.array(question_embedding), k=3)

    best_chunk = " ".join([chunks[i] for i in indices[0]])

    payload = {
        "inputs": {
            "question": question,
            "context": best_chunk
        }
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        params={"wait_for_model": True}
    )

    result = response.json()

    if isinstance(result, dict):

        answer = result.get("answer", "")
        score = result.get("score", 0)

        # IMPORTANT: confidence threshold
        if score < 0.2 or answer.strip() == "":
            return "Sorry, out of scope question."

        return answer

    return "Sorry, out of scope question."

def process_document(file_path):

     text = extract_text(file_path)

     chunks = split_text(text)

     index, embeddings = build_vector_store(chunks)

     return chunks, index
# ------------------------------
# MAIN
# ------------------------------

if __name__ == "__main__":

    file_path = input("Enter file path: ")

    print("Reading document...")

    text = extract_text(file_path)

    print("Splitting text into chunks...")

    chunks = split_text(text)

    print("Creating embeddings...")

    index, embeddings = build_vector_store(chunks)

    print("RAG system ready!")

    while True:

        question = input("\nAsk a question (type exit to quit): ")

        if question.lower() == "exit":
            break

        answer = ask_question(chunks, index, question)

        print("\nAnswer:", answer)

