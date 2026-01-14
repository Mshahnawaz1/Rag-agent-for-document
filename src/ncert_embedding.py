from utils import document_loader, chunking
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv

load_dotenv()

PERSIST_DIRECTORY = "../data/ncert_chroma_db"

class NCERTEmbedding:
    def __init__(self):
        self.embedding = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            task_type="retrieval_document"
        )
        self.vectordb = None

    def create_embedding(self, file_path: str):
        loaded = document_loader(file_path)
        chunked = chunking(loaded)

        self.vectordb = Chroma.from_documents(
            documents=chunked,
            embedding=self.embedding,
            persist_directory=PERSIST_DIRECTORY
        )
        print(f"NCERT Vector store created at {PERSIST_DIRECTORY}")

if __name__ == "__main__":
    ncert_embedder = NCERTEmbedding()
    file_path = '../data/test.pdf'  # Replace with actual NCERT document path
    ncert_embedder.create_embedding(file_path)