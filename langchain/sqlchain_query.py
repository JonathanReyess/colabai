from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.callbacks import get_openai_callback
import os


openai_api_key = os.getenv("OPENAI_API_KEY")

dburi = "sqlite:///data/sample_database/pathways.db"
db = SQLDatabase.from_uri(dburi)

#print(db.dialect)
#print(db.get_usable_table_names())
#print(db.run("SELECT * FROM courses LIMIT 10;")) 


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)
answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

answer = answer_prompt | llm | StrOutputParser()
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer
)


while True:
    user_query = input("Enter your query (type 'end' to exit): ")

    if user_query.lower() == 'end':
        break 

    with get_openai_callback() as cb:
        result = chain.invoke({"question": user_query})
        #print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")

    print(f"Answer: {result}")

