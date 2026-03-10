Document Question Answering System (RAG Based)

Project Description

This project is a Retrieval Augmented Generation (RAG) based document question answering system.

Users can:

1. Upload a document (PDF, DOCX, TXT)
2. Ask questions about the document
3. The system retrieves relevant content and generates answers

If a question is not related to the document, the system returns:

Sorry, out of scope question.

The system uses FastAPI for backend, Sentence Transformers for embeddings, and HuggingFace QA model for answering questions.

---

System Requirements

Make sure the following are installed:

- Python 3.9 or higher
- pip (Python package manager)
- Internet connection (for downloading ML models)

---

Step 1 — Clone or Download the Project

Download the project folder and open it in VS Code or any terminal.

Navigate to the project directory.

Example:

cd project-folder-name

---

Step 2 — Install Required Libraries

Run the following commands in the terminal.

pip install fastapi
pip install uvicorn
pip install sentence-transformers
pip install transformers
pip install torch
pip install pypdf
pip install python-docx
pip install python-multipart
pip install jinja2
pip install numpy

These libraries are required for:

Library| Purpose
fastapi| Backend API framework
uvicorn| FastAPI server
sentence-transformers| Text embeddings
transformers| HuggingFace QA model
torch| Deep learning framework
pypdf| PDF text extraction
python-docx| DOCX file reading
python-multipart| File upload support
jinja2| HTML template rendering
numpy| Vector operations

---

Step 3 — Run the Backend Server

After installing all libraries, run the server using:

uvicorn main:app --reload

If successful, you will see:

Uvicorn running on http://127.0.0.1:8000

---

Step 4 — Open the Web Application

Open your browser and go to:

http://127.0.0.1:8000

This will open the login page.

---

Step 5 — Using the System

1. Login to the dashboard
2. Upload a document
3. Ask questions related to the document
4. The system will return answers from the uploaded document

---

Project Structure

project-folder
│
├── main.py
├── rag_engine.py
├── README.md
│
├── templates
│   ├── login.html
│   └── dashboard.html
│
├── uploads

---

Technologies Used

- Python
- FastAPI
- Sentence Transformers
- HuggingFace Transformers
- PyPDF
- Python-Docx
- HTML / JavaScript

---

END...