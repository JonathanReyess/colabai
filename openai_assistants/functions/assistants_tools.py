import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import requests
#from function_completion import get_course_description, execute_function_call


###Setup OpenAI Client

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 



###Define all functions here
def get_course_description(name):
    url = "https://api.pathways.duke.edu/api/v1/courses"  
    params = {'name': name}
    headers = {'accept': '*/*'}
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()[0]['description']
    else:
        return f"Error: Unable to fetch coursedetails. Status code: {response.status_code}"

###Define all available functions here    

available_functions = {
    "get_course_description": get_course_description,
}


###Define all tools here 
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_course_description",
            "description": "Retrieves the description of a course given its name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the course."
                    }
                },
                "required": ["name"]
            }
        }
    }
]


###Create your assistant here and modify names, instructions, model, and tools as needed
assistant = client.beta.assistants.create(
  name="Pathways Bot",
  instructions="You are a Pathways database Q&A bot. Use the provided functions to answer questions. Synthesize your answer based on provided function output and be concise.",
  model="gpt-4-1106-preview",
  tools = tools
)


###Call our function when needed
def execute_function_call(function_name,arguments):
    function = available_functions.get(function_name,None)
    if function:
        arguments = json.loads(arguments)
        results = function(**arguments)
    else:
        results = f"Error: function {function_name} does not exist"
    return results

query = "What is Intro to Python about?" 

###Create a message thread and run it 
def create_message_and_run(assistant,query,thread=None):
  if not thread:
    thread = client.beta.threads.create()

  message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=query
  )
  run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id
  )
  return run,thread

run,thread = create_message_and_run(assistant=assistant,query=query)

###Information about the function that we use 
def get_function_details(run):

  print("\nrun.required_action\n",run.required_action)

  function_name = run.required_action.submit_tool_outputs.tool_calls[0].function.name
  arguments = run.required_action.submit_tool_outputs.tool_calls[0].function.arguments
  function_id = run.required_action.submit_tool_outputs.tool_calls[0].id

  print(f"function_name: {function_name} and arguments: {arguments}")

  return function_name, arguments, function_id


def submit_tool_outputs(run,thread,function_id,function_response):
    run = client.beta.threads.runs.submit_tool_outputs(
    thread_id=thread.id,
    run_id=run.id,
    tool_outputs=[
      {
        "tool_call_id": function_id,
        "output": str(function_response),
      }
    ]
    ) 
    return run



while True:
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    print("run status", run.status)

    if run.status=="requires_action":

        function_name, arguments, function_id  = get_function_details(run)

        function_response = execute_function_call(function_name,arguments)

        run = submit_tool_outputs(run,thread,function_id,function_response)

        continue
    if run.status=="completed":

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        latest_message = messages.data[0]
        text = latest_message.content[0].text.value
        print(text)

        user_input = input()
        if user_input == "STOP":
          break

        run,thread = create_message_and_run(assistant=assistant,query=user_input,thread=thread)

        continue
    

