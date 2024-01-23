from langchain.agents import create_sql_agent
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.utilities import SQLDatabase
from dotenv import load_dotenv
from langchain.agents.agent_types import AgentType
from langchain.callbacks import get_openai_callback

load_dotenv()

dburi = "sqlite:///Pathways DB/database/pathways.db"
db = SQLDatabase.from_uri(dburi)

'''agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0),
    toolkit=SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0)),
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)'''

agent_executor = create_sql_agent(
     llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-1106"),
     toolkit=SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0)),
     verbose=True,
     agent_type=AgentType.OPENAI_FUNCTIONS
 )

while True:
    user_query = input("Enter your query (type 'end' to exit): ")

    if user_query.lower() == 'end':
        break 
    with get_openai_callback() as cb:
        result = agent_executor.run(user_query)
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")

    if isinstance(result, str):
        answer = result
    else:
        answer = result.get('Answer', 'No answer available.')

    print(f"Answer: {answer}")

