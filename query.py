import partA
from collections import defaultdict
import json

def query():
    query = input('Enter Query: ')
    query = query.split(' ')
    with open('Past/inverted_index_stem.txt', 'r') as f:

        with open ('Past/indexed_index1.json') as l:
            letter_index = json.load(l)
            term_maps = dict()
            for i in range(len(query)):
                curr_index = letter_index[query[i][0]]#query[i][0]
                f.seek(curr_index)
                
            #sort queries by length of dictionary
            relavent_documents = defaultdict(int)
    
    #for term in query:
        #Grab term map from file


    #start with using AND on 1st 2, and continue from there
    #return 5 closest sites (ones with the most number of total query words)


if __name__ == '__main__':
    query()