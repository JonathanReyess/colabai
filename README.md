# Duke Innovation Co-Lab AI Project 
This project aims to explore the various ways in which the emerging field of artificial intelligence can be leveraged and applied to Duke University's Innovation Co-Lab. 

## Overview

The data primarily used throughout this project is sourced from Duke's Pathways database, an online platform offered by Duke University. Pathways provides free virtual and in-person co-curricular learning opportunities for the Duke community, aiming to foster skill growth through customizable education and flexible learning options.

Pathways was designed and built by the Office of Information Technology's Innovation Co-Lab Development Team and the Creative And User Experience team, with support from the Center for Computational Thinking.

## Environment

Let's first setup a virtual environment with miniconda. https://docs.anaconda.com/free/miniconda/index.html

```
conda create -n <env_name> python=<python_version>
```
```
conda create -n colab python=3.11.7
```
```
conda activate <env_name>
```


All required libraries and packages can be found in `requirements.txt`. To install these libraries, simply run:

```bash
pip install -r requirements.txt
```
Make sure to set your OpenAI API Key in the `.env` file as:

```
OPENAI_API_KEY = "your_api_key_here"
```

## 1. Pathways Course Recommender

### Content Based Filtering

The purpose of this subproject is to develop a program that recommends modules similar to those a user has already taken, utilizing Content Based Filtering. This method recommends items based on their features, suggesting modules similar to those a student has completed, relying on their previous actions or explicit feedback.

While this subproject does not utilize advanced neural networks or deep learning algorithms, it leverages machine learning and natural language processing (NLP) techniques.

### Steps

1. **Data Collection**: We gather data via web scraping using Python's `Pandas` library, enabling us to create datasets from Pathways. This includes both all available modules and a sample of completed modules by students.

2. **Data Preprocessing**: Using `Pandas`, we clean the data by removing unnecessary columns and considering factors such as attendance to ensure data validity.

3. **Text Vectorization**: We perform text vectorization using the Term Frequency-Inverse Document Frequency (TF-IDF) technique. This converts module descriptions into a numerical matrix, capturing the importance of terms within documents relative to the entire corpus.

4. **Similarity Calculation**: Utilizing the sigmoid kernel function, we calculate pairwise similarity between module descriptions and store the scores in a matrix. This function transforms TF-IDF values into similarity scores between 0 and 1.

5. **Recommendation Generation**: Given a module title as input, we use the similarity matrix to find similar modules, excluding the input module itself. Recommendations are made based on the highest similarity scores.

6. **Aggregation and Sorting**: Recommendations are aggregated and stored in a list, then transformed into a dictionary to count the frequency of each module recommendation. Finally, we sort the dictionary by frequency and return the top recommendations.

### Note:

This algorithm's effectiveness is contingent upon the modules a student has already completed. While it provides recommendations based on similarity scores, other factors such as student preferences and enjoyment of completed courses should also be considered.


## 2. OpenAI Assistants

In Fall 2023, OpenAI unveiled their new API that enabled developers to create conversational agents with features such as "Threads" to help manage longer conversations and "Retrieval" to help store text, along with improvements to the function-calling functionality.

In this subproject, we will be creating our very own assistant integrated with our Pathways API.

Per OpenAI, a typical integration of the Assistants API has the following flow:

- Create an Assistant in the API by defining its custom instructions and picking a model. If helpful, enable tools like Code Interpreter, Retrieval, and Function calling.

    - In our use case, we will be utilizing the Function Calling tool. Per OpenAI, the basic sequence of steps for function calling are as follows:

        - Call the model with the user query and a set of functions defined in the functions parameter.
        - The model can choose to call one or more functions; if so, the content will be a stringified JSON object adhering to your custom schema (note: the model may hallucinate parameters).
        - Parse the string into JSON in your code, and call your function with the provided arguments if they exist.
        - Call the model again by appending the function response as a new message, and let the model summarize the results back to the user.

- Create a Thread when a user starts a conversation.
- Add Messages to the Thread as the user ask questions.
- Run the Assistant on the Thread to trigger responses. This automatically calls the relevant tools.

We will be defining a function called `get_course_description()` which takes in the name of the course and returns its description through an HTTP request.

With assistants, our model will know when to call this function and how to parse our natural language to extract the name of the course we're asking about. It will then take the return value from our function, and respond to the initial question in an appropriate manner.

## Example Usage

**Q:** 
```
"What is Intro to Python about?" 
```
**Background Operations:** 

```
run status in_progress...
run status requires_action
run.required_action
RequiredAction(submit_tool_outputs=RequiredActionSubmitToolOutputs(tool_calls=[RequiredActionFunctionToolCall(id='call_36xP1bjO3RahDjDbIaAO8rTw', function=Function(arguments='{"name":"Intro to Python"}', name='get_course_description'), type='function')]), type='submit_tool_outputs')
function_name: get_course_description and arguments: {"name":"Intro to Python"}
run status in_progress...
run status completed
```

**A:** 
```
"Intro to Python" is a class designed for individuals with little to no programming experience. It focuses on teaching introductory programming concepts such as variables, input, output, strings, and loops. The course is suitable for those looking to learn the basics of programming.
```

In this snippet, we can see that our model is able to determine when a function call is required from the query and delivers an adequate answer.

## 3. LangChain 

LangChain is a framework for developing applications powered by language models. Chains refer to sequences of calls - whether to an LLM, a tool, or a data preprocessing step.

It enables the development of applications that are context-aware and able to reason about how to answer based on the given context. 

In this subproject, our goal will be to query a sample SQL database table made by converting our .csv file into a .db sqlite file with one table called "courses". 

The overarching process will be as follows: 

1. Convert question to SQL query: Model converts user input to a SQL query.
2. Execute SQL query: Execute the SQL query.
3. Answer the question: Model responds to user input using the query results.

A sample querying script can be found in `langchain/sqlchain_query.py`. 

### Agents 

"The core idea of agents is to use a language model to choose a sequence of actions to take. In chains, a sequence of actions is hardcoded (in code). In agents, a language model is used as a reasoning engine to determine which actions to take and in which order."

We would ideally want to use agents to build a more complex querying system that would handle data discrepencies, all while maximizing runtime and cost efficiency. 

In `langchain/agents/sql_agent.py` we can see an example of a Langchain SQL agent that utilizes dynamic few-shot prompting. 

Dynamic few-shot prompting allows us to optimize agent performance by inserting relevant queries in the prompt that the model can use as reference. 

We take in user input and select some number of examples from our curated list to add to our few-shot prompt by performing a semantic search using OpenAI's embeddings and vector store we configure to find the examples most similar to our input.

We can further customize agents through the `system_prefix` which are the set of instructions for our agent that determine its behavior.

### Example Usage 

**Q:** What are some classes about painting? 

```
> Entering new AgentExecutor chain...
```

```
Invoking: `sql_db_query` with `SELECT * FROM courses WHERE description LIKE '% painting %' OR name LIKE '% painting %' LIMIT 10`
```

```
Yes, there are painting classes available. Here are some examples:

1. Course: Co-Lab Cosplay Co-op: The Series
   Description: Are you a maker at heart? Have you always wanted to make an awesome prop or costume piece and just...
   [More Info](https://www.kamuicosplay.com/)
   Skills Taught: Familiarize yourself with varied fabrication methods, Plan a project from research stages to final product, Clothing Patterns, Sculpting Tools

2. Course: Co-Lab Cosplay Co-op: Painting and Weathering
   Description: If you're signed up for the Co-Lab Cosplay Co-op: The Series, you're automatically part of this one!
   [More Info](https://www.kamuicosplay.com/)
   Skills Taught: Learn basic hand-painting skills, Learn how to make details stand out with advanced painting skills
   Materials provided: Brown/Red/Black Oil paints, Spray primers

3. Course: Painting with Hweyon Grigoni
   Description: A landscape painting can draw you into a space in a special way. In this 2-hour workshop, we will look at various types of landscapes, and then create our own acrylic painting to take home. We'll paint together with some loose guidelines- you will choose your own...

4. Course: Day of the Dead Series: Exploratory Día de Los Muertos Acrylic Painting Workshop
   Description: This workshop will explore what Día de Los Muertos means to us! By the end of the workshop, you will create an acrylic painting. No painting experience is required.
   Instructor: Antonio Alanís

5. Course: Portrait Painting
   Description: Portrait painting has probably been around as long as people have been around. In this workshop we'll continue the tradition and create our own (self, other, abstract, etc.) portrait of choice. Beginners welcome. We'll cover the basics of portrait painting and attend to...

Please let me know if you need more information.

```

```
> Finished chain.
```

## Azure SQL Server Bot (DEPRECATED)

Given the results of the test run above, it would only be rational to then try and create a conversational chatbot using a large-language model's SQL querying capabilities


### Streamlit 

Streamlit is a free and open-source Python-based framework to rapidly build and share machine learning and data science web apps. 

From here on outward, we will be using Streamlit to design our chatbot's user interface and deploy it to the web.

For more information on Streamlit, visit https://streamlit.io 

### SQL Server 

We will first need to set up our SQL database. For our use case, let's use Microsoft Azure's SQL Server. 

Once our server is up and running, we will need the following information from our database connection string: 

```
server = "server-name.database.windows.net" # Your az SQL server name
database = "database-name" # SQL server DB name 
username = "username" # SQL server username 
password = "password" # SQL server password
```

We will store this information in a file called `secrets.toml`under our `.streamlit` folder. Inside this folder, you should also include 
information such as your Azure OpenAI credentials. 


In st_sql_bot.py, we will then connect to our database through SQL Alchemy and create our database enine with the following connection string: 

```
odbc_str = (
'mssql+pyodbc:///?odbc_connect='
'Driver={ODBC Driver 17 for SQL Server}' +
';Server=tcp:' + st.secrets["server"] + ';PORT=1433' +
';DATABASE=' + st.secrets["database"] +
';Uid=' + st.secrets["username"] +
';Pwd=' + st.secrets["password"] +
';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
)
```

We will then use LangChain to connect our SQL Database to our GPT-3.5 model:

```
llm = AzureChatOpenAI(
    openai_api_version="2023-05-15",
    deployment_name="colab-copilot",
    model_name="gpt-35-turbo",
)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
```

### Few-Shot Prompting 

Few-shot prompting is a technique that involves dynamically selecting and formatting examples based on input to provide context for a model. It's useful for chat models as it allows for adaptation to various conversational scenarios. We can tailor examples to suit our specific Q&A needs, ensuring the model's responses are relevant and accurate. 

In our case, we will be using dynamic few-shot prompting, which further enhances this capability by allowing examples to be chosen based on semantic similarity to the input, improving the model's contextual understanding and response quality.

We will first create a list of examples for our chatbot to reference: 

```
examples = [

    {
        "input": "Give me some art classes", 
        "query": "SELECT * FROM courses WHERE description LIKE '% Art %' OR name LIKE '% Art %';"
     },

    {
        "input": "What's a course about making candles about?",
        "query": "SELECT description FROM courses WHERE name LIKE '%candle%';",
    },
```

This will give our chatbot an idea of what a question might look like, and what we expect it to do. 

Now here's where the magic happens. 

### Vector Embeddings

Vector embeddings are numerical representations that capture the meaning and relationships of various data types, such as words, sentences, and more. They transform data into points in a multidimensional space, where similar points cluster together. These representations facilitate efficient data processing and enable tasks like sentiment analysis. 

OpenAI offers several embedding models (https://platform.openai.com/docs/guides/embeddings). In essence, such model will enable us to turn our words into numbers and map these numbers into a matrix where similar words are closer to eachother. 

We will specifically embed the user's question along with all examples we have provided our model. Then, we will perform FAISS
(Facebook AI Similarity Search - a library for efficient similarity search and clustering of dense vectors ) between the two.  

```
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    AzureOpenAIEmbeddings(azure_deployment="copilot-embedding",
    openai_api_version="2023-05-15",),
    FAISS,
    k=5,
    input_keys=["input"],
)
```

We will then return the top 5 examples that are most similar to our question, and our model will do the rest depending on our instructions in "system_prefix".  

### Prompt Engineering 

Prompt engineering involves guiding generative AI to produce desired outputs by crafting detailed instructions in the form of prompts. These prompts are natural language texts that specify tasks for the AI to perform. In prompt engineering, we carefully design prompts, selecting appropriate formats, phrases, and symbols to guide the AI to interact meaningfully with users. This process involves creativity and experimentation to refine prompts until desired outcomes are achieved.

Prompt engineering is crucial because generative AI, while powerful, requires context and detailed instructions to generate accurate and relevant responses. By systematically designing prompts, we ensure that AI applications produce meaningful and usable content. Prompt engineering also provides greater developer control over AI interactions, improves user experience by delivering coherent and relevant responses, and increases flexibility by enabling reuse of prompts across different scenarios and domains.

[Per Amazon Web Services]

Here's a chunk from our SQL Bot's prompt as an example:

```
system_prefix = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.'''
```

## MongoDB Atlas Bot 

In line with what we've done so far, we will continue to use Streamlit for UI and hosting purposes along with LangChain and vector embeddings.

If we can embed a list of examples and a user's question to peform dynamic few-shot prompting, it would only be rational to then ask "Why not embed our whole databse and perform FAISS with the user question?" And that's exactly what we are going to do. 

We will host our course data from `data/pathways_exports/courses.csv` as a MongoDB collection. Similar to how we had to initially connect to our SQL Server database, we will first need to establish a connection with our MongoDB cluster.

We will store the following in our `.streamlit/secrets.toml` file. 

```
mdbpassword = "password"
address = "address"
uid = "user-id"
```

Once these are set, we can connect to our database. 

```
uri = "mongodb+srv://" + st.secrets["uid"] + ":" + st.secrets["mdbpassword"] + st.secrets["address"] + ".mongodb.net/?retryWrites=true&w=majority"

mdbClient = MongoClient(uri, server_api=ServerApi('1'))
```

### Atlas Vector Search

Vector search is a semantic search capability that utilizes machine learning models to transform various types of data, such as text, audio, or images, into high-dimensional vectors. These vectors capture the semantic meaning of the data, enabling searches based on similarities in the vector space rather than exact text matches. This technique complements traditional keyword-based search and enhances the capabilities of large language models (LLMs) by providing additional context. Vector search allows for finding relevant results even when exact wording is unknown, making it useful in natural language processing and recommendation systems.

Benefits of vector search include semantic understanding, scalability for large datasets, and flexibility to search different types of data. With MongoDB, vector search is efficient as vectors are stored together with the original data, ensuring consistency and simplicity in the application architecture. MongoDB Atlas supports scalable vector search, both horizontally and vertically, providing efficiency and reliability for demanding workloads.

For information on how to set this up, follow: https://www.mongodb.com/developer/products/atlas/semantic-search-mongodb-atlas-vector-search/

Now let's examine lines 187 to 208 of our code. 

```
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
                "descriptionname": 1,
                'score': {
                    '$meta': 'vectorSearchScore'
      }
            
            }
        }
            ]
    return pipeline
```

Here we see the question parameter `query` being passed into our `get_text_embedding()` function which uses OpenAI's `text-embedding-3-small` to embed our question. We then perform similar search with `description_embedding`, a field within our MongoDB collection that is automatically through a trigger that embeds our description of courses whenever new data is aggregated. We consider all 219 courses and only return the top 5 most similar. Our `vector_index` uses cosine similarity and approximate nearest neighbor (ANN) search with the Hierarchical Navigable Small Worlds (HNSW) algorithm. ANN optimizes for speed by approximating the most similar vectors in multi-dimensional space without scanning every vector. This approach is particularly useful for retrieving data from large vector datasets.
THe `$project` field indicates what our pipeline will return after the similarity search is done with `0` denoting `no return` and `1` denoting `return`. In this case, we only want the `name` and `description` of the courses along with their `score`. 

Score is useful in our case as it captures and allows us to filter any matches that may be high in semenatic similarity, but not relevant to eachother. For example `Java` and `JavaScript` are two completely different coding languages, however, as we see here:

```
Query: I want to learn Java.

``` 

```
Reponse: {'name': 'Intro to JavaScript', 'descriptionname': '<p>What is Javascript? Is it related to Java? What is vanillaJS? Is it hard to learn? I know you have many questions, and this workshop is here to help you bust these myths. Javascript is a front-end development language. It can help you build a website and make it ....[redacted for clarity], 'score': 0.6352804899215698}]
```

As we can see, JavaScript classes are still returned due to the semantic similarity in `Java`, however, the confidence score is relatively low at `0.635`. This is where our functions `check_confidence` and `check_most_confident` come into play, allowing us to only pass as context the courses that meet a minimum confidence threshold. 

## Memory 

### Azure OpenAI

### Moving Forward 






