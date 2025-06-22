# # app/api/langgraph_routes.py
# from fastapi import APIRouter, UploadFile, File, Form
# from app.langgraph_flow import get_graph
# import pandas as pd

# router = APIRouter()
# workflow = get_graph()

# @router.post("/generate-erd")
# async def generate_erd(
#     model_type: str = Form(...),
#     business_requirement: str = Form(...),
#     erp_system_name: str = Form(None),
#     fantasy_mode: bool = Form(False),
#     file: UploadFile = File(None)
# ):
#     # Extract and format data dictionary if file is provided
#     data_dictionary = None
#     if file:
#         try:
#             df = pd.read_excel(file.file)
#             if "Table Name" not in df.columns or "Column Name" not in df.columns:
#                 raise ValueError("Excel must contain 'Table Name' and 'Column Name' columns.")
#             grouped = df.groupby("Table Name")["Column Name"].apply(list)
#             data_lines = [f"Table: {table}\nColumns: {', '.join(cols)}" for table, cols in grouped.items()]
#             data_dictionary = "\n\n".join(data_lines)
#         except Exception as e:
#             return {"success": False, "error": f"Excel parsing error: {str(e)}"}

#     # Run LangGraph workflow
#     result = workflow.invoke({
#         "model_type": model_type,
#         "business_requirement": business_requirement,
#         "erp_system_name": erp_system_name,
#         "data_dictionary": data_dictionary,
#         "fantasy_mode": fantasy_mode
#     })

#     return {
#         "success": True,
#         "erd_json": result.get("erd_json"),
#         "summary": result.get("summary")
#     }

# app/api/langgraph_routes.py
from fastapi import APIRouter, UploadFile, File, Form
from app.langgraph_flow import get_graph
import pandas as pd

router = APIRouter()
workflow = get_graph()

@router.post("/generate-erd")
async def generate_erd(
    model_type: str = Form(...),
    business_requirement: str = Form(...),
    erp_system_name: str = Form(None),
    fantasy_mode: bool = Form(False),
    file: UploadFile = File(None)
):
    # Extract and format data dictionary if file is provided
    data_dictionary = None
    if file:
        try:
            df = pd.read_excel(file.file)
            if "Table Name" not in df.columns or "Column Name" not in df.columns:
                raise ValueError("Excel must contain 'Table Name' and 'Column Name' columns.")
            grouped = df.groupby("Table Name")["Column Name"].apply(list)
            data_lines = [f"Table: {table}\nColumns: {', '.join(cols)}" for table, cols in grouped.items()]
            data_dictionary = "\n\n".join(data_lines)
        except Exception as e:
            return {"success": False, "error": f"Excel parsing error: {str(e)}"}

    # Run LangGraph workflow
    result = workflow.invoke({
        "model_type": model_type,
        "business_requirement": business_requirement,
        "erp_system_name": erp_system_name,
        "data_dictionary": data_dictionary,
        "fantasy_mode": fantasy_mode
    })

    return {
        "success": True,
        "erd_json": result.get("erd_json"),
        "summary": result.get("summary"),
        "fantasy_entities": result.get("fantasy_entities")  # return LLM-generated fantasy entities
    }
