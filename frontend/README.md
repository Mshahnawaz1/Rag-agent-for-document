# React Frontend for RAG Agent

A simple React frontend built with Vite for the RAG Document Assistant.

## Prerequisites

- Node.js (v18 or higher) and npm installed
- FastAPI backend running on `http://127.0.0.1:8000`

## Setup

1. Install dependencies:
```bash
npm install
```

## Development

Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Build for Production

Build the production bundle:
```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Chat.jsx          # Chat interface component
│   │   ├── Sidebar.jsx       # Sidebar with upload and controls
│   │   └── Message.jsx       # Individual message component
│   ├── App.jsx               # Main app component
│   ├── App.css               # App styles
│   ├── index.css             # Global styles
│   └── main.jsx              # Entry point
├── index.html                # HTML template
├── package.json              # Dependencies and scripts
├── vite.config.js           # Vite configuration
└── README.md                # This file
```

## Features

- Upload documents (PDF, TXT, DOCX)
- Ask questions about uploaded documents
- Query NCERT knowledge base
- Clear vector database
- Real-time chat interface

## Configuration

The API base URL can be configured via environment variable:
- Create a `.env` file in the frontend directory
- Add: `VITE_API_URL=http://127.0.0.1:8000`
- Or modify the BASE_URL in `src/App.jsx`
