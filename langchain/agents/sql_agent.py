import os
from langchain_community.utilities import SQLDatabase
from langchain.chains.sql_database.prompt import SQL_PROMPTS
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings


openai_api_key = os.getenv("OPENAI_API_KEY")

dburi = "sqlite:///data/sample_database/pathways.db"
db = SQLDatabase.from_uri(dburi)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature="0")
chain = create_sql_query_chain(llm, db)
#chain.get_prompts()[0].pretty_print()

context = db.get_context()
#prompt_with_context = chain.get_prompts()[0].partial(table_info=context["table_info"])
#print(prompt_with_context.pretty_repr()[:1500])


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
    
]


example_prompt = PromptTemplate.from_template("User input: {input}\nSQL query: {query}")
prompt = FewShotPromptTemplate(
    examples=examples[:5],
    example_prompt=example_prompt,
    prefix="You are a SQLite expert. Given an input question, create a syntactically correct SQLite query to run. Unless otherwise specificed, do not return more than {top_k} rows.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries.",
    suffix="User input: {input}\nSQL query: ",
    input_variables=["input", "top_k", "table_info"],
)

print(prompt.format(input="How many artists are there?", top_k=3, table_info=context["table_info"]))

