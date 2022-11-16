import partA
from collections import defaultdict
import json
from nltk.stem import PorterStemmer


def query():
    query = input('Enter Query: ')
    query = query.split(' ')
    doc_list = []
    ps = PorterStemmer()
    with open('Past/inverted_index_stem.txt', 'r') as f:

        with open ('Past/indexed_index1.json') as l:
            letter_index = json.load(l)
            term_maps = dict()
            for i in range(len(query)):
                curr_index = letter_index[query[i][0]]#query[i][0]
                f.seek(curr_index)
                line = f.readline()
                first, second = line.split('?')
                first = ps.stem(first)
                q = query[i].lower()
                while(first <= q):
                    if first == q:
                        second = eval(second)
                        doc_list.append(set(second.keys()))
                    line = f.readline()
                    first, second = line.split('?')
                    first = ps.stem(first)
    
    #Gets all documents in common
    doc_list = set.intersection(*doc_list)
    print(doc_list)

    with open ('Past/doc_index_stem.json') as d:
        doc_index = json.load(d)

        results = []
        for i in doc_list:
            file = doc_index[str(i)]
            with open(file) as f:
                content = json.load(f)
                results.append(content['url'])

    print(results)

    #return 5 closest sites (ones with the most number of total query words)

    #Load doc index into memory and return top 5 urls 


if __name__ == '__main__':
    query()