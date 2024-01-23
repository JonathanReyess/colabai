from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from dotenv import load_dotenv

load_dotenv()

dburi = "sqlite:///Pathways DB/database/pathways.db"
db = SQLDatabase.from_uri(dburi)
llm = OpenAI(temperature=0, verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=False)

while True:
    user_query = input("Enter your query (type 'end' to exit): ")

    if user_query.lower() == 'end':
        break 

    result = db_chain.run(user_query)

    if isinstance(result, str):
        answer = result
    else:
        answer = result.get('Answer', 'No answer available.')

    print(f"Answer: {answer}")

