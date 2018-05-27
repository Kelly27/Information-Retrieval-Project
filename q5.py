#question 4 ==========================================================================
from myfunc import *
from nltk import word_tokenize
import matplotlib.pyplot as plt

def question5(documents, ranking, query):

    print('>>>QUESTION 5')
    recall_list = []
    precision_list = []
    recall_precision_list = [[], []]

    print('Your query was: (based on query entered for Question 1 to Question 3) ' + str(query ))
    for enum, rank in enumerate(ranking):
        print(enum + 1, rank[0])

    rel_doc = input('Select the relevant documents based on the index above - (eg. 1 5 10):')
    rel_doc = [int(s) for s in rel_doc.split() if s.isdigit()]

    rel_doc.sort();

    for r in rel_doc:
        recall = (rel_doc.index(r) + 1)/len(rel_doc) * 100
        recall_precision_list[0].append(rounddown(recall))
        precision = rel_doc.index(r) + 1 / r * 100
        recall_precision_list[1].append(precision)

    recall_list = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    j = 0;
    for i in recall_list:
        precision_list.append(recall_precision_list[1][j])
        if i == recall_precision_list[0][j]:
            j += 1

    print('Recall       |  Precision')
    for index in range(0, len(recall_list)):
        print(recall_list[index], '                 ', precision_list[index])

    plt.plot(recall_list, precision_list, 'ro', recall_list, precision_list)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.show()
