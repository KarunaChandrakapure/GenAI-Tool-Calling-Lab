import os
from dotenv import load_dotenv
from openai import OpenAI
import database
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
response = client.responses.create(model="gpt-5-mini",input="How many Helmet alerts did Camera_1 generate?",tools=tools)
# print(response.output)
for item in response.output:
    print("TYPE",item.type)

    if item.type=="function_call":
        print("TOOL:",item.name)
        print("ARGUMENTS:",item.arguments)
        print("CALL_ID:",item.call_id)