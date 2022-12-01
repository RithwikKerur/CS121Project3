import partA
from collections import defaultdict
import json
import math
from nltk.stem import PorterStemmer
import time

TOTAL_NUMBER_DOCUMENTS = 55306

def query():
    with open ('Past/doc_index_stem.json') as d:
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
                                doc_frequency = len(second)
                                # for doc_id, term_frequency in second.items():
                                #     tfidf[doc_id] += ((1 + math.log2(term_frequency)) * math.log2(TOTAL_NUMBER_DOCUMENTS/doc_frequency))
                                doc_list.append(set(second.keys())) #first = term, {docids:term frequency}
                                doc_dicts.append(second)
                            line = f.readline()
                            first, second = line.split('?')
        #print(f'Before Intersection: {doc_list}')
        '''
        For every document in doc_list, for each term, calculate tf-idf
        Store in a new map, the doc_id : tf-idf
        Rank/sort based off of tf-idf ranking
        '''
        #Gets all documents in common
        if len(doc_dicts) == 1:
            # with open ('Past/doc_index_stem.json') as d:
            doc_index = json.load(d)

            results = []
            # print("Here")
            for i in sorted(doc_dicts[0].items(), key = lambda x : x[1], reverse=True):# doc_dicts[0].items():
                file = doc_index[str(i[0])]
                with open(file) as f:
                    content = json.load(f)
                    # results.append(content['url'])
                    results.append(content['url'])
            # best_results = []
            toc = time.perf_counter()
            for i in range(len(results[:10])):
                print(f'{i+1}: {results[i]}')
            # for _ in range(10):
            #     new_result = max(results, key = lambda x : doc_dicts[0][x[1]])
            #     best_results.append(new_result[0])
            #     results.remove(new_result)

            # toc = time.perf_counter()
            # for i in range(len(best_results)):
            #     print(f'{i+1}: {best_results[i]}')
                        
        elif len(doc_list) > 0:
            doc_list = set.intersection(*doc_list)
            tfidf = defaultdict(int)
            for term in doc_dicts:
                for doc_id, term_frequency in term.items():
                    if doc_id in doc_list:
                        tfidf[doc_id] += ((1 + math.log2(term_frequency)) * math.log2(TOTAL_NUMBER_DOCUMENTS/doc_frequency))
            
            #print(f'After Intersection: {doc_list}')

            with open ('Past/doc_index_stem.json') as d:
                doc_index = json.load(d)

                results = []
                for i in sorted(tfidf.items(), key = lambda x : x[1], reverse=True):
                    file = doc_index[str(i[0])]
                    with open(file) as f:
                        content = json.load(f)
                        results.append(content['url'])
        

            #print(results[:5])

            for i in range(len(results[:10])):
                print(f'{i+1}: {results[i]}')
            toc = time.perf_counter()
        else:
            print("No documents found")

        print(f"Ran in {toc - tic:0.4f} seconds")
    
    #return 5 closest sites (ones with the most number of total query words)

    #Load doc index into memory and return top 5 urls 


if __name__ == '__main__':
    query()