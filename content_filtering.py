import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel

modules = pd.read_csv("data/all_modules.csv")
student = pd.read_csv("data/student_modules.csv")
modules_clean_df = modules.drop(columns=['Page Number'])
#print(modules_clean_df.info())
#print(modules_clean_df.head)
#print(modules_clean_df.head(1)['Description']) ##we will convert this description into a document matrix that will act as a vector of number.

tfv = TfidfVectorizer(min_df=3, max_features=None, 
                      strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}', ngram_range=(1,3), stop_words= 'english')
modules_clean_df['Description'] = modules_clean_df['Description'].fillna('')
tfv_matrix = tfv.fit_transform(modules_clean_df['Description'])
#print(tfv_matrix.shape) #combination of 1017 words for our columns, this comes from the token_pattern = r\w{1,}
sig = sigmoid_kernel(tfv_matrix, tfv_matrix) #the sigmoid library is responsible for transforming our input between 0-1, formula: 1 / 1 + e^-1
#how is the sentence in descriptio #1 related to description #2? 
#print(sig[0])

#reverse mapping of indices and module names

indices = pd.Series(modules_clean_df.index, index=modules_clean_df['Title'].str.strip()).drop_duplicates()
#print(indices['Github Pages'])

#function to recommend a module based on the title you enter 

def rec(title, sig=sig):
    #index of original title then the sig of that title
    index = indices[title]
    sig_scores = list(enumerate(sig[index]))
    sig_scores = sorted(sig_scores, key=lambda x:x[1], reverse =True )
    sig_scores = sig_scores[1:6]
    module_indices = [i[0] for i in sig_scores]
    return modules_clean_df['Title'].iloc[module_indices]


print(rec('Wordle with Python'))