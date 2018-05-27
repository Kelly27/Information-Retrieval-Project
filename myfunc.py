import math
import PyPDF2 #pip install PyPDF2

class Doc:
    def __init__(self, doc_name, words, freq, tf, tf_idf):
        self.doc_name = doc_name
        self.words = words
        self.freq = freq
        self.tf = tf
        self.tf_idf = tf_idf,

    def __repr__(self):
        return "doc_name: %s, words: %s, freq: %s, tf: %s, tf_idf: %s" % (self.doc_name, self.words, self.freq, self.tf, self.tf_idf)

class Query:
    def __init__(self, q, matched, weight):
        self.q = q
        self.matched = matched
        self.weight = weight

    def __repr__(self):
        return "q: %s, matched: %s, weight: %s" % (self.q, self.mathed, self.weight)

class Termset:
    def __init__(self, termset, freq_termset, small_n):
        self.termset = termset
        self.freq_termset = freq_termset
        self.small_n = small_n

    def __repr__(self):
        return "termset: %s, freq_termset: %s, small_n: %s" % (self.termset, self.freq_termset, self.small_n)

# ===========================================================================
def readFiles(read_file):
    #read pdf file
    fileRead = PyPDF2.PdfFileReader(read_file)
    fileRead.numPages #print total number of pages in the pdf file
    pageObj = fileRead.getPage(0)
    text = pageObj.extractText()
    text = text.replace("\n", "")
    return text.lower()

def rm_punctuation(listing):
    punctuations = ['(', ")", '?', ';',':','[',']',',', '-', "''", '``', '.', "'", "a", "an", "the", 'to', 'of', 'in', 'at', 'as']
    for p in punctuations:
        for kw in listing:
            if(p in listing):
                listing.remove(p)
    return listing

def rm_duplicates(listing):
    final_list = []
    for i in listing:
        if i not in final_list:
            final_list.append(i)
    return final_list

def check_greater(list1, val):
    for x in list1:
        if x < val:
            return False
    return True

def rounddown(x):
    return int(math.floor(x / 10.0)) * 10