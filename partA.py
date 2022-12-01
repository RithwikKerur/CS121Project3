# python partA.py testfile.txt (How it will get called)
from collections import defaultdict
import sys
import json 
import io
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
import unidecode

stopwords = set(['a',	'about',	'above',	'after',	'again',	'against',	'all',	'am',	'an',	'and',	'any',	'are','as',	'at',	'be',	'because',	'been',	'before',	'being',	'below',	'between',	'both',	'but',	'by',	'cannot',	'could',	'did',		'do',	'does',		'doing',	'down',	'during',	'each',	'few',	'for',	'from',	'further',	'had',	'has',		'have',		'having',	'he',	'her',	'here',		'hers',	'herself',	'him',	'himself',	'his',	'how',		'i','if',	'in',	'into',	'is',		'it',		'its',	'itself',		'me',	'more',	'most',		'my',	'myself',	'no',	'nor',	'not',	'of',	'off',	'on',	'once',	'only',	'or',	'other',	'ought',	'our',	'ours',	'out',	'over',	'own',	'same',		'she',		'should',		'so',	'some',	'such',	'than',	'that',		'the',	'their',	'theirs',	'them',	'themselves',	'then',	'there',		'these',	'they',		'this',	'those',	'through',	'to',	'too',	'under',	'until',	'up',	'very',	'was',	'we',			'were',		'what',	'when',	'where',	'which',	'while',	'who',	'whom',	'why',	'with',	'would',	'you','your',	'yours',	'yourself',	'yourselves',	'ourselves'])


#This function should run in O(n^2) time complexity where n is the number of lines in the file
#This is because for each line we iterate over, we have to iterate over a possible infinite number of characters, resulting in 
#an n^2 run time in the worst case.
def tokenize(file: str) -> list:
  all_tokens = []
  curr_token = []
  #f'Downloads/{file}'
  try:
    ps = PorterStemmer()
    with open(file, encoding='utf-8') as f:
      data = json.load(f)
      parser = BeautifulSoup(data['content'], 'xml')
      curr_token = []

      if parser is not None:
        for tags in parser.findAll('b'):
          for i in tags.get_text().strip():
            for char in i:
              if char.isalnum():
                curr_token.append(char)
              else:
                if curr_token != []:
                  new_token = "".join(curr_token).lower()
                  #First we stem the token then check if the length is greater than 1
                  new_token = ps.stem(new_token)
                  if len(new_token) > 1:
                    all_tokens.append(unidecode.unidecode(new_token).replace(" ", "").lower())
                  curr_token = []
            

        for tags in parser.findAll('h1'):
          for i in tags.get_text().strip():
            for char in i:
              if char.isalnum():
                curr_token.append(char)
              else:
                if curr_token != []:
                  new_token = "".join(curr_token).lower()
                  #First we stem the token then check if the length is greater than 1
                  new_token = ps.stem(new_token)
                  if len(new_token) > 1:
                    all_tokens.append(unidecode.unidecode(new_token).replace(" ", "").lower())
                  curr_token = []
        
        for tags in parser.findAll('h2'):
          for i in tags.get_text().strip():
            for char in i:
              if char.isalnum():
                curr_token.append(char)
              else:
                if curr_token != []:
                  new_token = "".join(curr_token).lower()
                  #First we stem the token then check if the length is greater than 1
                  new_token = ps.stem(new_token)
                  if len(new_token) > 1:
                    all_tokens.append(unidecode.unidecode(new_token).replace(" ", "").lower())
                  curr_token = []
        
        if parser.find('title') is not None:
          for tags in parser.find('title'):
            for i in tags.get_text().strip():
              for char in i:
                if char.isalnum():
                  curr_token.append(char)
                else:
                  if curr_token != []:
                    new_token = "".join(curr_token).lower()
                    #First we stem the token then check if the length is greater than 1
                    new_token = ps.stem(new_token)
                    if len(new_token) > 1:
                      all_tokens.append(unidecode.unidecode(new_token).replace(" ", "").lower())
                    curr_token = []
      
      f = io.StringIO(parser.get_text())
      if f.readable():
        while True:
          try:
            line = f.readline()
            if not line:
              break
            for char in line:
              if char.isalnum():
                curr_token.append(char)
              else:
                if curr_token != []:
                  new_token = "".join(curr_token).lower()
                  #First we stem the token then check if the length is greater than 1
                  new_token = ps.stem(new_token)
                  if len(new_token) > 1:
                    all_tokens.append(unidecode.unidecode(new_token).replace(" ", "").lower())
                  curr_token = []
          except Exception as e:
            new_token = "".join(curr_token).lower()
            #First we stem the token then check if the length is greater than 1
            new_token = ps.stem(new_token)
            if len(new_token) > 1:
              all_tokens.append(unidecode.unidecode(new_token.lower()))
            curr_token = []
      
  except Exception as e:
    print(e)
    exit()
  return all_tokens

def countFrequencies(tokens: list, common_words) -> dict:
  #counts = defaultdict(int)
  for token in tokens:
    common_words[token] += 1
  
  return common_words

'''
def printTokens(counts: dict) -> None:
  for token, count in sorted(counts.items(), key=lambda token : token[1]): #, reverse=True
    print(f'{token} -> {count}')
if __name__ == '__main__':
  text_file = sys.argv[-1]
  try:
    printTokens(countFrequencies(tokenize(text_file)))
  except:
    pass
'''