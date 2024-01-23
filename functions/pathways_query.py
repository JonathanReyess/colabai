import requests
import json

def get_courses():
    headers = {
        'accept': '*/*',
    }

    response = requests.get('https://api.pathways.duke.edu/api/v1/courses?published=true', headers=headers)
    return response.json()

print(get_courses())

'''
client = OpenAI()
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[{"role": "user", "content": "Give me a list of all courses"},{"role": "function", "name": get_courses, "content":""} ],
  functions = functions,
)
#print(completion.choices[0].message.content)

response = completion.choices[0].message.content
print(response)'''
