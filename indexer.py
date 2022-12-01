import os 
from collections import defaultdict
import partA
import json
import re
import unidecode
from pathlib import Path
import math

TOTAL_NUMBER_DOCUMENTS = 55284
def mergePartialIndices():
    curr_dir = os.getcwd()
    files = []
    lines = []
    path = os.path.join(curr_dir, "PartialIndex")

    #Create a list of file objects in the partial index directory
    for filename in os.listdir(path):
        files.append(open(os.path.join(path, filename), 'r'))

    #Create a list of line objects to mark where we currently are 
    for file in files:
        lines.append(file.readline())

    merged = open(f"Past/inverted_index_stem.txt", 'w')
    indexed_index = dict()
    prev_token = 0
    seeked = 0

    #While at least one file has content keep iterating through
    while(len(lines) != 0):
        to_write = []
        prev = None
        tfidf = defaultdict(int)
        
        #iterate through all the lines and get a list of all that have the same token 
        for line in range(len(lines)):
            token, docs = lines[line].split('?')
            if prev == None or token < prev:
                prev = token
                to_write = [line]
            elif prev == token:
                to_write.append(line)

        my_dict = dict()
        my_dict[prev] = dict()
        to_delete = []

        #For all the lines we have to write we merge them into one list
        for line in to_write:
            token, docs = lines[line].split('?')
            my_dict[prev].update(eval(docs))

            new_line = files[line].readline()
            if new_line == "":
                #If the file is done, we will delete it after
                to_delete.append(line)
            else:
                lines[line] = new_line

        #Deleting the file and line objects since we no longer need them 
        for line in to_delete:
            files[line].close()
            del files[line]
            del lines[line]

        doc_frequency = len(my_dict[prev])
        for doc_id, term_frequency in my_dict[prev].items():
            tfidf[doc_id] += ((1 + math.log2(term_frequency)) * math.log2(TOTAL_NUMBER_DOCUMENTS/doc_frequency))
        #Writing the token and accompnaying dictionary to disk
        to_write1 = f'{token}?{dict(sorted(tfidf.items(), key = lambda x: x[0]))}\n'
        merged.write(to_write1)

        if token[0:2] != prev_token:
            prev_token = token[0:2]
            indexed_index[prev_token] = seeked
        
        seeked+= len(str(to_write1))
    
    merged.close()
    i = json.dumps(indexed_index)
    f = open("Past/indexed_index.json", 'w')
    f.write(i)
    f.close()

def index():

    directory = 'Dev'
    words = defaultdict(int)
    unique_pages = set()

    inverted_index = dict()
    doc_index = dict()
    doc_count = 1

    offload = 1
    partial_indices = 0
    
    #We create a new directory to store the partial indicies
    curr_dir = os.getcwd()
    os.mkdir(os.path.join(curr_dir, "PartialIndex"))

    #Iterating through the Dev directory
    for dirname in os.listdir(directory):
        if os.path.isdir(directory + '/' + dirname):
            #Iterating through the sub directories
            for filename in os.listdir(directory + '/' + dirname):
                
                f = os.path.join(directory, dirname, filename)
                all_tokens = partA.tokenize(f)
                if len(all_tokens) < 10000:
                    #If the document isn't wasteful text


                    #doc_index[doc_count] = f #add the doc to our doc index
                    with open(f, 'r') as curr_file:
                        #add the url to our list of unique pages
                        content = json.load(curr_file)
                        url = content['url']
                        defrag_url = url.split('#')[0]
                        unique_pages.add(defrag_url.rstrip('\n'))
                        doc_index[doc_count] = defrag_url
                    
                    #Get the frequencies for all our words
                    words = partA.countFrequencies(all_tokens, words)

                    #Update our inverted index
                    for word, freq in words.items():
                        if word in inverted_index:
                            inverted_index[word][doc_count] = freq
                        else:
                            inverted_index[word] = dict()
                            inverted_index[word][doc_count] = freq
                    
                    words = defaultdict(int)

                    doc_count += 1
                    offload += 1
                
                #Check if it's time to offload the index to disk
                if offload >= 10000:
                    offload = 1
                    j = json.dumps(inverted_index)
                    f = open(f"PartialIndex/inverted_index_stem{partial_indices}.txt", 'w') 
                    for item, freq in sorted(inverted_index.items(), key = lambda x: x[0]):
                        item = unidecode.unidecode(item)
                        to_write = f"{item}?{str(freq)}\n"
                        
                        f.write(to_write)
                    inverted_index = dict()

                    partial_indices += 1
        
        
    #Dump the remaining index to disk 
    j = json.dumps(inverted_index)
    f = open(f"PartialIndex/inverted_index_stem{partial_indices}.txt", 'w')
    prev = 0
    seeked = 0
    indexed_index = dict()
    for item, freq in sorted(inverted_index.items(), key = lambda x: x[0]):
        item = unidecode.unidecode(item)
        to_write = f"{item}?{str(freq)}\n"
        
        f.write(to_write)
        '''
        if item[0] != prev:
            prev = item[0]
            indexed_index[prev] = seeked
        
        seeked+= len(str(to_write))
        '''
        
    f.close()

    '''
    i = json.dumps(indexed_index)
    f = open("Past/indexed_index.json", 'w')
    f.write(i)
    f.close()
    '''
    

    j = json.dumps(doc_index)
    f = open("Past/doc_index_stem.json", 'w')
    f.write(j)
    f.close()

    print(len(unique_pages))
    
if __name__ == '__main__':
    #index()
    mergePartialIndices()
    
    
             