from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from dotenv import load_dotenv

from utils import document_loader, chunking
import os

load_dotenv()

PERSIST_DIRECTORY = "../data/chroma_db"

TEMPLATE = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know. 
Keep the answer concise (max 3 sentences, 500 words). 
Always end the answer with "thanks for asking!".

Context:
{context}

Question: {question}

Helpful Answer:"""

class Rag:
    def __init__(self, template=TEMPLATE):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        self.embedding = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            task_type="retrieval_document"
        )

        self.vectordb = None
        self.QAprompt = ChatPromptTemplate.from_template(template)
        self.qa_chain = None

        if os.path.exists(PERSIST_DIRECTORY):
            try:
                temp_db = Chroma(
                    persist_directory=PERSIST_DIRECTORY,
                    embedding_function=self.embedding
                )
                if temp_db._collection.count() > 0:
                    self.vectordb = temp_db
                    print(f"Loaded existing vector store with {self.vectordb._collection.count()} chunks.")
                    self._initialize_lcel_chain()
                else:
                    print("Persistent directory exists but collection is empty.")
            except Exception as e:
                print(f"Error loading existing Chroma DB: {e}. Starting fresh.")

    def _load_docs(self, file_path: str):
        loaded = document_loader(file_path)
        chunked = chunking(loaded)

        self.vectordb = Chroma.from_documents(
            documents=chunked,
            embedding=self.embedding,
            persist_directory=PERSIST_DIRECTORY
        )
        self._initialize_lcel_chain()
        print(f"Vector store created at {PERSIST_DIRECTORY}")

    def _retriever_info(self, question: str):
        if not self.vectordb:
            return "No VectorDB loaded."
        results = self.vectordb.similarity_search(question, k=3)
        return "\n\n".join(doc.page_content for doc in results)

    def _initialize_lcel_chain(self):
        if not self.vectordb:
            print("Cannot initialize chain: VectorDB not loaded.")
            return

        self.qa_chain = (
            RunnablePassthrough.assign(
                context=lambda x: self._retriever_info(x["question"])
            )
            | self.QAprompt
            | self.llm
            | StrOutputParser()
        )

    def _clear_db(self):
        if self.vectordb:
            try:
                self.vectordb.delete_collection()
                self.vectordb = None
                return "Chroma DB cleared successfully."
            except Exception as e:
                return f"Error clearing DB: {e}"

    def ask(self, question: str):
        if not self.qa_chain:
            return {
                "status_code": 400,
                "response": "No documents loaded. Please load documents first."
            }

        answer = self.qa_chain.invoke({"question": question})
        return {"status_code": 200, "response": answer}

if __name__ == "__main__":
    path = "../data/uploads/inte.pdf"
    engine = Rag()
    engine._clear_db()

    engine._load_docs(path)
    while(True):
        que = input("What is your question?")
        result = engine.ask(que)
        print(result)