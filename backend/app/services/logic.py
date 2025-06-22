from app.models.schema import StepRequest
from app.services.llm_client import call_groq
import json
from typing import List, Optional


# ---------- STEP 1 ----------
async def handle_step1(request: StepRequest) -> str:
    prompt = (
        f"The user wants to generate a data model for an ERP system."
        f"\n\nERP System: {request.erp_system_name or 'Not specified'}"
        f"\n\nBusiness Requirement:\n{request.business_requirement}"
    )

    if request.data_dictionary:
        prompt += (
            f"\n\nThe user also provided the following data dictionary information "
            f"(tables and fields):\n{request.data_dictionary}\n\n"
            f"Use this to infer relevant modules and help structure the data model better."
        )
    else:
        prompt += "\n\nThe user did not provide a data dictionary."

    prompt += "\n\nStart by identifying key business domains and inferring ERP modules or entities."

    response = await call_groq(prompt)
    return response


# ---------- STEP 2 ----------
async def extract_erd_insights(requirement_summary: str, data_dictionary: Optional[str] = None) -> str:
    prompt = f"""
You're an expert data modeler.

Based on the business requirement summary and optional data dictionary, generate ERD insights.

Business Requirement Summary:
{requirement_summary}

{f"Data Dictionary:\n{data_dictionary}" if data_dictionary else "No data dictionary was provided."}

Respond with:
1. Key Entities (name and short description)
2. Main Attributes per entity
3. Relationships (1:N, N:M, etc.) between entities

Use Markdown for formatting.
"""
    return await call_groq(prompt)



async def generate_erd_json(requirement_summary: str, data_dictionary: Optional[str] = None) -> dict:
    prompt = f"""
You are a senior database architect.

Based on the business requirement and optional data dictionary, return a clean JSON representing an ERD model.

Business Requirement:
{requirement_summary}

{f"Data Dictionary:\n{data_dictionary}" if data_dictionary else "No data dictionary was provided."}


Please follow this format:

{{
  "entities": [
    {{
      "name": "EntityName",
      "attributes": [
        {{
          "name": "attribute_name",
          "type": "datatype",
          "primary_key": true/false,
          "foreign_key": "ReferencedEntity.Attribute" (optional)
        }}
      ]
    }}
  ],
  "relationships": [
    {{
      "from_entity": "EntityA",
      "to_entity": "EntityB",
      "type": "1:N or N:M",
      "description": "What the relationship means",
      "join_condition": "EntityA.foreign_key = EntityB.primary_key"
    }}
  ]
}}

Return only JSON. No explanation.
    """

    response_str = await call_groq(prompt)

    try:
        return json.loads(response_str)
    except json.JSONDecodeError as e:
        # Optional: return raw string and error for debugging
        return {
            "success": False,
            "error": "Invalid JSON received from LLM",
            "raw_response": response_str
        }
