from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma

from dotenv import load_dotenv
import os

from utils import document_loader, chunking, vectorstore, format_docs

load_dotenv()

PERSIST_DIRECTORY = "../data/chroma_db" 

TEMPLATE = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum with maximum of 500 words. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer. 
{context}
Question: {input}
Helpful Answer:"""

class Rag():
    def __init__(self, template=TEMPLATE):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        self.embedding = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            task_type="retrieval_document"  # Optimized for search
        )
        
        self.vectordb = None
        self.QAprompt = ChatPromptTemplate.from_template(template=template)
        self.qa_chain = None

         # Share state from disk to uvicorn workers, if any. 
        if os.path.exists(PERSIST_DIRECTORY):
            try:
                temp_db = Chroma(
                    persist_directory=PERSIST_DIRECTORY, 
                    embedding_function=self.embedding
                )
                
                if temp_db._collection.count() > 0:
                    self.vectordb = temp_db
                    print(f"Loaded existing vector store with {self.vectordb._collection.count()} chunks.")
                    
                    # Qa chain is initialized
                    self._initialize_lcel_chain()

                else:
                    print("Persistent directory exists but the Chroma collection is empty.")
            except Exception as e:
                print(f"Error loading existing Chroma DB: {e}. Starting with empty state.")

    def _load_docs(self, file_path: str):
        loaded = document_loader(file_path)
        chunked = chunking(loaded)
        self.vectordb = vectorstore(chunked, self.embedding, PERSIST_DIRECTORY)
        
        self._initialize_lcel_chain()
        print(f"Document loaded and vector store created at {PERSIST_DIRECTORY}")

    def _initialize_lcel_chain(self):
        if not self.vectordb:
            print("Cannot initialize chain: VectorDB is not loaded.")
            return

        retriever = self.vectordb.as_retriever()
        rag_chain_from_docs = (
            RunnablePassthrough.assign(
                context=lambda x: format_docs(x['context'])
            )
            | self.QAprompt  
            | self.llm
            | StrOutputParser() # Parse the output to a string
        )

        self.qa_chain = RunnableParallel(
            answer=rag_chain_from_docs,
            input=RunnablePassthrough()
        )

    def _clear_db(self):
        if self.vectordb:
            try:
                self.vectordb.delete_collection()
                self.vectordb = None
                message = "Chroma DB cleared successfully."
            except Exception as e:
                message = (f"Error clearing Chroma DB: {e}")
        return message
        

    def ask(self, question: str):
        if self.qa_chain is None:
            return {
                'status_code': 400,
                'response': "No documents loaded. Please load documents first.",
                'sources': []
            }
        result = self.qa_chain.invoke({"input": question})
        print(result)

        return {
            'status_code': 200,
            'response': result.get('answer', ''),
            'sources': [
                doc.metadata.get('source', 'unknown')
                for doc in result.get('context', [])
            ],
        }

if __name__ == "__main__":
    import keyboard

    path = "../data/uploads/inte.pdf"
    engine = Rag()
    engine._clear_db()

    engine._load_docs(path)
    while(True):
        que = input("What is your question?")
        result = engine.ask(que)
        print(result)