# # langgraph_flow.py
# from typing import TypedDict, Optional
# from langgraph.graph import END, StateGraph
# from langchain_core.runnables import Runnable
# from langchain_core.output_parsers import JsonOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_groq import ChatGroq
# import os

# # Load environment variable for Groq API key
# groq_api_key = os.getenv("GROQ_API_KEY")

# # LangGraph state definition
# class ERDState(TypedDict):
#     model_type: str
#     business_requirement: str
#     erp_system_name: Optional[str]
#     data_dictionary: Optional[str]
#     fantasy_mode: Optional[bool]
#     validated: Optional[bool]
#     enhanced_dict: Optional[str]
#     summary: Optional[str]
#     erd_json: Optional[dict]

# # Initialize Groq model
# model = ChatGroq(
#     model_name="llama3-70b-8192",
#     groq_api_key=groq_api_key,
#     temperature=0.3
# )

# # Node 1: Validate input
# def validate_input(state: ERDState) -> ERDState:
#     valid = bool(state['business_requirement'])
#     state['validated'] = valid
#     return state

# # Node 2: Enhance data dictionary (if file provided)
# def enhance_dictionary(state: ERDState) -> ERDState:
#     if state['data_dictionary']:
#         enhanced = f"Tables and columns detected:\n{state['data_dictionary']}"
#         state['enhanced_dict'] = enhanced
#     return state

# # Node 3: Generate ERD summary
# summary_prompt = ChatPromptTemplate.from_template(
#     """
# You are Schema Generator Pro. Given the ERP system, business requirement, and optionally a parsed data dictionary, summarize the business domains and orientation.

# ERP System: {erp_system_name}
# Business Requirement:
# {business_requirement}

# {enhanced_dict}

# Generate a clean, professional summary.
# """
# )
# summarizer = summary_prompt | model | (lambda x: {"summary": x.content})

# # Node 4: Generate ERD JSON
# erd_prompt = ChatPromptTemplate.from_template(
#     """
# You're a senior data architect. Based on the business requirement and enhanced data dictionary, generate a clean JSON ERD structure.

# Business Requirement Summary:
# {summary}

# {enhanced_dict}

# Output format:
# {{
#   "entities": [...],
#   "relationships": [...]
# }}
# Only return valid JSON.
# """
# )
# json_parser = JsonOutputParser()
# # erd_generator = erd_prompt | model | json_parser
# erd_generator = erd_prompt | model | json_parser | (lambda result: {"erd_json": result})

# # Node 5: Add fantasy tables (optional)
# def add_fantasy_modules(state: ERDState) -> ERDState:
#     if state.get("fantasy_mode") and state.get("erd_json"):
#         fantasy_entity = {
#             "name": "Audit_Log",
#             "attributes": [
#                 {"name": "log_id", "type": "int", "primary_key": True},
#                 {"name": "action", "type": "varchar"},
#                 {"name": "timestamp", "type": "datetime"}
#             ]
#         }
#         state["erd_json"]["entities"].append(fantasy_entity)
#     return state

# # Build the graph
# def get_graph():
#     builder = StateGraph(ERDState)
#     builder.add_node("validate", validate_input)
#     builder.add_node("enhance", enhance_dictionary)
#     builder.add_node("summarize", summarizer)
#     builder.add_node("generate_json", erd_generator)
#     builder.add_node("add_fantasy", add_fantasy_modules)

#     builder.set_entry_point("validate")
#     builder.add_edge("validate", "enhance")
#     builder.add_edge("enhance", "summarize")
#     builder.add_edge("summarize", "generate_json")
#     builder.add_edge("generate_json", "add_fantasy")
#     builder.add_edge("add_fantasy", END)

#     return builder.compile()

# # Example run
# if __name__ == "__main__":
#     workflow = get_graph()
#     result = workflow.invoke({
#         "model_type": "ERP-based",
#         "business_requirement": "We want to track sales orders and shipments",
#         "erp_system_name": "SAP",
#         "data_dictionary": "Table: Orders\nColumns: order_id, customer_id, order_date",
#         "fantasy_mode": True
#     })
#     from pprint import pprint
#     pprint(result['erd_json'])


# langgraph_flow.py
from typing import TypedDict, Optional
from langgraph.graph import END, StateGraph
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os

# Load environment variable for Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")

# LangGraph state definition
class ERDState(TypedDict):
    model_type: str
    business_requirement: str
    erp_system_name: Optional[str]
    data_dictionary: Optional[str]
    fantasy_mode: Optional[bool]
    validated: Optional[bool]
    enhanced_dict: Optional[str]
    summary: Optional[str]
    erd_json: Optional[dict]
    fantasy_entities: Optional[list]

# Initialize Groq model
model = ChatGroq(
    model_name="llama3-70b-8192",
    groq_api_key=groq_api_key,
    temperature=0.3
)

# Node 1: Validate input
def validate_input(state: ERDState) -> ERDState:
    state['validated'] = bool(state['business_requirement'])
    return state

# Node 2: Enhance data dictionary
def enhance_dictionary(state: ERDState) -> ERDState:
    if state['data_dictionary']:
        state['enhanced_dict'] = f"Tables and columns detected:\n{state['data_dictionary']}"
    return state

# Node 3: Generate ERD summary
summary_prompt = ChatPromptTemplate.from_template("""
You are Schema Generator Pro. Given the ERP system, business requirement, and optionally a parsed data dictionary, summarize the business domains and orientation.

ERP System: {erp_system_name}
Business Requirement:
{business_requirement}

{enhanced_dict}

Generate a clean, professional summary.
""")
summarizer = summary_prompt | model | (lambda x: {"summary": x.content})

# Node 4: Generate ERD JSON
erd_prompt = ChatPromptTemplate.from_template("""
You're a senior data architect. Based on the business requirement and enhanced data dictionary, generate a clean JSON ERD structure.

Business Requirement Summary:
{summary}

{enhanced_dict}

Output format:
{{
  "entities": [...],
  "relationships": [...]
}}
Only return valid JSON.
""")
json_parser = JsonOutputParser()
erd_generator = erd_prompt | model | json_parser | (lambda result: {"erd_json": result})

# Node 5a: Generate fantasy modules via LLM
fantasy_prompt = ChatPromptTemplate.from_template("""
You are a senior data architect.

Based on the current ERD JSON and business requirement, suggest 1–3 additional helpful fantasy tables.

ONLY return raw JSON. DO NOT include markdown or explanation.

Return format:
[
  {{
    "name": "FantasyEntity",
    "attributes": [
      {{"name": "attr1", "type": "type", "primary_key": true/false}}
    ]
  }}
]

Business Requirement:
{business_requirement}

ERD JSON:
{erd_json}
""")
fantasy_generator = fantasy_prompt | model | json_parser | (lambda result: {"fantasy_entities": result})

# Node 5b: Merge fantasy entities
def merge_fantasy(state: ERDState) -> ERDState:
    if state.get("fantasy_mode") and state.get("erd_json") and state.get("fantasy_entities"):
        state["erd_json"]["entities"].extend(state["fantasy_entities"])
    return state

# Build the graph
def get_graph():
    builder = StateGraph(ERDState)
    builder.add_node("validate", validate_input)
    builder.add_node("enhance", enhance_dictionary)
    builder.add_node("summarize", summarizer)
    builder.add_node("generate_json", erd_generator)
    builder.add_node("generate_fantasy", fantasy_generator)
    builder.add_node("merge_fantasy", merge_fantasy)

    builder.set_entry_point("validate")
    builder.add_edge("validate", "enhance")
    builder.add_edge("enhance", "summarize")
    builder.add_edge("summarize", "generate_json")
    builder.add_edge("generate_json", "generate_fantasy")
    builder.add_edge("generate_fantasy", "merge_fantasy")
    builder.add_edge("merge_fantasy", END)

    return builder.compile()

# Example run
if __name__ == "__main__":
    workflow = get_graph()
    result = workflow.invoke({
        "model_type": "ERP-based",
        "business_requirement": "We want to track sales orders and shipments",
        "erp_system_name": "SAP",
        "data_dictionary": "Table: Orders\nColumns: order_id, customer_id, order_date",
        "fantasy_mode": True
    })
    from pprint import pprint
    pprint(result['erd_json'])
