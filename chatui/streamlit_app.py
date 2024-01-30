import streamlit as st
from pathlib import Path
from langchain.llms.openai import OpenAI
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.schema import ChatMessage
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
llm = OpenAI(openai_api_key=openai_api_key, temperature=0, streaming=True)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
toolkit.get_tools()

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [ChatMessage(role="assistant", avatar=assistant, content="How can I help you?")]

for msg in st.session_state.messages:
    if msg.role == "user":
        with st.chat_message("user", avatar=user):
            st.markdown(msg.content)
    elif msg.role == "assistant":
        with st.chat_message("assistant", avatar=assistant):
            st.markdown(msg.content)

prompt = st.chat_input(placeholder="Ask me anything!")

if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", avatar=user, content=prompt))
    st.chat_message("user", avatar=user).write(prompt)


    with st.chat_message("assistant", avatar=assistant):
        st_cb = StreamlitCallbackHandler(st.container())
        response = agent.run(prompt, callbacks=[st_cb])
        st.session_state.messages.append(ChatMessage(role="assistant", avatar=assistant, content=response))

