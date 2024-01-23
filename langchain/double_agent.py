from langchain.chains import create_sql_query_chain
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.utilities import SQLDatabase
from langchain.callbacks import get_openai_callback
import sqlite3
from operator import itemgetter
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough

load_dotenv()

dburi = "sqlite:///Pathways DB/database/pathways.db"
db = SQLDatabase.from_uri(dburi)

chain = create_sql_query_chain(ChatOpenAI(temperature=0), db)

user_query = input("Enter your query (type 'end' to exit): ")

with get_openai_callback() as cb:
    response = chain.invoke({"question": user_query})
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Total Cost (USD): ${cb.total_cost}")

    if isinstance(response, str):
        answer = response
    else:
        answer = response.get('Answer', 'No answer available.')

conn = sqlite3.connect('Pathways DB/database/pathways.db')
curr = conn.cursor()

data = curr.execute(answer)

temp1 = data.fetchone()
print(temp1)

