# Duke Innovation Co-Lab AI Project 
This project aims to explore the various ways in which the emerging field of artificial intelligence can be leveraged and applied to Duke University's Innovation Co-Lab. 
# 1 - Pathways Course Recommender 
Recommendation system being applied: 
Content Based Filtering - usage of item features to recommend other items similar to what a user likes, based on their previous actions or explicit feedback (per Google for Developers - Machine Learning)

1. Look at a student’s module history and take into account which modules they’ve actually attended.
2. From our .csv with all module names and descriptions, passes each module name through the recommendation engine and returns 10 recommended modules. How does it do this? 
3. Read our .csv data files with Pandas and store it in our data frames.
4. Clean our data frames by removing unnecessary data columns.
5. Perform text vectorization for the description of each module using the Term Frequency-Inverse Document Frequency (TF-IDF), which converts our descriptions into a numerical matrix from sklearn.feature_extraction.text.
6. We then use the sigmoid kernel function to calculate the pairwise similarity between each module description and storing it in a matrix. We then transform the similarity scores into values between 0 and 1. 
7. We now map each module title with its corresponding indice of the matrix. 
8. Given a module title as input, we use our similarity matrix to find similar modules sorted by similarity scores, excluding the input module itself, and return a list of recommended modules. 
9. Every list of recommended modules for each corresponding module the student took is then stored in a list. 
10. We create a dictionary of every recommended module along with how many times it appeared in each recommendation.

