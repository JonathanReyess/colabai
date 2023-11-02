# Duke Innovation Co-Lab AI Project 
This project aims to explore the various ways in which the emerging field of artificial intelligence can be leveraged and applied to Duke University's Innovation Co-Lab. 
## 1 - Pathways Course Recommender 
**Recommendation system being applied:** 

Content Based Filtering - usage of item features to recommend other items similar to what a user likes, based on their previous actions or explicit feedback (per Google for Developers - Machine Learning)

### Steps

1. Store our two datasets in .csv format, one with a list of all modules and their descriptions, another with a student’s module history.
2. Read our .csv data files with Pandas and store it in our data frames.
3. Clean our data frames by removing unnecessary data columns and take into account whether the student attended the class. 

4. Perform text vectorization for the description of each module using the Term Frequency-Inverse Document Frequency (TF-IDF), which converts our descriptions into a numerical matrix from sklearn.feature_extraction.text.

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

   We will then produce a 174 x 1017 TF-IDF Matrix with numerical values for each word in each module's description, where the rows correspond to     modules and columns to unique words.

5. We then use the sigmoid kernel function from sklearn.metrics.pairwise to calculate the pairwise similarity between each module description and storing it in a matrix. We then transform the similarity scores into values between 0 and 1. 

The sigmoid_kernel function takes the TF-IDF matrix as input and applies a sigmoid transformation to it with the following formula:
S(x, y) = 1 / (1 + e^(-x * y))

Where S(x, y) represents the similarity between two modules (x and y) and e is the base of the natural logarithm (approximately 2.71828).

We then output a similarity matrix where each entry (i, j) represents the similarity score between module descriptions i and j.

6. We now map each module title with its corresponding indice of the matrix. 
7. Given a module title as input, we use our similarity matrix to find similar modules sorted by similarity scores, excluding the input module itself, and return a list of 10 recommended modules. 
8. Every list of recommended modules for each corresponding module the student took is then stored in a list. 
9. We create a dictionary of every recommended module along with how many times it appeared in each recommendation.
10. We sort this dictionary of modules, frequency pairs by frequency, and return the first five modules with the highest frequency. 
