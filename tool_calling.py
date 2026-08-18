import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from database import execute_sql
load_dotenv()

client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



tools = [
    {
        "type": "function",
        "name": "execute_sql",
        "description": (
            "Execute a read-only SQL SELECT query against the alerts database. "
            "Use this tool when the user asks a question that requires "
            "information from the alerts database."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "A valid SQL SELECT query using the alerts table. "
                        "The table contains: id, date, time, camera_name, alert_type."
                    )
                }
            },
            "required": ["query"],
            "additionalProperties": False
        },
        "strict": True
    }
]

#-------------------------------------------------------------------------
# 1. FIRST LLM CALL
#-------------------------------------------------------------------------
user_question = input("Ask a question: ")

first_response = client.responses.create(model="gpt-5-mini",input=user_question,tools=tools)
print(first_response.output_text)

#-------------------------------------------------------------------------
# 1. SECOND LLM CALL
#-------------------------------------------------------------------------
for item in first_response.output:
    if item.type=="function_call":
       tool_name = item.name
       arguments = json.loads(item.arguments)
       call_id = item.call_id
       if tool_name=="execute_sql":
        query= arguments["query"]
        #  actual python tool
        result = execute_sql(query)
        print("TOOL:", tool_name)
        print("ARGUMENTS:", arguments)
        print("DATABASE RESULT:", result)

        second_response = client.responses.create(
            model="gpt-5-mini",
            previous_response_id=first_response.id,
            input=[
                {
                    "type":"function_call_output",
                    "call_id":call_id,
                    "output":str(result)
                }
            ]
        )
        print(second_response.output_text) 


        
