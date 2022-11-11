import os 
from collections import defaultdict
import partA
import json

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
                    doc_index[doc_count] = filename
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
    f = open("inverted_index.json", 'w')
    f.write(j)
    f.close()

    j = json.dumps(doc_index)
    f = open("doc_index.json", 'w')
    f.write(j)
    f.close()
    
if __name__ == '__main__':
    #index()
    with open('inverted_index.json', encoding='utf-8') as f:
      data = json.load(f)
      print(len(data))
                