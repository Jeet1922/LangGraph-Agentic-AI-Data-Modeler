# app/api/routes.py
from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import List
import pandas as pd

from app.models.schema import StepRequest
from app.services.logic import handle_step1, extract_erd_insights, generate_erd_json

router = APIRouter()

# ---------- Step 1 Endpoint (Updated to support form + file) ----------
@router.post("/step1")
async def step1_logic(
    model_type: str = Form(...),
    business_requirement: str = Form(...),
    erp_system_name: str = Form(None),
    file: UploadFile = File(None)
):
    data_dictionary = None

    if file:
        try:
            df = pd.read_excel(file.file)
            if "Table Name" not in df.columns or "Column Name" not in df.columns:
                raise ValueError("Excel file must contain 'Table Name' and 'Column Name' columns.")

            grouped = df.groupby("Table Name")["Column Name"].apply(list)
            data_lines = [f"Table: {table}\nColumns: {', '.join(columns)}" for table, columns in grouped.items()]
            data_dictionary = "\n\n".join(data_lines)

        except Exception as e:
            return {"success": False, "error": f"Failed to parse Excel: {str(e)}"}

    request = StepRequest(
        model_type=model_type,
        business_requirement=business_requirement,
        erp_system_name=erp_system_name,
        data_dictionary=data_dictionary
    )

    try:
        response = await handle_step1(request)
        return {"success": True, "result": response}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ---------- Step 2 Model ----------
class ERDRequest(BaseModel):
    modules: List[str]
    summary: str

@router.post("/step2")
async def generate_erd_insights(payload: ERDRequest):
    try:
        response = await extract_erd_insights(payload.modules, payload.summary)
        return {"success": True, "erd_insights": response}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ---------- Step 3 Endpoint ----------
class Step3Request(BaseModel):
    modules: List[str]
    summary: str

@router.post("/step3")
async def step3_erd_json(request: Step3Request):
    try:
        response = await generate_erd_json(request.modules, request.summary)
        return {"success": True, "erd_json": response}
    except Exception as e:
        return {"success": False, "error": str(e)}
