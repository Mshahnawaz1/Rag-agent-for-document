from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from dotenv import load_dotenv

from ingestion import document_loader, chunking, vectorstore

load_dotenv()

PERSIST_DIRECTORY = "data/chroma_db"

TEMPLATE = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum with maximum of 500 words. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer. 
{context}
Question: {question}
Helpful Answer:"""

class RagEngine():
    def __init__(self, template=TEMPLATE):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        self.embedding = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",  
            task_type="retrieval_document" # Optimized for search
        )
        
        self.template = template
        self.vectordb = None
        self.QAprompt = ChatPromptTemplate.from_template(template=template)
        # self.chain = self.QAprompt | self.llm | StrOutputParser()

    def _load_docs(self, file_path: str):
        loaded = document_loader(file_path)
        chunked = chunking(loaded)
        self.vectordb = vectorstore(chunked, self.embedding, PERSIST_DIRECTORY)
        print(f"Document loaded and vector store created at {PERSIST_DIRECTORY}")

    def retrieve(self, query: str, k: int = 3):
        if not self.vectordb:
            self.vectordb = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=self.embedding)
        docs = self.vectordb.similarity_search(query, k=k)
        return "\n\n".join([doc.page_content for doc in docs])
        
    # def invoke(self, input_dict={}):
    #     try:
    #         response = self.chain.invoke(input_dict)
    #         return response
    #     except Exception as e:
    #         return f"API Test Failed. Ensure the GOOGLE_API_KEY is correctly set in your .env file. Error: {e}" 
        
    def ask(self, question: str):
        # context = self.retrieve(question)
        if self.vectordb is None:
            return "No documents loaded. Please load documents first."
        
        qa_chain = RetrievalQA.from_chain_type(self.llm,
                                       retriever=self.vectordb.as_retriever(),
                                       return_source_documents=False,
                                       chain_type_kwargs={"prompt": self.QAprompt})
        return qa_chain({"query": question})

if __name__ == "__main__":
    path = "../data/text_files/kf100.txt"
    engine = RagEngine()
    engine._load_docs(path)
    result = engine.ask("What is name of characters?")
    print(result)