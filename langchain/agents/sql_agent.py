import os
from langchain_community.utilities import SQLDatabase
from langchain.chains.sql_database.prompt import SQL_PROMPTS
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.callbacks import get_openai_callback


openai_api_key = os.getenv("OPENAI_API_KEY")

dburi = "sqlite:///data/sample_database/pathways.db"
db = SQLDatabase.from_uri(dburi)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=False)
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
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
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


while True:
    user_query = input("Enter your query (type 'end' to exit): ")

    if user_query.lower() == 'end':
        break 

    with get_openai_callback() as cb:
        result = agent.invoke({"input": user_query})
        #print(f"Total Tokens: {cb.total_tokens}")
        print(result['output'])
