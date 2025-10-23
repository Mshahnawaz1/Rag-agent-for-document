from typing import Union
import os
from fastapi import UploadFile, File
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from dotenv import load_dotenv

from rag_engine import Rag


app = FastAPI(title="RAG Engine API", description="API for RAG", version="1.0.0")
_rag = Rag()
load_dotenv()

@app.get("/")
def read_root():
    return {"Hello": "World"}

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
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    _rag._load_docs(file_path)


    return JSONResponse(content={"message": f"File '{filename}' uploaded successfully! \n Content:"})

@app.post("/ask")
async def ask_question(question: str):
    if not os.getenv("GOOGLE_API_KEY"):
        raise HTTPException(status_code=400, detail="Missing GOOGLE_API_KEY in environment.")

    response = _rag.ask(question)
    return JSONResponse(content=response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# uvicorn main:app --reloadB
# http://127.0.0.1:8000/docs#/