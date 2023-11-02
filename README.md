# Duke Innovation Co-Lab AI Project 
This project aims to explore the various ways in which the emerging field of artificial intelligence can be leveraged and applied to Duke University's Innovation Co-Lab. 
# 1 - Pathways Course Recommender 
Recommendation system being applied: 
Content Based Filtering - usage of item features to recommend other items similar to what a user likes, based on their previous actions or explicit feedback (per Google for Developers - Machine Learning)

1. Store our two datasets in .csv format, one with a list of all modules and their descriptions, another with a student’s module history.
2. Read our .csv data files with Pandas and store it in our data frames.
3. Clean our data frames by removing unnecessary data columns.
4. Perform text vectorization for the description of each module using the Term Frequency-Inverse Document Frequency (TF-IDF), which converts our descriptions into a numerical matrix from sklearn.feature_extraction.text.
5. We then use the sigmoid kernel function to calculate the pairwise similarity between each module description and storing it in a matrix. We then transform the similarity scores into values between 0 and 1. 
6. We now map each module title with its corresponding indice of the matrix. 
7. Given a module title as input, we use our similarity matrix to find similar modules sorted by similarity scores, excluding the input module itself, and return a list of 10 recommended modules. 
8. Every list of recommended modules for each corresponding module the student took is then stored in a list. 
9. We create a dictionary of every recommended module along with how many times it appeared in each recommendation.
10. We sort this dictionary of modules, frequency pairs by frequency, and return the first five modules with the highest frequency. 

