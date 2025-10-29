# AI-Powered Document Assistant (RAG System)

<div align="center">
<div align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"/></a>
  <a href="https://chromadb.com/"><img src="https://img.shields.io/badge/ChromaDB-007FFF?style=flat&logo=chroma&logoColor=white" alt="ChromaDB"/></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white" alt="FastAPI"/></a>
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker"/></a>
</div>
</div>

---

## Summary

This project implements an **AI-Powered Document Assistant** using a **Retrieval-Augmented Generation (RAG)** architecture. It allows users to upload various document types (PDF, TXT, DOCX), processes them to create embeddings, stores them in a vector database, and uses the Google Gemini model to answer user queries based solely on the uploaded content.

This system provides accurate, context-aware answers without hallucination by grounding the LLM's response in your specific documents.

---

## Tech Stack & Key Components

* **LLM & Embeddings:** **Google Gemini API** (Specifically, `gemini-pro` for generation and `models/text-embedding-004` for embeddings).
* **Vector Database:** **Chroma DB** for persistent storage of document embeddings.
* **Backend:** **FastAPI** for building a high-performance, asynchronous request-response API.
* **Frontend:** **JavaScript** and **HTML** for a user interface (with potential for future framework integration).
* **Deployment:** **Docker** and **Docker Compose** for easy containerization and setup.

---

## Working Principle

1.  **Ingestion:** The user uploads a supported document (**`.pdf`**, **`.txt`**, **`.docx`**).
2.  **Embedding Creation:** The document content is split into chunks, and the Google **`models/text-embedding-004`** model generates a high-quality vector **embedding** for each chunk.
3.  **Storage:** These embeddings are stored in a **Chroma DB** collection, establishing a persistent knowledge base.
4.  **Retrieval-Augmentation (RAG):**
    * When a user asks a question, an embedding is created for the query.
    * This query embedding is used to search the Chroma DB for the **most relevant document chunks** (currently using similarity search).
    * These chunks are then packaged as **context** and passed along with the user's original question to the **Gemini LLM**.
5.  **Generation:** The **Gemini LLM** (`gemini-pro`) generates a precise answer grounded *only* in the provided document context.

---

## Setup & Installation

You have two options for setting up the project: directly using a virtual environment or via Docker.

### Option 1: Direct Setup (Recommended for Development)

1.  **Clone the Repository:**
    ```bash
    git clone <(https://github.com/Mshahnawaz1/Rag-agent-for-documen)>
    cd <Rag-agent-for-document>
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # .\venv\Scripts\activate  # Windows
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt # Assuming you have a requirements.txt file
    ```

4.  **Set Environment Variable:**
    Create a file named `.env` in the root directory and add your API key:
    ```
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```

5.  **Run the FastAPI Server:**
    ```bash
    cd src
    uvicorn app:main --reload
    ```
    The application will be accessible at `http://127.0.0.1:8000`.

### Option 2: Using Docker Compose (Recommended for Production/Easy Deployment)

1.  **Set Environment Variable:** Ensure you have your `GEMINI_API_KEY` set in a `.env` file or passed to the environment.

2.  **Build and Run Containers:**
    ```bash
    docker-compose up --build
    ```
    This command will build the necessary Docker images and start the services, including the FastAPI backend and Chroma DB.

---

## 🤝 Contribution

This is an open-source project, and contributions are highly welcome!

Feel free to **collaborate** with me and **create a pull request** for bug fixes, new features, or improvements to the documentation. Please check the existing issues before starting work.

---
