import partA
from collections import defaultdict
import json
import math
from nltk.stem import PorterStemmer
import time

TOTAL_NUMBER_DOCUMENTS = 55306

def query():
    with open ('Past/doc_index_stem.json') as d:
        doc_index = json.load(d)
        query = input('Enter Query: ')
        tic = time.perf_counter()
        query = query.split(' ')
        doc_list = []
        doc_dicts = []
        ps = PorterStemmer()
        tfidf = defaultdict(int) #doc_id : tf-idf
        with open('Past/inverted_index_stem.txt', 'r') as f:

            with open ('Past/indexed_index.json') as l:
                letter_index = json.load(l)
                term_maps = dict()
                for i in range(len(query)):
                    q = ps.stem(query[i].lower())
                    if q[0] in letter_index:
                        curr_index = letter_index[q[0]]#query[i][0]
                        f.seek(curr_index)
                        line = f.readline()
                        
                        
                        first, second = line.split('?')
                        ans = []
                        while(first <= q):
                            if first == q:
                                second = eval(second)
                                if len(tfidf) != 0:
                                    for doc_id, score in second.items():
                                        tfidf[doc_id] += score
                                else:
                                    tfidf = defaultdict(int, second)
                            line = f.readline()
                            first, second = line.split('?')
        #print(f'Before Intersection: {doc_list}')
        '''
        For every document in doc_list, for each term, calculate tf-idf
        Store in a new map, the doc_id : tf-idf
        Rank/sort based off of tf-idf ranking
        '''
        #Gets all documents in common
        if len(tfidf) > 0:

            results = []
            for i in sorted(tfidf.items(), key = lambda x : x[1], reverse=True):
                results.append(doc_index[str(i[0])])

            #print(results[:5])

            toc = time.perf_counter()
            for i in range(len(results[:10])):
                print(f'{i+1}: {results[i]}')
            print(f"Ran in {toc - tic:0.4f} seconds")
        else:
            print("No documents found")

    
    #return 5 closest sites (ones with the most number of total query words)

    #Load doc index into memory and return top 5 urls 


if __name__ == '__main__':
    query()