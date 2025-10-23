import os
from typing import List
from langchain_core.documents import Document
from langchain.document_loaders import TextLoader,PyPDFLoader,Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma


FILE_LOADER_MAP = {
    ".txt": TextLoader,
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
}

def document_loader(file_path: str) -> List[Document]:
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()

    if extension in FILE_LOADER_MAP:
        LoaderClass = FILE_LOADER_MAP[extension]
        loader = LoaderClass(file_path)
        print("-----Loading Document-----")
        return loader.load()
    else:
        supported = ", ".join(FILE_LOADER_MAP.keys())
        raise ValueError(
            f"Unsupported file type '{extension}'. Supported types are: {supported}"
        )

def chunking(documents: List[Document], chunk_size: int = 500, chunk_overlap: int = 50) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunked_documents = text_splitter.split_documents(documents)
    return chunked_documents

def vectorstore(documents: List[Document], embedding_model, persist_directory: str):
    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory)
        
    vectordb = Chroma.from_documents(
        documents,
        embedding_model,
        persist_directory=persist_directory
    )
    return vectordb

def add_memory():
    pass

