Checkout this video for the application demo: https://github.com/Jeet1922/LangGraph-Agentic-AI-Data-Modeler/blob/main/app.mp4
Follow these steps to run the application: https://github.com/Jeet1922/LangGraph-Agentic-AI-Data-Modeler/blob/main/run%20steps.txt

# LangGraph Agentic AI Data Modeler

This project is an AI-powered ERD and data model generation solution that turns business requirements into structured database designs. It combines LangGraph orchestration, Groq LLM inference, RAG-style context enrichment, and a modern frontend for generating and exploring entity relationship diagrams.

## Overview

The application helps users:

- Describe a business requirement in plain English
- Optionally upload an Excel data dictionary with table and column metadata
- Generate an ERD in JSON format with entities, attributes, and relationships
- Receive a business summary and architecture recommendations
- Generate SQL DDL for a target database
- Generate synthetic test data based on the ERD
- Enable fantasy-mode expansion for additional creative entities when needed

This is especially useful for ERP-oriented scenarios such as SAP process modeling, fraud detection, procurement, finance, and operational data design.

## Solution Architecture

The solution is built in two main layers:

- Backend: FastAPI service with LangGraph workflow orchestration
- Frontend: Next.js UI for form input, schema review, and data export

### Workflow

The backend uses a LangGraph pipeline with the following steps:

1. Validate the request inputs
2. Enhance the provided data dictionary context
3. Summarize the business domain and model intent
4. Generate ERD JSON based on the requirement
5. Optionally generate fantasy entities
6. Merge the fantasy entities into the output model

This creates a semi-agentic flow where the model interprets enterprise context and produces a structured database design.

## Key Features

- Natural-language ERD generation from business requirements
- Optional ERP and SAP-specific prompting
- Excel upload support for metadata and table/column extraction
- Chroma-based context enhancement for more relevant schema generation
- Business summary generation alongside the ERD
- DDL generation for PostgreSQL/MySQL/SQLite-style database outputs
- Synthetic data generation for testing and prototyping
- Frontend visualization-ready ERD JSON output
- Fantasy mode for additional optional entities

## Tech Stack

- Python
- FastAPI
- Uvicorn
- LangGraph
- LangChain
- Groq API
- Chroma
- sentence-transformers
- pandas and openpyxl
- Next.js
- React
- Tailwind CSS

## Project Structure

- backend/app/main.py - FastAPI app entry point
- backend/app/langgraph_flow.py - LangGraph workflow and ERD generation logic
- backend/app/api/langgraph_routes.py - API endpoints for ERD, DDL, and synthetic data generation
- backend/app/api/routes.py - legacy step-based endpoints
- backend/app/services/llm_client.py - Groq integration and retry/fallback logic
- backend/app/services/logic.py - prompt orchestration helpers
- backend/app/models/schema.py - request models
- frontEnd - Next.js frontend for user interaction
- data/ - sample data and metadata content
- backend/chroma_db/ - local vector DB storage used by Chroma

## Prerequisites

Before running the app, make sure you have:

- Python 3.10 or newer
- Node.js 18+ and npm
- A Groq API key
- Access to the internet for LLM calls

## Environment Configuration

Create a .env file inside the backend folder with the following:

```bash
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

Notes:

- Use a supported Groq model name. Some older model names are deprecated and may fail.
- The project includes fallback logic for common Groq model issues, but a valid API key is still required.

## Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Linux/macOS
# or: .\venv\Scripts\activate   # Windows PowerShell
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend API will usually run on:

- http://127.0.0.1:8000

## Frontend Setup

```bash
cd frontEnd
npm install
npm run dev
```

Then open the app in the browser at:

- http://localhost:3000

## Supported Input Types

The app accepts:

- Plain English business requirements
- ERP names such as SAP, Oracle, Dynamics, or custom systems
- Optional Excel files with columns named Table Name and Column Name
- Optional fantasy mode toggle for generating additional conceptual entities

## Example Business Prompts

```text
Create a data model on manual journal entries which are risky based on debit amount/credit amount of 999999.
```

```text
Create a data model for SAP to find fraudulent manual journal entries. Use technical table names as maintained in SAP ERP while generating the data model in the ERD.
```

These prompts are designed for SAP and ERP-domain modeling, including operational and control-focused data models.

## API Endpoints

### Generate ERD

Endpoint: POST /generate-erd

Request fields:

- model_type: required
- business_requirement: required
- erp_system_name: optional
- fantasy_mode: optional boolean toggle
- file: optional Excel file

Response contains:

- success
- erd_json
- summary
- fantasy_entities

### Generate DDL

Endpoint: POST /generate-ddl

Request body example:

```json
{
  "erd_json": {
    "entities": [
      {"name": "Vendor", "attributes": [{"name": "vendor_id", "type": "string", "primary_key": true}]}
    ],
    "relationships": []
  },
  "db_type": "postgresql"
}
```

### Generate Synthetic Data

Endpoint: POST /generate-synthetic-data

Request fields:

- erd_json: required
- num_rows: number of rows to generate per table
- format: json, csv, or sql

## Example ERD Output Structure

```json
{
  "entities": [
    {
      "name": "ManualJournalEntry",
      "attributes": [
        {"name": "entry_id", "type": "string", "primary_key": true},
        {"name": "debit_amount", "type": "decimal"},
        {"name": "credit_amount", "type": "decimal"},
        {"name": "document_date", "type": "date"}
      ]
    }
  ],
  "relationships": [
    {
      "type": "one-to-many",
      "from": "AccountingPeriod",
      "to": "ManualJournalEntry",
      "fromColumn": "period_id",
      "toColumn": "period_id"
    }
  ]
}
```

## Notes and Common Troubleshooting

- If Groq returns a model decommissioned error, update GROQ_MODEL to a supported value such as llama-3.1-8b-instant.
- Ensure the backend environment has the required Python dependencies installed.
- Use an Excel file with the expected column names Table Name and Column Name.
- If the frontend cannot connect to the backend, confirm the FastAPI server is started and CORS is enabled.
- The project is designed to work well with ERP-focused, finance-heavy, and compliance-driven business use cases.

## Result

This solution delivers an end-to-end agentic workflow for database design generation, making it suitable for data architects, enterprise analysts, and teams building ERP-aligned domain models quickly with AI assistance.

More details to come soon.
