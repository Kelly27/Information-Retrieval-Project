#Author: KELLY KONG KAI LI (BI14110125)
# import PyPDF2 #pip install PyPDF2
from myfunc import *
from q4 import *
from q5 import *
import os, os.path, nltk, xlsxwriter, math
import numpy as np
from nltk import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

#main==================================
nltk.download('punkt')
nltk.download('stopwords')
np.set_printoptions(threshold=np.nan)

workbook = xlsxwriter.Workbook('tf-idf.xlsx')
freq = workbook.add_worksheet('frequency')
tf_sheet = workbook.add_worksheet('tf')
idf_sheet = workbook.add_worksheet('idf')
tf_idf_sheet = workbook.add_worksheet('tf-idf')
rank_sheet = workbook.add_worksheet('rank_result')

directory = input("Please enter the directory of your files: (enter 'IR_PDF\\') ")
print("Directory is", directory,".")
files = [name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))]

row = 0
col = 1

extracted_word = ''
documents = [] #store all the Doc object
idf_arr = []
doc_rank = []

for i in files:
    #d = Doc(i, )
    read_file = open(directory + '\\' + i, 'rb') #rb, read binary is important here
    words = word_tokenize(readFiles(read_file))
    words = rm_punctuation(words)
    d = Doc(i, words, [], [], [])
    documents.append(d)
    extracted_word = extracted_word + readFiles(read_file) #to store all words

word_list = word_tokenize(extracted_word)
word_list = rm_punctuation(word_list)
word_list = rm_duplicates(word_list) #remove duplicates
for w in word_list:
    freq.write(row, 0, w)
    tf_sheet.write(row, 0, w)
    idf_sheet.write(row, 0, w)
    tf_idf_sheet.write(row, 0, w)
    row += 1
row = 0 # reset row

#store frequency and tf
for d in documents:
    row = 0
    count_word = Counter(d.words)
    words_array = []
    tf_array = []
    for word in word_list:
        #freq
        words_array.append(count_word[word])
        #tf
        if(count_word[word] > 0): #prevent match error
            tf = 1 + math.log(count_word[word], 2)
            tf_array.append(tf)
        else:
            tf_array.append(0)

    d.freq = words_array
    d.tf = tf_array

    for x in d.freq:
        freq.write(row, col, x)
        row += 1
    row = 0 #reset

    for x in d.tf:
        tf_sheet.write(row, col, x)
        row += 1

    col += 1


row = 0 #reset
col = 1 #reset

#idf calculation
for word in word_list:
    doc_number = 0
    for d in documents:
        if(word in d.words):
           doc_number = doc_number + 1
    if(doc_number > 0):
        idf = math.log(len(documents) / doc_number, 2)
        idf_sheet.write(row, 1, idf)
        idf_arr.append(idf)
    else:
        idf_arr.append(0)
        idf_sheet.write(row, 1, 0)
    row += 1

row = 0 #reset

#td-idf calculation
for d in documents:
    row = 0
    tf_idf_arr = []
    for i, tf_item in enumerate(d.tf):
            tf_idf = tf_item * idf_arr[i]
            tf_idf_arr.append(tf_idf)
    d.tf_idf = tf_idf_arr
    for x in d.tf_idf:
        tf_idf_sheet.write(row, col, x)
        row += 1
    col += 1
#print(repr(d))

#query ranking
query = word_tokenize(input('What is your query? (Please enter in lower case) - '))
query = rm_punctuation(query)
for d in documents:
    query_match = []
    all_query_weights = []
    matching_query_weights = []
    query_vector = 0.0
    doc_weights = []
    query_not_found = []
    doc_vector = 0.0
    q_sum = 0.0
    d_sum = 0.0
    numerator = 0.0

    q_counter = Counter(query)

    for q in query:
        if(q in word_list):
            qw = (1 + math.log(q_counter[q], 2)) * idf_arr[word_list.index(q)]
            all_query_weights.append(qw)

            if(q in d.words):
                query_match.append(q)
                matching_query_weights.append(qw)
        else:
            query_not_found.append(q)

    for q in query_match:
        dw = d.tf_idf[word_list.index(q)]
        doc_weights.append(dw)


    for x in all_query_weights:
        q_sum += math.pow(x, 2)
    query_vector = math.sqrt(q_sum) #found query's vector norms

    for x in d.tf_idf:
        d_sum += math.pow(x, 2)
    doc_vector = math.sqrt(d_sum) #found document's vector norms


    np_doc_weights = np.array(doc_weights)
    np_matching_query_weights = np.array(matching_query_weights)

    for i in range(0, len(doc_weights)):
        numerator += (doc_weights[i] * matching_query_weights[i])
    r = numerator / (query_vector * doc_vector)
    doc_rank.append([d.doc_name, r])
sorted_ranking = sorted(doc_rank, key=lambda x:x[1], reverse=True)
rank_sheet.write(0, 0, 'Document Name')
rank_sheet.write(0, 1, 'Rank')
row = 1
print('>>> Hence, ranking of the documents with the query of ', query, ' is as follow:')
for i in sorted_ranking:
    print('>>> Document name: ', i[0], ', Rank: ', i[1])
for i in range(0, (len(sorted_ranking) - 1)):
    rank_sheet.write(row, 0, sorted_ranking[i][0])
    rank_sheet.write(row, 1, sorted_ranking[i][1])
    row += 1
print('>>> Query that cannot be found: ', query_not_found)
rank_sheet.write(row+1, 0, "Query: ")
col = 1
for q in query:
    rank_sheet.write(row+1, col, q)
    col += 1
rank_sheet.write(row+2, 0, "Query cannot be found: ")
col = 1
for q in query_not_found:
    rank_sheet.write(row+2, col, q)

workbook.close()
print('>>> !!! You may see the result from the generated Excel file.')
print('>>> END OF QUESTION 1,2, AND 3.')

for i in range(1, 5):
    print('...')

#question 4 =======================================================
question4(documents)

#question 5 =======================================================
question5(documents, sorted_ranking, query)

#end of code ======================================================
input("Press enter to exit ;)")

