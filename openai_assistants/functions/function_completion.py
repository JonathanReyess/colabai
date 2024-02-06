import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import requests

#create our OpenAI client 

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 

#define our function to get the description of a course given its name

def get_course_description(name):
    url = "https://api.pathways.duke.edu/api/v1/courses"  
    params = {'name': name}
    headers = {'accept': '*/*'}
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()[0]['description']
    else:
        return f"Error: Unable to fetch coursedetails. Status code: {response.status_code}"
    
#print(get_course_description("Design & Laser Cut Jewelry with Rhino"))

#map function names to their corresponding functions 

available_functions = {
    "get_course_description": get_course_description,
}

#describe the functions for the API

functions = [
    {
        "name": "get_course_description",
        "description": "Retrieves the description of a course given its name ",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The name of a course."}
            },
            "required": ["name"],
        },
    }
]

def get_gpt_response(messages):
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=functions,
        function_call="auto",
    )

def execute_function_call(function_name,arguments):
    function = available_functions.get(function_name,None)
    if function:
        arguments = json.loads(arguments)
        results = function(**arguments)
    else:
        results = f"Error: function {function_name} does not exist"
    return results

#query = "What is Make Your Own Silicone Mold about?"
#query = "What's a course about making candles about?" #the problem with this is that OpenAI needs to first know the names of all courses available, otherwise, the name argument is not passed in properly in our api call
#query = "Tell me a joke"

messages = [{"role": "user", "content": query}] 
response = get_gpt_response(messages) ##this is not returning content from the function call yet 
#print(response.choices[0].message)

function_name = response.choices[0].message.function_call.name
arguments = response.choices[0].message.function_call.arguments
#print(function_name,arguments)


function_response = execute_function_call(function_name, arguments)
#print(function_response)

# extend conversation with assistant's reply
messages.append(response.choices[0].message)  
messages.append(
    {
        "role": "function",
        "name": function_name,
        "content": str(function_response),
    }
)
#print(messages)

call = get_gpt_response(messages)
print(call.choices[0].message.content)
