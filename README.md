# Duke Innovation Co-Lab AI Project 
This project aims to explore the various ways in which the emerging field of artificial intelligence can be leveraged and applied to Duke University's Innovation Co-Lab. 

## Overview

The data primarily used throughout this project is sourced from Duke's Pathways database, an online platform offered by Duke University. Pathways provides free virtual and in-person co-curricular learning opportunities for the Duke community, aiming to foster skill growth through customizable education and flexible learning options.

Pathways was designed and built by the Office of Information Technology's Innovation Co-Lab Development Team and the Creative And User Experience team, with support from the Center for Computational Thinking.

## 1. Pathways Course Recommender

### Content Based Filtering

The purpose of this subproject is to develop a program that recommends modules similar to those a user has already taken, utilizing Content Based Filtering. This method recommends items based on their features, suggesting modules similar to those a student has completed, relying on their previous actions or explicit feedback.

While the technique employed here does not utilize advanced neural networks or deep learning algorithms, it leverages machine learning and natural language processing (NLP) techniques.

### Steps

1. **Data Collection**: We gather data via web scraping using Python's `Pandas` library, enabling us to create datasets from Pathways. This includes both all available modules and a sample of completed modules by students.

2. **Data Preprocessing**: Using `Pandas`, we clean the data by removing unnecessary columns and considering factors such as attendance to ensure data validity.

3. **Text Vectorization**: We perform text vectorization using the Term Frequency-Inverse Document Frequency (TF-IDF) technique. This converts module descriptions into a numerical matrix, capturing the importance of terms within documents relative to the entire corpus.

4. **Similarity Calculation**: Utilizing the sigmoid kernel function, we calculate pairwise similarity between module descriptions and store the scores in a matrix. This function transforms TF-IDF values into similarity scores between 0 and 1.

5. **Recommendation Generation**: Given a module title as input, we use the similarity matrix to find similar modules, excluding the input module itself. Recommendations are made based on the highest similarity scores.

6. **Aggregation and Sorting**: Recommendations are aggregated and stored in a list, then transformed into a dictionary to count the frequency of each module recommendation. Finally, we sort the dictionary by frequency and return the top recommendations.

## Note

This algorithm's effectiveness is contingent upon the modules a student has already completed. While it provides recommendations based on similarity scores, other factors such as student preferences and enjoyment of completed courses should also be considered.
