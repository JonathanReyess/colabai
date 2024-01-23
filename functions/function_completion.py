from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

# For Agent and Tools
from langchain.agents import AgentType
from langchain.agents import initialize_agent, Tool
from langchain.tools import BaseTool, format_tool_to_openai_function
from pydantic import BaseModel, Field
from typing import Optional, Type, List
import json
import requests

# For Message schemas
from langchain.schema import HumanMessage, AIMessage, ChatMessage, FunctionMessage
from dotenv import load_dotenv
import os

load_dotenv('.env')

function_definitions = [
    {
        'name': 'get_courses',
        'description': 'Get a list of pathways courses',
        'parameters': {
            'type': 'object',
            'properties': {
                'name': {
                    'type': 'string',
                    'description': 'Name of the course'
                }
            }
         }
    },
    {
        'name': 'get_course_description',
        'description': 'What is the course about?',
        'parameters': {
            'type': 'object',
            'properties': {
                'description': {
                    'type': 'string',
                    'description': 'Details about the course'
                }
            }
         }
    }
]

class Course(BaseModel):
    id: int
    department_id: int
    department_name: str
    name: str
    description: str
    materials: str
    objectives: str
    tools: str
    featured_at: Optional[str]
    published_at: str
    archived_at: Optional[str]
    created_at: str
    updated_at: str
    default_location_id: Optional[int]
    default_size: Optional[str]



headers = {'accept': '*/*'}
response = requests.get('https://api.pathways.duke.edu/api/v1/courses', headers=headers)
json_data = response.json()


def get_courses():
    course_names = [course['name'] for course in json_data]
    return course_names


def get_course_description(course_name):
    for course in json_data:
        if course['name'] == course_name:
            return course['description']
    return None  


description = get_course_description('Advanced Epoxy: Make a Hand Shaped Bowl')

#print(description)



#print(get_courses())


class GetCoursesCheckInput(BaseModel):
    pass  # No arguments for get_courses

class GetCoursesTool(BaseTool):
    name = "get_courses"
    description = "Used to get a list of courses"

    def _run(self, query: Optional[str] = None):
        if query:
            # If a query is provided, filter courses based on the description
            courses_data = get_courses()
            filtered_courses = [course for course in courses_data if query.lower() in course['description'].lower()]
            return filtered_courses
        else:
            # If no query is provided, return the full list of courses
            return get_courses()

    def _arun(self):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = GetCoursesCheckInput
    courses_output_schema: Optional[Type[BaseModel]] = List[Course]


tools = [GetCoursesTool()]
functions = [format_tool_to_openai_function(tool) for tool in tools]

query = input("Question: ")

model = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
)

# Assume you have already defined the 'functions' list as per your tools
response_ai_message = model.predict_messages([HumanMessage(content=query)], functions=functions)

# Print the response
#print(response_ai_message)

# Extract function call details from the response
function_call_details = response_ai_message.additional_kwargs.get('function_call', {})

#print(function_call_details)

if function_call_details:
    arguments = json.loads(function_call_details.get('arguments', '{}'))
    #print(arguments)

if function_call_details and function_call_details['name'] == 'get_courses':
    courses_result = get_courses()
    #print(courses_result)


# Assume that the tool result is stored in the 'arguments' variable obtained from Step 4
# For the sake of this example, we will use the actual result from the get_courses function
arguments = get_courses()

# Create a FunctionMessage with the tool name and the content as a string representation of the tool result
function_message = FunctionMessage(name="get_courses", content=str(arguments))

messages = [
    HumanMessage(content=query),
    response_ai_message,
    function_message,
]

# Predict the final response from the model
response_final = model.predict_messages(messages, functions=functions)
print(response_final)