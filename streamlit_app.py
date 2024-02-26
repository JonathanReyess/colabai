import streamlit as st
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain.chains.sql_database.prompt import SQL_PROMPTS
from langchain_community.vectorstores import FAISS
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import (ChatPromptTemplate, FewShotPromptTemplate, MessagesPlaceholder, PromptTemplate, 
                                    SystemMessagePromptTemplate,)
from langchain_openai import OpenAIEmbeddings
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
import base64
import pyodbc


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
  

driver = '{ODBC Driver 18 for SQL Server}'

# Construct the ODBC connection string using st.secrets
odbc_str = (
    'mssql+pyodbc:///?odbc_connect='
    'Driver=' + driver +
    ';Server=tcp:' + st.secrets["server"] + ';PORT=1433' +
    ';DATABASE=' + st.secrets["database"] +
    ';Uid=' + st.secrets["username"] +
    ';Pwd=' + st.secrets["password"] +
    ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
)

# Create the SQLAlchemy engine
db_engine = create_engine(odbc_str)
db = SQLDatabase(db_engine)
openai_api_key = st.secrets["OPENAI_API_KEY"]
user = "person-fill.svg"
assistant = "blue-bot.svg"
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)


examples = [
    {"input": "Give me some art classes", 
     "query": "SELECT * FROM courses WHERE description LIKE '% Art %' OR name LIKE '% Art %';"
     },
    {
        "input": "What's a course about making candles about?",
        "query": "SELECT description FROM courses WHERE name LIKE '%candle%';",
    },
    {
        "input": "I want to learn to make video games",
        "query": "SELECT * FROM courses WHERE description LIKE '% unity %';",
    },
    {
        "input": "Are there any classes about video games?",
        "query": "SELECT * FROM courses WHERE description LIKE '% unity %';",
    },
    {
        "input": "Are there any classes about Java?", 
        "query": "SELECT * FROM courses WHERE description LIKE '% Java %' OR name LIKE '% Java %';"
    },
    
]

example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    FAISS,
    k=5,
    input_keys=["input"],
)

system_prefix = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 3 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the given tools. Only use the information returned by the tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database, just return "I don't know" as the answer.

Here are some examples of user inputs and their corresponding SQL queries:"""

few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=PromptTemplate.from_template(
        "User input: {input}\nSQL query: {query}"
    ),
    input_variables=["input", "dialect", "top_k"],
    prefix=system_prefix,
    suffix="",
)

full_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(prompt=few_shot_prompt),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

agent = create_sql_agent(
    llm=llm,
    db=db,
    prompt=full_prompt,
    verbose=False,
    agent_type="openai-tools",
)

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

prompt = st.chat_input(placeholder="Ask me anything!")

if prompt := st.chat_input():
    st.session_state.messages.append({"role":"user", "avatar":"user", "content": prompt })
    st.chat_message("user", avatar=user).write(prompt)


    with st.chat_message("assistant", avatar=assistant):
        #st_cb = StreamlitCallbackHandler(st.container())
        #response = agent.run(prompt, callbacks=[st_cb])
        response = agent.run(prompt)
        st.session_state.messages.append({"role":"assistant", "avatar":"assistant", "content": response})
        st.write(response)
