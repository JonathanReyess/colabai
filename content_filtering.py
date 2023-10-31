import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

modules = pd.read_csv("all_modules.csv")
student = pd.read_csv("student_modules.csv")
modules_clean_df = modules.drop(columns=['Page Number'])
print(modules_clean_df.info())
#print(modules_clean_df.head)
print(modules_clean_df.head(1)['Description']) ##we will convert this description into a document matrix that will act as a vector of number.

tfv = TfidfVectorizer(min_df=3, max_features=None, 
                      strip_accents='unicode', analyzer='word', token_pattern=r'\w{1}', ngram_range=(1,3), stop_words= 'english')
