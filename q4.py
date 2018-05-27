#question 4 ==========================================================================
import itertools
from myfunc import *
from nltk import word_tokenize

def question4(documents):

    print('>>>QUESTION 4')
    termset_list = []

    query4 = word_tokenize(input('>>> Give a query of three words: '))
    while not len(query4) == 3:
        query4 = word_tokenize(input('>>> !Error! Please enter a query of three words. \n Give a query of three words: '))
    query4 = rm_punctuation(query4)
    print('Your entered query is ' , query4)
    threshold = input('>>> Give a threshold on the frequency termsets (number): ')
    while not threshold.isdigit():
        threshold = input('>>> !Error! Please enter a digit. \n Give a threshold on the frequency termsets (number): ')

    print('Your entered threshold is ', threshold, ' \n >>>TIME TO COMPUTE ALL FREQUENT TERMSETS FOR THE GIVEN QUERY!')

    for n in range(1,len(query4)+1):
        for comb in itertools.combinations(query4, n):
            ts = Termset(comb,[], n)
            print('\n', comb)
            for d in documents:
                # for c in comb:
                    freq = [d.words.count(c) for c in comb]
                    print(d.doc_name, freq)
                    isTermset = check_greater(freq, int(threshold))
                    if isTermset:
                        ts.freq_termset.append(d.doc_name)
            termset_list.append(ts)

    for t in termset_list:
        if len(t.freq_termset) > 0:
            print('>>> !!! FREQUENT-'+str(t.small_n)+'-TERMSET >> ', 'TERMSET:', t.termset, ', FREQUENT TERMSET:', t.freq_termset)
        else:
            print('>>> !!! THERE ARE NO FREQUENT TERMSETS FOR GIVEN QUERY AND TRESHOLD.')

    print('>>>END OF QUESTION 4.')
    for i in range(1, 5):
        print('...')
