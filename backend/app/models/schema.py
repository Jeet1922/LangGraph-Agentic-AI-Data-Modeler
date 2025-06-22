# app/models/schema.py
from typing import Optional, List
from pydantic import BaseModel

class StepRequest(BaseModel):
    model_type: str
    business_requirement: str
    erp_system_name: Optional[str] = None
    data_dictionary: Optional[str] = None

class StepResponse(BaseModel):
    status: str
    result: str
