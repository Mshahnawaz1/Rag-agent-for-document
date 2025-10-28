from fastapi import UploadFile, File, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os

from dotenv import load_dotenv
from rag_engine import Rag

app = FastAPI(title="RAG Engine API", description="API for RAG", version="1.0.0")
_rag = Rag()
load_dotenv()

UPLOAD = "../data/uploads"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,             # Allow cookies and Authorization header
    allow_methods=["*"],      
    allow_headers=["*"],                # Allow all headers (including custom ones)
)

@app.get("/")
def read_root():
    file_path = os.path.join(os.path.dirname(__file__), "../frontend/index.html")
    return FileResponse(file_path)


@app.get("/clearDB")
def clear_db():
    res = _rag._clear_db()
    return {"message": res}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not os.getenv("GOOGLE_API_KEY"):
        raise HTTPException(status_code=400, detail="Missing GOOGLE_API_KEY in environment.")

    filename = file.filename

    filename = file.filename or "uploaded_file"
    if not (filename.lower().endswith(".pdf") or filename.lower().endswith(".txt") or filename.lower().endswith(".docx")):
        raise HTTPException(status_code=400, detail="Only .pdf, .txt, .docx are supported.")

    # Save uploaded file
    os.makedirs(UPLOAD, exist_ok=True)
    file_path = os.path.join(UPLOAD, filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    _rag._load_docs(file_path)


    return JSONResponse({
        'status_code': 200,
        'message': f"File '{filename}' uploaded and processed successfully!"
    })

class AskRequest(BaseModel):
    query: str


@app.post("/ask")
async def ask_question(request: AskRequest):
    query = (request.query or "").strip()

    if not query:
        raise HTTPException(status_code=400, detail="'query' must be a non-empty string")

    if not os.getenv("GOOGLE_API_KEY"):
        raise HTTPException(status_code=400, detail="Missing GOOGLE_API_KEY in environment.")

    response = _rag.ask(query)

    # Expect response to be a dict with keys 'status_code', 'response', 'sources'
    return JSONResponse({
        'status_code': response.get('status_code', 200),
        'response': response.get('response', ''),
        'sources': response.get('sources', [])
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# uvicorn main:app --reload
# http://127.0.0.1:8000/docs#/