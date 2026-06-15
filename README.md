<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,16,18,20&height=200&section=header&text=Multi-Agent%20Research%20Assistant&fontSize=50&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Autonomous%20AI%20Research%20Pipeline%20%7C%20LangGraph%20%7C%20Claude%20API%20%7C%20FastAPI&descAlignY=60&descAlign=50" width="100%" />

<br/>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=22&duration=3000&pause=800&color=9333EA&center=true&vCenter=true&multiline=false&repeat=true&width=700&lines=Multi-Agent+AI+Research+System;LangGraph+Orchestration+%7C+Claude+API;Web+Search+%2B+Summarise+%2B+Cite;FastAPI+Backend+%7C+React+Frontend" alt="Typing SVG" />

<br/><br/>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18.3-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2-FF6B35?style=for-the-badge&logo=langchain&logoColor=white)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude-D97706?style=for-the-badge&logo=anthropic&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)

</div>

---

## 🧠 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    LangGraph StateGraph                         │
│                                                                 │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│   │   Agent 1   │───▶│   Agent 2   │───▶│   Agent 3   │         │
│   │             │    │             │    │             │         │
│   │  🔍 Search  │    │  🧠 Summar  │    │  📚 Cite    │         │
│   │  DuckDuckGo │    │  Claude API │    │  APA Format │         │
│   └─────────────┘    └─────────────┘    └─────────────┘         │
│          │                  │                  │                │
│          ▼                  ▼                  ▼                │
│   search_results       summary{}          citations[]           │
│                                                                 │
│                    ┌─────────────┐                              │
│                    │  Compile    │                              │
│                    │  Report     │                              │
│                    └─────────────┘                              │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────┐          ┌──────────────────────┐
│  FastAPI        │◀────────▶│  React + Vite        │
│  POST /research │          │  Dark-theme UI       │
│  :8000          │          │  :5173               │
└─────────────────┘          └──────────────────────┘
```

---

## ✨ Features

- 🔍 **Real Web Search** — DuckDuckGo Lite HTML scraping, no API key required, top 5 results per query
- 🧠 **Claude-Powered Summarisation** — Structured output with overview, key findings, and implications
- 📚 **APA Citation Formatter** — Automatically formats all sources as APA 7th edition citations
- ⚡ **LangGraph Orchestration** — Type-safe `StateGraph` wires agents together in a directed pipeline
- 🚀 **FastAPI Backend** — Async REST API with CORS support, Pydantic validation, and auto-generated docs
- 🎨 **Dark React UI** — Clean dark-themed frontend with loading states, agent progress, and card-based report display
- 🔄 **Full Pipeline** — Single POST request triggers all three agents and returns a structured research report

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- An [Anthropic API key](https://console.anthropic.com/)

### Backend Setup

```bash
# 1. Navigate to the backend directory
cd backend

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your .env file
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env

# 5. Start the FastAPI server
python main.py
# or: uvicorn main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`.  
Interactive API docs: `http://localhost:8000/docs`

### Frontend Setup

```bash
# 1. Navigate to the frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start the Vite dev server
npm run dev
```

The frontend will be available at `http://localhost:5173`.

---

## 📡 API Reference

### `POST /research`

Run the full multi-agent research pipeline.

**Request:**
```json
{
  "query": "What are the latest developments in quantum computing?"
}
```

**Response:**
```json
{
  "query": "What are the latest developments in quantum computing?",
  "report": "# Research Report: ...",
  "sections": {
    "overview": "Quantum computing has seen...",
    "key_findings": [
      "IBM unveiled a 1000-qubit processor...",
      "Google achieved quantum advantage in..."
    ],
    "implications": "These advances suggest that..."
  },
  "citations": [
    {
      "id": 1,
      "apa": "Title. (n.d.). Site. Retrieved June 15, 2026, from https://...",
      "url": "https://example.com/article",
      "title": "Article Title"
    }
  ]
}
```

---

## 🗂️ Project Structure

```
multi-agent-research-assistant/
├── backend/
│   ├── main.py                  # FastAPI app, CORS, /research endpoint
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── search_agent.py      # DuckDuckGo Lite scraper (requests + bs4)
│   │   ├── summarise_agent.py   # Claude API structured summarisation
│   │   ├── citation_agent.py    # APA 7th edition citation formatter
│   │   └── orchestrator.py      # LangGraph StateGraph pipeline
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx             # React entry point
│       ├── App.jsx              # Main app component
│       └── App.css              # Dark theme styles
└── README.md
```

---

## 🛠️ Tech Stack

<div align="center">

<img src="https://skillicons.dev/icons?i=python,fastapi,react,vite,js&theme=dark" />

</div>

| Layer | Technology |
|-------|-----------|
| Orchestration | LangGraph 0.2 StateGraph |
| Summarisation | Anthropic Claude API (claude-opus-4-5) |
| Web Search | DuckDuckGo Lite (requests + BeautifulSoup4) |
| Backend | FastAPI 0.115 + Uvicorn |
| Frontend | React 18 + Vite 5 |
| HTTP Client | Axios |
| Validation | Pydantic v2 |

---

## 📄 License

MIT © [isamkhan1809](https://github.com/isamkhan1809)

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,16,18,20&height=120&section=footer" width="100%" />

</div>
