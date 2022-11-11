import os 
from collections import defaultdict
import partA

def index():
    directory = 'Dev'
    words = defaultdict(int)
    unique_pages = set()

    inverted_index = dict()
    doc_index = dict()
    doc_count = 1

    for dirname in os.listdir(directory):
        for filename in os.listdir(directory + '/' + dirname):
            f = os.path.join(directory, dirname, filename)
            all_tokens = partA.tokenize(f)
            print(all_tokens)
            if len(all_tokens) < 10000:
                doc_index[doc_count] = filename
                with open(f, 'r') as curr_file:
                    url = curr_file.readline()
                    defrag_url = url.split('#')[0]
                    unique_pages.add(defrag_url.rstrip('\n'))

                # with open(filename, 'r') as f:
                #print(f'{url} has {len(all_tokens)} number of words')
                
                words = partA.countFrequencies(all_tokens, words)
                print(words)
                for word in words:
                    if word in inverted_index:
                        inverted_index[word].append(doc_count)
                    else:
                        inverted_index[word] = [doc_count]
                
                words = defaultdict(int)

                doc_count += 1
        break
    print(inverted_index)
    print(doc_count)
    
if __name__ == '__main__':
    index()
                