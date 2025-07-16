# 🌐 LangGraph Agentic AI Data Modeler

This project is a full-stack, agentic AI-powered tool that generates Entity-Relationship Diagrams (ERDs) from business requirements using LLMs via LangGraph and Groq. It supports enhanced automation, data dictionary processing, and optional fantasy entity generation to assist data architects and developers.

**Landing page**
<img width="1952" height="1189" alt="image" src="https://github.com/user-attachments/assets/f4664406-45e6-4ad1-b238-a43f13836982" />

**After Execution**
<img width="2529" height="3523" alt="image" src="https://github.com/user-attachments/assets/a14b07ad-5057-4b92-8d0a-46623aeed39e" />
---

## 🚀 Features

- ✅ Step-by-step LangGraph-based ERD generation flow
- 📋 Upload Excel data dictionary to guide ERD output
- ✨ Optional fantasy modules (e.g., audit tables) via LLM
- 📄 Summarized business domain analysis
- 🧠 Backed by `llama3-70b` model from Groq API
- 🌈 Frontend built with V0 (React / Next.js)
- 🧰 FastAPI-powered backend

---

## 🏗️ Project Structure

```bash
LangGraph-Agentic-AI-Data-Modeler/
├── backend/                 # FastAPI + LangGraph backend
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   └── main.py
│   ├── langgraph_flow.py
│   └── requirements.txt
└── frontend/                # V0-generated React frontend
    ├── app/
    ├── components/
    └── erd-generator.tsx

📦 Backend Setup (FastAPI + LangGraph)
1. Clone the repo and create virtual environment:
git clone https://github.com/Jeet1922/LangGraph-Agentic-AI-Data-Modeler.git
cd LangGraph-Agentic-AI-Data-Modeler/backend
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux

2. Install dependencies:
pip install -r requirements.txt

Make sure you have your GROQ_API_KEY set in a .env file.
GROQ_API_KEY=your_groq_api_key_here

3. Run FastAPI server:
uvicorn app.main:app --reload

🧪 API Endpoint
POST /generate-erd

Field	Type	Description
model_type	string	"ERP-based" or "Generic"
business_requirement	string	Free-text business description
erp_system_name	string	Optional: ERP name (e.g., SAP)
fantasy_mode	boolean	Include optional fantasy modules
file	UploadFile	Excel file with Table Name, Column Name

✅ Sample Response:
{
  "success": true,
  "erd_json": {
    "entities": [...],
    "relationships": [...]
  },
  "summary": "...",
  "fantasy_entities": [...]
}

🎨 Frontend Setup (Next.js + V0)
cd ../frontend
npm install

2. Run the frontend:
npm run dev

3. Connect to Backend
In erd-generator.tsx, update the fetch URL:
const apiResponse = await fetch("http://localhost:8000/generate-erd", {
  method: "POST",
  body: formDataToSend
})

📊 Output
📘 Business Domain Summary: High-level explanation of entity interactions

🔧 ERD JSON: Entities, attributes, relationships

🧙 Fantasy Tables: Optional extra tables based on LLM creativity

💡 Future Improvements
Diagram auto-render via Mermaid or D3.js

Export DDL/SQL from JSON

User authentication & project history

LangGraph branching logic for corrections

🤝 Contributions & Support
Contributions are warmly welcome!
If you find this project helpful, inspiring, or are building on top of it—feel free to contribute, improve, or even share feedback.

💛 Optional: If you'd like to show appreciation, consider donating to a cause.
I’d love to raise funds for NGOs doing meaningful work.

Your support could help this project inspire both people and purpose.

Together, we can build impactful tools and do good.

✨ Credits
Built using LangGraph, Groq, FastAPI, and V0

LLMs powered by llama3-70b for fast reasoning and generation
