from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import shutil

from rag_engine import process_document, ask_question

app = FastAPI()

templates = Jinja2Templates(directory="templates")

current_chunks = None
current_index = None


@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):

    if username == "admin" and password == "admin":
        return {"status": "success"}

    return {"status": "fail"}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    path = f"uploads/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    global current_chunks, current_index

    current_chunks, current_index = process_document(path)

    return {"message": "Document processed successfully"}


@app.post("/ask")
def ask(question: str = Form(...)):

    global current_chunks, current_index

    if current_chunks is None:
        return {"answer": "Upload a document first"}

    answer = ask_question(current_chunks, current_index, question)

    return {"answer": answer}