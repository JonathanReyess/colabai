import os
import base64
import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings, AzureOpenAI, AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
import uuid 

LOGO_IMAGE = "colab.png"

st.markdown(
    """
    <style>
    .container {
        display: flex;
        align-items: center;
    }
    .logo-text1 {
        margin-left: 10px;
        font-weight:700 !important;
        font-size:60px !important;
        color: #000000  !important;
        padding-top: 75px !important;
    }
    .logo-text2 {
        margin-left: 0px;
        font-weight:700 !important;
        font-size:60px !important;
        color: #5f97bf!important;
        padding-top: 75px !important;
    }
    .logo-img {
        margin-top: 61px;
        float:right;
        width: 100px;
        height: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
        <p class="logo-text1">CO-LAB&nbsp</p>
        <p class="logo-text2">CO-PILOT</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
            
<style>
	[data-testid="stDecoration"] {
		display: block;
        background-image: linear-gradient(90deg, rgb(0, 102, 204), rgb(102, 255, 255));
        position: absolute;
        top: 0px;
        right: 0px;
        left: 0px;
        height: 0.250rem;
	}
            
    [data-testid="stChatInput"]{
            
        background-color: rgba(0, 0, 0, 0);
            
        border-bottom-color: rgba(46,81,115,255);
        border-bottom-left-radius: 8px;
        border-bottom-right-radius: 8px;
        border-bottom-style: solid;
        border-bottom-width: 2px;
            
        border-left-color: rgba(46,81,115,255);
        border-left-style: solid;
        border-left-width: 2px;
            
        border-right-color: rgba(46,81,115,255);
        border-right-style: solid;
        border-right-width: 2px;
            
        border-top-color: rgba(46,81,115,255);
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        border-top-style: solid;
        border-top-width: 2px;
            
        box-sizing: border-box; 
    }
    
    [data-testid="stButton"]{
     
    }
    
    [data-testid="stMarkdownContainer"]{
            
    }
        
    [data-testid="baseButton-secondary"]{
            
    }
    [data-testid="stNotification"]{
        
        background-color: rgba(0, 0, 0, 0);
            
        border-bottom-color: rgba(46,81,115,255);
        border-bottom-left-radius: 4px;
        border-bottom-right-radius: 4px;
        border-bottom-style: solid;
        border-bottom-width: 2px;
            
        border-left-color: rgba(46,81,115,255);
        border-left-style: solid;
        border-left-width: 2px;
            
        border-right-color: rgba(46,81,115,255);
        border-right-style: solid;
        border-right-width: 2px;
            
        border-top-color: rgba(46,81,115,255);
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        border-top-style: solid;
        border-top-width: 2px;
            
        box-sizing: border-box; 
    }
            
    [data-testid="stChatMessage"]{
            
        background-color: rgba(255, 255, 255, 0.45);
        box-sizing: border-box; 
        border-top-color: rgba(0, 0, 0, 0);
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        border-top-style: solid;
        border-top-width: 2px;
            
    }

</style>""",

unsafe_allow_html=True)

    # Initialize connection.
    # Uses st.cache_resource to only run once.

user = "person-fill.svg"
assistant = "blue-bot.svg"

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["AZURE_OPENAI_ENDPOINT"]= st.secrets["AZURE_OPENAI_ENDPOINT"]


os.environ["OPENAI_API_TYPE"]  = st.secrets["OPENAI_API_TYPE"]
os.environ["OPENAI_API_VERSION"] = st.secrets["OPENAI_API_VERSION"]


uri = "mongodb+srv://" + st.secrets["uid"] + ":" + st.secrets["mdbpassword"] + st.secrets["address"] + ".mongodb.net/?retryWrites=true&w=majority"
#print(uri)
mdbClient = MongoClient(uri, server_api=ServerApi('1'))

db = mdbClient["Pathways"]
collection = db["Courses"]
sessions_collection = db['session_ids']

try:
    mdbClient.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


embedding_client = AzureOpenAIEmbeddings(azure_deployment="copilot-embedding", openai_api_version="2023-05-15",)

def get_text_embedding(input_text):
    response = embedding_client.embed_query(input_text)
    return response
#print(get_text_embedding("Hello"))

def pipeline(query):
    pipeline = [
                {"$vectorSearch": {
                    "queryVector": get_text_embedding(query),
                    "path": "description_embedding",
                    "numCandidates": 219,
                    "limit": 5,
                    "index": "vector_index",
                }},
        {
            "$project": {
                "_id": 0,
                "name": 1,
                "description": 1,
                'score': {
                    '$meta': 'vectorSearchScore'
      }
            
            }
        }
            ]
    return pipeline

def return_top_k(query):
    documents = collection.aggregate(pipeline(query))
    return list(documents)

def check_most_confident(documents):
    valid_documents = []
    for document in documents:
        if document['score'] > 0.73:
            valid_documents.append(document)
    if not valid_documents:
        return None
    return max(valid_documents, key=lambda x: x['score'])

def check_confidence(documents):
    valid_documents = []
    for document in documents:
        if document['score'] > 0.69:
            valid_documents.append(document)
    names = [entry['name'] for entry in valid_documents]

    return names


main_client = AzureChatOpenAI(openai_api_version="2023-05-15", deployment_name="colab-copilot", model_name="gpt-35-turbo")


template = """

You are a conversational assistant for Duke University's Innovation Co-Lab.  \

If the user asks a question mentioning Danai, you will respond with "He is straight up DAWG". \

Otherwise, you will use the information below to recommend them a course to take. \

Here is the question the user is asking: {message} \

This is the most relevant course: {course_list} \

These courses are related, but you should only return them if there is no most relevant course: {all_courses} \

If the user asks a question about a class, but the list is empty, tell the user there are no courses relating to that topic. \

If the user asks a question about a Duke University class (ie. CS250, CS201, CS330, CS350): You will tell them that the Co-Lab has in person office hours. \

If the user asks a question about a programming concept (linked-lists, graph traversal, recursion): You will tell them that the Co-Lab has in person office hours. \

Use three sentences maximum and keep the answer concise. \

"""

prompt = PromptTemplate(
    input_variables=["message", "course_list", "all_courses"],
    template=template
)

chain = LLMChain(llm=main_client, prompt=prompt, verbose=False)
  
def generate_response(message):
    courses = return_top_k(message)
    valid_courses = check_confidence(courses)
    most_valid_courses = check_most_confident(courses)
    print()
    print("****************This is the most valid course****************")
    print()
    print(most_valid_courses)
    print()
    print("****************These are valid courses****************")
    print()
    print(valid_courses)
    print()
    response = chain.run(message=message, course_list=most_valid_courses, all_courses=valid_courses)
    return response


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role":"assistant", "avatar":"assistant", "content":"How can I help you?"}]

reset_button_key = "reset_button"
reset_button = st.button("Reset Chat",key=reset_button_key)

if reset_button:

    st.session_state["messages"] = [{"role":"assistant", "avatar":"assistant", "content":"How can I help you?"}]
    

#if st.sidebar.button("Clear message history"):
     #st.session_state["messages"] = [{"role":"assistant", "avatar":"assistant", "content":"How can I help you?"}]

for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar=user):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant", avatar=assistant):
            st.markdown(msg["content"])

#prompt = st.chat_input(placeholder="Ask me anything!")

if prompt := st.chat_input(placeholder="Try 'Are there any classes about Python programming? or What is Intro to React about?' "):
    st.session_state.messages.append({"role":"user", "avatar":"user", "content": prompt })
    st.chat_message("user", avatar=user).write(prompt)

    # Generate and display response
    with st.chat_message("assistant", avatar=assistant):
        final = generate_response(prompt)
        st.session_state.messages.append({"role":"assistant", "avatar":"assistant", "content": final})
        st.write(final)

