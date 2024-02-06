# Duke Innovation Co-Lab AI Project 
This project aims to explore the various ways in which the emerging field of artificial intelligence can be leveraged and applied to Duke University's Innovation Co-Lab. 


## Data 

The data primarily used throughout this project will be from Duke's Pathways database. 

Duke Pathways is an online platform offered by Duke University that provides free virtual and in-person co-curricular learning opportunities for the Duke community. It aims to help individuals grow their skills through customizable education and flexible learning options.

Duke Pathways was designed and built by the Office of Information Technology's Innovation Co-Lab Development Team and the Creative And User Experience team, with support from the Center for Computational Thinking. 


## 1 - Pathways Course Recommender 

**Content Based Filtering** - usage of item features to recommend other items similar to what a user likes, based on their previous actions or explicit feedback (per Google for Developers - Machine Learning)

The purpose of this subproject is to develop a program that when given a 'Student' along with a list of completed 'Modules', returns a list of modules that they are likely to have interest in. 

Although this task does not involve advanced neural networks or deep learning algorithms, it leverages machine learning and natural language processing (NLP) techniques. 

### Steps

1. One way to obtain our data is through a webscraper as demonstrated in course_recommender/pathways_scraper.py and data/scraped_data. This is an option when all the data we need can be easily accessible directly from a webpage. Webscraping enables us to gatherg data and build the datasets we need, in this case data/scraped_data/all_modules.csv and data/scraped_data/student_sample_modules.csv. 


2. We will be utilizing Python's Pandas library to process our .csv data files and create our data frames. It's important to clean our data by removing unecessary columns and take into consideration certain conditions such as whether or not a student attended the module they enrolled for our not to ensure validity and prepare our data for our algorithms. 

4. Perform text vectorization for the description of each module using the Term Frequency-Inverse Document Frequency (TF-IDF) technique. TF-IDF is a classic technique used in natural language processing tasks that:

1. Measures the frequency of a term within a document, calculated as the number of times a term appears in a document divided by the total number of terms in that document (TF). 

TF(t, d) = (Number of times term t appears in document d) / (Total number of terms in document d)

2. Measures how unique or rare a term is across all documents in the corpus, calculated as the logarithm of the total number of documents in the corpus divided by the number of documents containing the term, with the result being scaled to prevent the domination of terms that occur in many documents. (IDF)

IDF(t) = log_e(Total number of documents / Number of documents containing term t)

3. Combining our TF and IDF values to indicate the importance of a term within a document relative to the entire corpus.

TF-IDF(t, d) = TF(t, d) * IDF(t)

5. As a result, we use the scikit-learn Python library to convert our descriptions for each module into a numerical matrix. 

   We can modify the following parameters when creating our TF-IDF matrix to control how TF-IDF values are calculated:

   ```
      tfv = TfidfVectorizer(
          min_df=3,           # Ignore terms that appear in fewer than 3 descriptions
          max_features=None,  # Keep all unique terms
          strip_accents='unicode',
          analyzer='word',    # Treat words as the analytical unit
          token_pattern=r'\w{1,}',  # Consider words with at least 1 character
          ngram_range=(1, 3),      # Consider unigrams, bigrams, and trigrams
          stop_words='english'     # Remove common English stop words
      )
   ```

   This produces a ***174 x 1017*** TF-IDF Matrix with numerical values for each word in each module's description, where rows correspond to each module and columns to unique words.

6. We will now utilize the sigmoid kernel function to calculate the pairwise similarity between each module description and store it in another matrix. The similartiy scores returned will be a value between 0 and 1.    

   The sigmoid_kernel function takes the TF-IDF matrix as input and applies a sigmoid transformation to it with the following formula:

   ***S(x, y) = 1 / (1 + e^(-x * y))***

   Where S(x, y) represents the similarity between two modules (x and y) and e is the base of the natural logarithm.

   We then output a similarity matrix where each entry (i, j) represents the similarity score between module descriptions i and j.

6. Now that we have our similarity matrix, we will now map each module 'title' with its corresponding indice of the matrix. 

7. Now passing a module title as input to our function, we use the similarity matrix we created from all available modules to find similar modules, excluding the input module itself, and return a list modules with the highest similarity scores. For this step, we are taking every module the student has completed and returning recommendations for that singular module specifically.

8. We will store our lists of recommendations in a separate list that we will use to create a dictionary by iterating through each list. The key in this dictionary will be a module name, with the value being how many times it appears in our 2D array.  


10. Finally sort this dictionary of {module, frequency} pairs by frequency, and return the first n modules with the highest frequency. These will be the n courses our algorithm has recommended. 


Now this algorithm isn't perfect, other factors to consider might include whether or not the student actually enjoyed the class they completed. As it may be assumed, our algorithm is highly dependent on the modules the student has already completed. The more modules a student has taken, the better the recommendation results. 


## 2 - OpenAI Tools 

**OpenAI API being used :** Assistants - https://platform.openai.com/docs/assistants/how-it-works 

- Call models such as GPT-4 with specific instructions to tune their personality and capabilities.
- Access multiple built-in tools in parallel, such as Code interpreter and Knowledge retrieval — or tools you build / host (via Function calling).
- Assistants can access persistent Threads. 
   - Threads simplify AI application development by storing message history and truncating it when the conversation gets too long for the model’s context length. You create a       Thread once, and simply append messages to it as your users reply.
- Create files (e.g., images, spreadsheets, etc) and cite files they reference in the messages they create.

- Example: Provided the following webpage from Duke OIT - https://oit.duke.edu/service/eprint/) - we can now ask questions about content on the page.
```
- Hey, I'm your Co-Lab Co-Pilot! Ask me some questions!


How can I help you?How much printing money do I get a semester?

Task completed successfully

I'll check the information for you. 

Do you have any other questions? (yes/no) yes

How can I help you?Do you have an answer?
> 
Task completed successfully

Yes, Duke students receive an allocation of $32 per semester in black-and-white laser printing at designated ePrint stations, and undergraduate students have the option to request an increase in their printing allocation once per semester【7†source】. 

Do you have any other questions? (yes/no) no
Alrighty then, I hope you learned something!
```



