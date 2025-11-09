

# app/api/langgraph_routes.py
from fastapi import APIRouter, UploadFile, File, Form
from app.langgraph_flow import get_graph
from app.services.llm_client import call_groq
from pydantic import BaseModel
from typing import Optional, Dict, Any
import pandas as pd
import json

router = APIRouter()
workflow = get_graph()

# Request models
class DDLRequest(BaseModel):
    erd_json: Dict[str, Any]
    db_type: Optional[str] = "postgresql"  # postgresql, mysql, sqlite, etc.

class SyntheticDataRequest(BaseModel):
    erd_json: Dict[str, Any]
    num_rows: Optional[int] = 100  # Number of rows per table
    format: Optional[str] = "json"  # json, csv, sql

@router.post("/generate-erd")
async def generate_erd(
    model_type: str = Form(...),
    business_requirement: str = Form(...),
    erp_system_name: str = Form(default=""),
    fantasy_mode: str = Form(default="false"),  # Accept as string to handle form data properly
    file: UploadFile = File(default=None)
):
    try:
        # Validate required fields
        if not model_type or not model_type.strip():
            return {
                "success": False,
                "error": "model_type is required and cannot be empty"
            }
        if not business_requirement or not business_requirement.strip():
            return {
                "success": False,
                "error": "business_requirement is required and cannot be empty"
            }
        
        # Convert fantasy_mode string to boolean (handle None, empty string, or various true values)
        if not fantasy_mode:
            fantasy_mode_bool = False
        else:
            fantasy_mode_bool = str(fantasy_mode).lower() in ("true", "1", "yes", "on")
        
        # Handle erp_system_name
        erp_system_name_clean = erp_system_name.strip() if erp_system_name else ""
        
        # Extract and format data dictionary if file is provided
        data_dictionary = None
        if file and file.filename:
            try:
                # Reset file pointer to beginning
                file.file.seek(0)
                df = pd.read_excel(file.file)
                if "Table Name" not in df.columns or "Column Name" not in df.columns:
                    return {
                        "success": False,
                        "error": "Excel must contain 'Table Name' and 'Column Name' columns."
                    }
                grouped = df.groupby("Table Name")["Column Name"].apply(list)
                data_lines = [f"Table: {table}\nColumns: {', '.join(cols)}" for table, cols in grouped.items()]
                data_dictionary = "\n\n".join(data_lines)
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Excel parsing error: {str(e)}"
                }

        # Run LangGraph workflow (invoke is synchronous, so run in thread pool to avoid blocking)
        import asyncio
        try:
            # Run the synchronous workflow.invoke in a thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: workflow.invoke({
                    "model_type": model_type.strip(),
                    "business_requirement": business_requirement.strip(),
                    "erp_system_name": erp_system_name_clean,
                    "data_dictionary": data_dictionary,
                    "fantasy_mode": fantasy_mode_bool
                })
            )
        except Exception as e:
            error_msg = str(e)
            import traceback
            error_trace = traceback.format_exc()
            print(f"ERD Generation Error: {error_msg}\n{error_trace}")  # Log for debugging
            
            # Check if it's a model-related error
            if "model" in error_msg.lower() or "decommissioned" in error_msg.lower() or "400" in error_msg:
                return {
                    "success": False,
                    "error": f"Model/API error: {error_msg}. Please check your Groq API key and model configuration."
                }
            return {
                "success": False,
                "error": f"Error during ERD generation: {error_msg}"
            }

        # Validate the result
        if not result:
            return {
                "success": False,
                "error": "ERD generation returned empty result. Please try again."
            }

        return {
            "success": True,
            "erd_json": result.get("erd_json"),
            "summary": result.get("summary"),
            "fantasy_entities": result.get("fantasy_entities")  # return LLM-generated fantasy entities
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }

@router.post("/generate-ddl")
async def generate_ddl(request: DDLRequest):
    """
    Generate DDL (Data Definition Language) statements for the ERD.
    """
    try:
        erd_json = request.erd_json
        db_type = request.db_type or "postgresql"
        
        # Validate ERD JSON structure
        if not erd_json or "entities" not in erd_json:
            return {
                "success": False,
                "error": "Invalid ERD JSON: missing 'entities' field"
            }
        
        # Create a more concise prompt for DDL generation
        # Format entities in a cleaner way to reduce token usage
        entities_str = ""
        for entity in erd_json.get("entities", []):
            entity_name = entity.get("name", "Unknown")
            attributes = entity.get("attributes", []) or entity.get("columns", [])
            attrs_str = ", ".join([
                f"{attr.get('name')} ({attr.get('type', 'string')})" + 
                (" PK" if attr.get("primary_key") or attr.get("primaryKey") else "") +
                (" FK" if attr.get("foreign_key") or attr.get("foreignKey") else "")
                for attr in attributes
            ])
            entities_str += f"\n- {entity_name}: {attrs_str}"
        
        relationships_str = ""
        for rel in erd_json.get("relationships", []):
            from_entity = rel.get("from") or rel.get("from_entity", "Unknown")
            to_entity = rel.get("to") or rel.get("to_entity", "Unknown")
            rel_type = rel.get("type", "unknown")
            relationships_str += f"\n- {from_entity} -> {to_entity} ({rel_type})"
        
        prompt = f"""Generate SQL DDL statements for {db_type} database based on this ERD:

Entities:
{entities_str}

Relationships:
{relationships_str}

Requirements:
- CREATE TABLE for each entity
- Proper {db_type} data types (string->VARCHAR, int->INTEGER, date->DATE)
- PRIMARY KEY constraints
- FOREIGN KEY constraints from relationships
- NOT NULL where appropriate
- Indexes on foreign keys

Return ONLY SQL DDL statements, no markdown or explanations."""
        
        system_message = "You are an expert database architect. Generate clean, production-ready SQL DDL statements."
        ddl = await call_groq(prompt, system_message)
        
        return {
            "success": True,
            "ddl": ddl.strip(),
            "db_type": db_type
        }
    except Exception as e:
        error_message = str(e)
        # Clean up error messages for better UX
        if "Groq API error" in error_message:
            return {
                "success": False,
                "error": error_message
            }
        else:
            return {
                "success": False,
                "error": f"Error generating DDL: {error_message}"
            }

@router.post("/generate-synthetic-data")
async def generate_synthetic_data(request: SyntheticDataRequest):
    """
    Generate synthetic dataset based on the ERD structure.
    """
    try:
        erd_json = request.erd_json
        num_rows = request.num_rows or 100
        format_type = request.format or "json"
        
        # Validate and limit num_rows to prevent excessive generation
        if num_rows > 1000:
            num_rows = 1000  # Cap at 1000 rows per table
        
        # Validate ERD JSON structure
        if not erd_json or "entities" not in erd_json:
            return {
                "success": False,
                "error": "Invalid ERD JSON: missing 'entities' field"
            }
        
        # Create a more concise prompt
        entities_info = []
        for entity in erd_json.get("entities", []):
            entity_name = entity.get("name", "Unknown")
            attributes = entity.get("attributes", []) or entity.get("columns", [])
            attrs = [f"{attr.get('name')} ({attr.get('type', 'string')})" for attr in attributes[:10]]  # Limit attributes
            entities_info.append(f"{entity_name}: {', '.join(attrs)}")
        
        entities_str = "\n".join(entities_info[:20])  # Limit to 20 entities
        
        relationships_info = []
        for rel in erd_json.get("relationships", []):
            from_entity = rel.get("from") or rel.get("from_entity", "Unknown")
            to_entity = rel.get("to") or rel.get("to_entity", "Unknown")
            relationships_info.append(f"{from_entity} -> {to_entity}")
        
        relationships_str = "\n".join(relationships_info[:20])  # Limit relationships
        
        # Build detailed entity information with data types
        detailed_entities = []
        for entity in erd_json.get("entities", []):
            entity_name = entity.get("name", "Unknown")
            attributes = entity.get("attributes", []) or entity.get("columns", [])
            attr_details = []
            for attr in attributes[:15]:  # Limit to 15 attributes per entity
                attr_name = attr.get("name", "")
                attr_type = attr.get("type", "string").lower()
                is_pk = attr.get("primary_key") or attr.get("primaryKey", False)
                is_fk = attr.get("foreign_key") or attr.get("foreignKey", False)
                pk_marker = " (PRIMARY KEY)" if is_pk else ""
                fk_marker = " (FOREIGN KEY)" if is_fk else ""
                attr_details.append(f"{attr_name}: {attr_type}{pk_marker}{fk_marker}")
            detailed_entities.append(f"Table: {entity_name}\n  Columns: {', '.join(attr_details)}")
        
        entities_detail = "\n\n".join(detailed_entities[:10])  # Limit to 10 entities for prompt
        
        # Create format-specific instructions
        if format_type.lower() == "json":
            format_instructions = """Return ONLY valid JSON in this exact format (no markdown, no code blocks):
{
  "TableName1": [
    {"column1": "value1", "column2": "value2", ...},
    {"column1": "value3", "column2": "value4", ...}
  ],
  "TableName2": [
    {"column1": "value1", "column2": "value2", ...}
  ]
}"""
        elif format_type.lower() == "csv":
            format_instructions = """Return CSV data in this format (one table per section):
=== TableName1 ===
column1,column2,column3
value1,value2,value3
value4,value5,value6

=== TableName2 ===
column1,column2
value1,value2"""
        else:  # SQL
            format_instructions = """Return SQL INSERT statements in this format:
INSERT INTO TableName1 (column1, column2, column3) VALUES
('value1', 'value2', 'value3'),
('value4', 'value5', 'value6');

INSERT INTO TableName2 (column1, column2) VALUES
('value1', 'value2'),
('value3', 'value4');"""
        
        prompt = f"""Generate exactly {num_rows} rows of realistic synthetic data for each table in {format_type.upper()} format.

Database Schema:
{entities_detail}

Relationships:
{relationships_str}

CRITICAL REQUIREMENTS:
1. Generate exactly {num_rows} rows per table
2. Use realistic values based on column names and data types:
   - For 'id', 'uuid', 'guid': Generate unique identifiers
   - For 'name', 'title', 'description': Generate realistic text
   - For 'email': Generate valid email addresses
   - For 'date', 'created_at', 'updated_at': Generate dates in YYYY-MM-DD or ISO format
   - For 'amount', 'price', 'debit', 'credit': Generate numeric values
   - For 'status', 'type': Generate appropriate enum-like values
   - For boolean fields: Use true/false or 1/0
3. Respect foreign key relationships - foreign key values must reference valid primary keys
4. Ensure primary keys are unique
5. For numeric types (int, decimal, float): Generate appropriate numeric values
6. For string types: Generate realistic text (names, descriptions, etc.)

{format_instructions}

IMPORTANT: Return ONLY the data in the requested format. Do NOT include Python code, explanations, or markdown code blocks. Just the raw data."""
        
        system_message = "You are an expert in generating realistic, consistent synthetic datasets. Generate data directly in the requested format (JSON/CSV/SQL), not Python code. Ensure all data is valid and respects database constraints."
        synthetic_data = await call_groq(prompt, system_message)
        
        return {
            "success": True,
            "data": synthetic_data.strip(),
            "format": format_type,
            "num_rows": num_rows
        }
    except Exception as e:
        error_message = str(e)
        # Clean up error messages for better UX
        if "Groq API error" in error_message:
            return {
                "success": False,
                "error": error_message
            }
        else:
            return {
                "success": False,
                "error": f"Error generating synthetic data: {error_message}"
            }
