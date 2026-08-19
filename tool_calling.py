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
            "If the tool returns an error, analyze the error and generate "
            "a corrected SQL query and call the tool again."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "A valid SQL SELECT query using the alerts table. "
                        "The table contains: id, date, time, camera, alert_type."
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

response = client.responses.create(model="gpt-5-mini",input=user_question,tools=tools)


#-------------------------------------------------------------------------
# 2. SECOND LLM CALL
#-------------------------------------------------------------------------
MAX_TOOL_CALLS = 5
tool_call_count = 0

while True:

    # Check the limit before executing another tool
    if tool_call_count >= MAX_TOOL_CALLS:
        print("\nMAX TOOL CALL LIMIT REACHED")
        break

    tool_call_found = False

    for item in response.output:

        if item.type != "function_call":
            continue

        tool_call_found = True
        tool_call_count += 1

        print(f"\n========== TOOL CALL #{tool_call_count} ==========")

        tool_name = item.name
        arguments = json.loads(item.arguments)
        call_id = item.call_id

        print("TOOL:", tool_name)
        print("ARGUMENTS:", arguments)

        if tool_name == "execute_sql":

            query = arguments["query"]

            print("SQL:", query)

            result = execute_sql(query)

            print("TOOL RESULT:", result)

            response = client.responses.create(
                model="gpt-5-mini",
                previous_response_id=response.id,
                input=[
                    {
                        "type": "function_call_output",
                        "call_id": call_id,
                        "output": str(result)
                    }
                ],
                tools=tools
            )

        break


    # If the model didn't request a tool,
    # we're finished.
    if not tool_call_found:
        break


print("\nTOTAL TOOL CALLS:", tool_call_count)

print("\nFINAL ANSWER:")
print(response.output_text)
       
        
            

            

            




        
