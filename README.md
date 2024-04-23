# Duke Innovation Co-Lab AI Project 
This project aims to explore the various ways in which the emerging field of artificial intelligence can be leveraged and applied to Duke University's Innovation Co-Lab. 

## Overview

The data primarily used throughout this project is sourced from Duke's Pathways database, an online platform offered by Duke University. Pathways provides free virtual and in-person co-curricular learning opportunities for the Duke community, aiming to foster skill growth through customizable education and flexible learning options.

Pathways was designed and built by the Office of Information Technology's Innovation Co-Lab Development Team and the Creative And User Experience team, with support from the Center for Computational Thinking.

## Environment

Let's first setup a virtual environment with miniconda. https://docs.anaconda.com/free/miniconda/index.html

conda create -n <env_name> python=<python_version>

conda create -n colab python=3.11.7

conda activate <env_name>



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

### MongoDB Atlas and Compass 

### Vector Embeddings

### Streamlit 

### Azure SQL Server Bot (DEPRECATED)
## How it was more tedious because of pymssql==2.2.7 and hard to integrate with LC, ODBC drivers (pyodbc==5.0.1).

### Azure OpenAI

### Moving Forward 


Update the requirements.txt file. and talk about the technology used. 




