import os 
from collections import defaultdict
import partA
import json
import re
import unidecode


def index():
    directory = 'Dev'
    words = defaultdict(int)
    unique_pages = set()

    inverted_index = dict()
    doc_index = dict()
    doc_count = 1

    for dirname in os.listdir(directory):
        if os.path.isdir(directory + '/' + dirname):
            for filename in os.listdir(directory + '/' + dirname):
                f = os.path.join(directory, dirname, filename)
                all_tokens = partA.tokenize(f)
                if len(all_tokens) < 10000:
                    doc_index[doc_count] = f
                    with open(f, 'r') as curr_file:
                        url = curr_file.readline()
                        defrag_url = url.split('#')[0]
                        unique_pages.add(defrag_url.rstrip('\n'))
                    
                    words = partA.countFrequencies(all_tokens, words)
                    for word, freq in words.items():
                        if word in inverted_index:
                            inverted_index[word][doc_count] = freq
                        else:
                            inverted_index[word] = dict()
                            inverted_index[word][doc_count] = freq
                    
                    words = defaultdict(int)

                    doc_count += 1
        

    j = json.dumps(inverted_index)
    f = open("Past/inverted_index_stem.txt", 'w')
    prev = 0
    seeked = 0
    indexed_index = dict()
    for item, freq in sorted(inverted_index.items(), key = lambda x: x[0]):
        item = unidecode.unidecode(item)
        to_write = f"{item}?{str(freq)}\n"
        
        f.write(to_write)
        if item[0] != prev:
            prev = item[0]
            indexed_index[prev] = seeked
        
        seeked+= len(str(to_write))


    f.close()

    i = json.dumps(indexed_index)
    f = open("Past/indexed_index.json", 'w')
    f.write(i)
    f.close()

    j = json.dumps(doc_index)
    f = open("Past/doc_index_stem.json", 'w')
    f.write(j)
    f.close()

    print(len(unique_pages))
    
if __name__ == '__main__':
    index()
    
    
             