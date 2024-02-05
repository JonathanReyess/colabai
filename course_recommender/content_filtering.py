import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
import operator

modules = pd.read_csv("data/scraped_data/all_modules.csv")
student = pd.read_csv("data/scraped_data/student_sample_modules.csv")
modules_clean_df = modules.drop(columns=['Page Number'])
#print(modules_clean_df.info())
#print(modules_clean_df.head)
#print(modules_clean_df.head(1)['Description']) ##we will convert this description into a document matrix that will act as a vector of number.

tfv = TfidfVectorizer(min_df=3, max_features=None, 
                      strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}', ngram_range=(1,3), stop_words= 'english')
modules_clean_df['Description'] = modules_clean_df['Description'].fillna('')
tfv_matrix = tfv.fit_transform(modules_clean_df['Description'])
#print(modules_clean_df['Description'])
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
    sig_scores = sig_scores[1:11]
    module_indices = [i[0] for i in sig_scores]
    recommendation = modules_clean_df['Title'].iloc[module_indices]
    final = []
    for i in range(0,3):
        temp = recommendation.index[i]
        final.append(recommendation[temp])
    return final

#print(rec('Backing up and Sharing Code: Git'))

#now that we have our recommendation function, we need to get a list of descriptions from the courses the student has taken, and pass it into
#the recommendation engine as a temporary module. 

student_clean_df = student.drop(columns=['Type', 'Hours', 'Date']) #in the future we may want to incorportate recency bias
student_indices = pd.Series(student_clean_df.index, index=student_clean_df['Module Name'].str.strip()).drop_duplicates()
word = "attend"
module_list = []
recs_list = []
for i, row in student_clean_df.iterrows():
    if word in row['Status']:
        module_list.append(row['Module Name'])
for module in module_list:
    recs = rec(module)
    for item in recs:
        if item not in module_list:
            recs_list.append(item)


recset = set(recs_list)
reclist = []
for item in recset:
    reclist.append(item)

final_recs = []
frequency = []
for recs in recset:
    count = 0
    for mod in recs_list: 
        if mod == recs:
            count +=1
    frequency.append(count)

freq_dict = {reclist[i]: frequency[i] for i in range(len(reclist))}

sorted_dict = dict(sorted(freq_dict.items(), key=operator.itemgetter(1), reverse=True))
modules = list(sorted_dict.keys())
courses = [course for course in modules[:5]]
recommendations = "Your recommendations are: \n" + "\n".join(courses)
print(recommendations)



##sort list by frequency of title and then return the top 3


#print(module_list)
#description_list = []
#for word in module_list:
    #for i, row in modules_clean_df.iterrows():
        #if word in row['Title']:
            #description_list.append(row['Description'])
#print(description_list)

#p_description = " ".join(description_list)
#print(p_description)

##now what if we take this description and pass it through an LLM to summarize it?