from openai import OpenAI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


client = OpenAI()
def get_text_embedding(input_text):
    response = client.embeddings.create(
        input=input_text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding




uri = "mongodb+srv://jonathanreyes:.zc2luy2.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
mdbClient = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    mdbClient.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = mdbClient["Pathways"]

col = db["Courses"]

 
documents = col.aggregate([
            {"$vectorSearch": {
                "queryVector": get_text_embedding("JavaScript"),
                "path": "description_embedding",
                "numCandidates": 219,
                "limit": 5,
                "index": "coursesDescriptionIndex",
            }},
    {
        "$project": {
            "_id": 0,
            "name": 1,
           
        }
    }
        ])

print(list(documents))




