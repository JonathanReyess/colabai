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

## Deprecated: Azure SQL Server Bot

Based on the test run results above, it's logical to explore the creation of a conversational chatbot leveraging a large-language model's SQL querying capabilities.

### Streamlit 

Streamlit is a powerful, free, and open-source Python framework designed for rapid development and sharing of machine learning and data science web applications.

From this point forward, we'll utilize Streamlit to design the user interface of our chatbot and deploy it to the web, enabling seamless interaction with our users.

For further information about Streamlit and its capabilities, visit [Streamlit's official website](https://streamlit.io).

### Azure OpenAI Setup

Moving forward, we'll transition to using Azure's OpenAI Studio to manage our models. Follow the provided documentation to set up this resource and deploy our models:

[Microsoft Azure OpenAI Studio Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal)

Once your Azure OpenAI Studio resource is configured, populate the following environment variables and store them in a file named `secrets.toml` under our `.streamlit` folder:

```toml
[azure_openai]
OPENAI_API_KEY = "your-azure-openai-api-key-here"
AZURE_OPENAI_ENDPOINT = "your-azure-openai-endpoint-here"
OPENAI_API_VERSION = "2023-05-15"
OPENAI_API_TYPE = "azure"
```

These environment variables will facilitate secure communication with Azure's OpenAI services, ensuring seamless integration of our models into our application architecture.

### SQL Server Setup

To initiate our SQL database, we'll utilize Microsoft Azure's SQL Server. Once the server is operational, we'll require specific information from our database connection string:

```
server = "server-name.database.windows.net"  # Your Azure SQL server name
database = "database-name"  # SQL server DB name
username = "username"  # SQL server username
password = "password"  # SQL server password
```

These details will be securely stored in `secrets.toml` under our `.streamlit` folder.

In `st_sql_bot.py`, we'll establish a connection to our database using SQL Alchemy and create our database engine with the following connection string:

```python
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

Next, we'll leverage LangChain to link our SQL Database with our GPT-3.5 model:

```python
llm = AzureChatOpenAI(
    openai_api_version="2023-05-15",
    deployment_name="colab-copilot",
    model_name="gpt-35-turbo",
)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
```

This setup enables seamless interaction between our SQL Database and the GPT-3.5 model, facilitating sophisticated querying and responses based on user input.

### Few-Shot Prompting

Few-shot prompting is a technique employed to dynamically select and format examples based on input to provide context for a model. This approach is particularly useful for chat models as it allows adaptation to various conversational scenarios, ensuring that the model's responses remain relevant and accurate.

In our context, we're leveraging dynamic few-shot prompting, which further enhances this capability by enabling examples to be chosen based on semantic similarity to the input. This enhances the model's contextual understanding and improves response quality.

To start, we create a list of examples for our chatbot to reference:

```python
examples = [
    {
        "input": "Give me some art classes",
        "query": "SELECT * FROM courses WHERE description LIKE '% Art %' OR name LIKE '% Art %';"
    },
    {
        "input": "What's a course about making candles about?",
        "query": "SELECT description FROM courses WHERE name LIKE '%candle%';",
    },
]
```

These examples provide our chatbot with insights into what questions might look like and the expected responses.

Now, let's dive into the dynamic few-shot prompting process, where the magic happens. This approach dynamically selects and formats examples based on semantic similarity to the input, thereby enriching the model's understanding and enabling it to provide more contextually relevant responses.

### Vector Embeddings

Vector embeddings are numerical representations that capture the semantic meaning and relationships of various data types, such as words, sentences, and more. By transforming data into points in a multidimensional space, vector embeddings enable efficient data processing and support tasks like sentiment analysis and semantic similarity comparison.

OpenAI provides a variety of embedding models, each tailored for specific use cases ([OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)). These models convert words into numerical representations and organize them in a matrix where similar words are positioned closer to each other.

In our scenario, we aim to embed both the user's question and all examples provided to our model. Subsequently, we will utilize FAISS (Facebook AI Similarity Search), a library designed for efficient similarity search and clustering of dense vectors, to compare the embeddings.

```python
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    AzureOpenAIEmbeddings(
        azure_deployment="copilot-embedding",
        openai_api_version="2023-05-15",
    ),
    FAISS,
    k=5,
    input_keys=["input"],
)
```

By employing FAISS, we can efficiently identify the top 5 examples most similar to our question. From there, our model can execute further instructions based on the provided "system_prefix". This approach streamlines the process of finding relevant examples and enhances the user experience by offering contextually appropriate responses.

### Prompt Engineering

Prompt engineering is the art of guiding generative AI systems to produce desired outputs by crafting detailed instructions in the form of prompts. These prompts are natural language texts that articulate specific tasks for the AI to perform. In prompt engineering, meticulous attention is given to designing prompts, selecting appropriate formats, phrases, and symbols to effectively guide the AI to interact meaningfully with users. This iterative process involves creativity and experimentation, refining prompts until the desired outcomes are consistently achieved.

The significance of prompt engineering lies in providing generative AI systems with the necessary context and instructions to generate accurate and relevant responses. By systematically designing prompts, developers can ensure that AI applications produce meaningful and usable content. Prompt engineering offers several benefits, including:

- **Greater Developer Control:** Prompt engineering empowers developers to exert control over AI interactions by providing detailed instructions, leading to more predictable behavior and outcomes.
  
- **Improved User Experience:** Well-designed prompts result in coherent and relevant responses from AI systems, enhancing the overall user experience and satisfaction.
  
- **Increased Flexibility:** Reusable prompts can be adapted across different scenarios and domains, enabling developers to leverage existing prompts and streamline development processes.

[Adapted from Amazon Web Services]

Here's a snippet from our SQL Bot's prompt as an example:

```python
system_prefix = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer."""
```

This excerpt illustrates the use of prompts to guide the AI agent in understanding its role and task within the context of interacting with a SQL database.

## MongoDB Atlas Bot

Continuing with our established approach, we will persist with Streamlit for both UI development and hosting, alongside LangChain and vector embeddings.

Considering the capability to embed a list of examples and a user's question for dynamic few-shot prompting, it's logical to extend this concept further. Why not embed our entire database and perform FAISS (Facebook AI Similarity Search) with the user question? That's precisely our next step.

We intend to host our course data from `data/pathways_exports/courses.csv` as a MongoDB collection. Similar to our initial connection setup with the SQL Server database, we'll need to establish a connection with our MongoDB cluster.

To facilitate this, we'll store the necessary credentials in our `.streamlit/secrets.toml` file:

```
mdbpassword = "password"
address = "address"
uid = "user-id"
```

Once these credentials are configured, we can connect to our database using the following code snippet:

```python
uri = "mongodb+srv://" + st.secrets["uid"] + ":" + st.secrets["mdbpassword"] + st.secrets["address"] + ".mongodb.net/?retryWrites=true&w=majority"

mdbClient = MongoClient(uri, server_api=ServerApi('1'))
```

This setup ensures secure access to our MongoDB cluster, enabling seamless interaction with our course data for enhanced user experiences.

### Atlas Vector Search

Vector search is a sophisticated semantic search method that utilizes machine learning models to transform various types of data, like text, audio, or images, into high-dimensional vectors. These vectors capture the semantic meaning of the data, enabling searches based on similarities in the vector space rather than exact text matches. This technique complements traditional keyword-based search and enhances the capabilities of large language models (LLMs) by providing additional context. Vector search is particularly useful in natural language processing and recommendation systems, allowing for finding relevant results even when exact wording is unknown.

Benefits of vector search include semantic understanding, scalability for large datasets, and flexibility to search different types of data. With MongoDB, vector search is efficient as vectors are stored together with the original data, ensuring consistency and simplicity in the application architecture. MongoDB Atlas supports scalable vector search, both horizontally and vertically, providing efficiency and reliability for demanding workloads.

To set up vector search with MongoDB Atlas, follow the guide at: [MongoDB Atlas Vector Search](https://www.mongodb.com/developer/products/atlas/semantic-search-mongodb-atlas-vector-search/)

Now, let's delve into our pipeline.

```python
def pipeline(query):
    pipeline = [
        {
            "$vectorSearch": {
                "queryVector": get_text_embedding(query),
                "path": "description_embedding",
                "numCandidates": 219,
                "limit": 5,
                "index": "vector_index",
            }
        },
        {
            "$project": {
                "_id": 0,
                "name": 1,
                "descriptionname": 1,
                "score": {"$meta": "vectorSearchScore"},
            }
        }
    ]
    return pipeline
```

In this pipeline, the `query` parameter is passed into our `get_text_embedding()` function, which employs OpenAI's `text-embedding-3-small` to embed our question. We then conduct a similarity search using `description_embedding`, a field within our MongoDB collection automatically embedded through a trigger whenever new data is aggregated. We consider all 219 courses and return only the top 5 most similar ones.

Our `vector_index` employs cosine similarity and an approximate nearest neighbor (ANN) search with the Hierarchical Navigable Small Worlds (HNSW) algorithm. ANN optimizes for speed by approximating the most similar vectors in multi-dimensional space without scanning every vector, which is particularly useful for retrieving data from large vector datasets.

The `$project` field specifies what our pipeline will return after the similarity search. In this case, we only want the `name` and `description` of the courses along with their `score`.

The `score` is crucial as it allows us to filter out matches that may be high in semantic similarity but not relevant to each other. For instance, even though "Java" and "JavaScript" are semantically similar, they are distinct languages. We utilize functions like `check_confidence` and `check_most_confident` to filter out courses based on a minimum confidence threshold before passing them as context.

## Memory

In `mdb_memory_bot.py`, you'll find a version of our MongoDB Atlas integrated with memory capabilities. It leverages LangChain's `MongoDBChatMessageHistory` and `RunnableWithMessageHistory` to retrieve message history with the user and provide it as context to the prompt.

```python
    chat_message_history = MongoDBChatMessageHistory(
        session_id=session_id, # the user's session id
        connection_string=uri, # your MongoDB connection string URI
        database_name="",   # name of your MDB database storing chat messages
        collection_name="",  # name of your MDB collection containing chat logs
    )
```

The `session_id` enables us to retrieve the appropriate context from our collection and should be updated whenever a new conversation begins.

Currently, we haven't progressed with this version of the chatbot due to compatibility issues with Streamlit Cloud.

## Deployment

To run the application locally, execute `streamlit run st_atlas_bot.py` in your preferred IDE's terminal. Prior to running, ensure the existence of a `.streamlit/secrets.toml` file containing your Azure OpenAI and MongoDB URI credentials. It's crucial not to share these credentials with anyone. Instead, employ a local `.gitignore` file to safeguard sensitive information.

For hosting, we'll leverage Streamlit's free community cloud services, facilitating deployment, management, and global accessibility of our application.

Upon cloning this repository:

1. Sign in to Streamlit via Github or SSO (https://share.streamlit.io/signup)
2. Select this repository, the desired branch, and the file `st_atlas_bot.py`
3. Initiate deployment by clicking "Deploy"!

With each git push, your application will promptly update. Ensure that all required files for Streamlit are not nested within any directories.


### Moving Forward

Our focus lies on enhancing consistency and accuracy within our project through prompt engineering. To achieve this, we aim to dockerize the project and manage it independently, enabling us to implement memory and session management effectively. Our ideal trajectory involves establishing a multi-agent workflow: initially classifying user questions using a model, then directing them to a relevant language model with tailored context and prompts for optimal responses. This approach ensures that each query receives the most suitable and accurate answer, refining the user experience and bolstering the project's efficacy.






