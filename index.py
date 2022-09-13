import sys
from os import link
from pydoc import pager
import re
from telnetlib import PRAGMA_HEARTBEAT
import xml.etree.ElementTree as et
import math


import file_io
import nltk
nltk.download('stopwords')
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

'''This class is meant to parse through the xml file and populate the various dictionaries. It also writes onto three other txt files 
that are passed in.'''
class Index:
    def __init__(self, wiki_path : str, title_path : str, document_path : str, words_path : str):
        self.ids_to_titles = {}
        self.titles_to_ids = {}
        self.words_to_doc_relevances = {}
        self.ids_to_rank = {}
        self.words_to_doc_frequency = {}
        self.ids_to_max_counts = {}
        self.ids_to_links = {}
        self.term_frequency = {}
        self.words_idf = {}
        self.words_ids_to_tf = {}


        #stop words
        self.STOP_WORDS = set(stopwords.words('english'))
        # examples:
        'the' in self.STOP_WORDS # True
        'milda' in self.STOP_WORDS # False
        #stemming 
        self.nltk_test = PorterStemmer()
        self.nltk_test.stem("Stemming") # outputs "stem"

        self.parse(wiki_path)
        self.page_rank()
        self.calc_tf()
        self.calc_idf()
        self.calc_relevance()
        

        file_io.write_title_file(title_path, self.ids_to_titles)
        file_io.write_words_file(words_path, self.words_to_doc_relevances)
        file_io.write_docs_file(document_path, self.ids_to_rank)
            
    '''This method is used to parse through the entire corpus and process all of the words and links. I takes in a file to parse through'''
    def parse(self, file : str):
        wiki_pages = et.parse(file).getroot()

        for page in wiki_pages:
            title: str = page.find('title').text.strip()
            page_id: int = int(page.find('id').text)

            self.ids_to_titles[page_id] = title
            self.titles_to_ids[title] = page_id
            
        for i,page in enumerate(wiki_pages):
            print(f"PROGRESS: {i}/ {len(wiki_pages)}")
            title: str = page.find('title').text.strip()
            page_id: int = int(page.find('id').text)

            page_text = page.find('text').text
            page_text += " " + title
            self.myRegex = r"\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+"
            words = re.findall(self.myRegex, page_text)
            
            for word in words:
                if word == "":
                    continue
                if self.check_if_link(word):
                    title, text = self.process_link(word)
                    text = [self.stop_and_stem(x) for x in text]
                    if page_id not in self.ids_to_links:
                        self.ids_to_links[page_id] = set()
                    if title in self.titles_to_ids and self.titles_to_ids[title] != page_id:
                        self.ids_to_links[page_id].add(self.titles_to_ids[title])
                    for x in text:
                        if x not in self.words_to_doc_frequency:
                            self.words_to_doc_frequency[x] = {}
                        if page_id not in self.words_to_doc_frequency[x]:
                            self.words_to_doc_frequency[x][page_id] = 0
                        self.words_to_doc_frequency[x][page_id] +=1
                        self.update_frequency(x, page_id)
                
                else: #stem and stop the word and add to dictionaries
                    lower_word = word.lower()
                    if lower_word not in self.STOP_WORDS:
                        stem_word = PorterStemmer().stem(lower_word)
                        if stem_word not in self.words_to_doc_frequency:
                            self.words_to_doc_frequency[stem_word] = {}
                        if page_id not in self.words_to_doc_frequency[stem_word]:
                            self.words_to_doc_frequency[stem_word][page_id] = 0
                        self.words_to_doc_frequency[stem_word][page_id] +=1
                        self.update_frequency(stem_word, page_id)

        
    '''This method returns a boolean that lets us know if a word is a link or not.'''
    def check_if_link(self, word):
        my_word = word.strip()
        link_regex = r"\[\[[^\[]+?\]\]"
        return bool(re.match(link_regex, my_word))
            

    '''This method is used to process links. It also handles the case in which the link has a pipe. '''
    def process_link(self, str):
        my_word = str[2 : -2]
        my_regex = r"[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+"
        title = my_word
        text = my_word
        if "|" in my_word:
                split_link = my_word.split("|")
                title= split_link[0]
                text = split_link[1]
        text = re.findall(my_regex, text)
        return title.strip(), text 
            
    '''This method is used to remove the stop words and stem for any word that is passed in. It is used on all of the words in the corpus'''
    def stop_and_stem(self, word : str):
        if word.lower() in self.STOP_WORDS:
            return ""
        else: 
            stem_word = self.nltk_test.stem(word.lower())
            return stem_word
    

    '''This method calculates all of the weights for each document. It also creates the weight dictionary and populates it. This method is used to calculate 
    pagerank.'''
    def calc_weight(self):
        # quantifying relationship between each page and every other page
        # for every k see if it links to j 

        # for k # for j and use ids to links to see if k links to j... 
        # idstolinks[j] and check if k is inside of that 
        
       # ids to titles hashmap
        epsilon = 0.15
        weight = {}
        
        for j in self.ids_to_titles:
            for k in self.ids_to_titles:
                if j not in weight:
                    weight[j] = {}
                if j == k:
                    weight[j][k] =  epsilon/len(self.ids_to_titles)
                elif j not in self.ids_to_links or len(self.ids_to_links[j]) == 0:
                    weight[j][k] = epsilon/len(self.ids_to_titles) + (1 - epsilon) * (1 / (len(self.ids_to_titles)-1))
                else:
                    if k not in self.ids_to_links[j]:
                        #link once to everything except to itself
                        weight [j][k] = epsilon/len(self.ids_to_titles)
                        # nk for this case is n-1
                    else:
                        weight[j][k] =  epsilon/len(self.ids_to_titles) + (1 - epsilon)*(1/len(self.ids_to_links[j]))
        return weight
    
    '''This method is used to calculate total difference in the pageranks from one iteration to another. It is used to determine when
    the pagerank calculations should end'''
    def distance(self, prev_rank, current_rank):
        my_sum = 0
        for id in current_rank:
            my_sum += (current_rank[id] - prev_rank[id])**2
        distance = math.sqrt(my_sum)
        return distance
    
    '''This method calculates the pagerank for each document and populates the ids_to_rank dictionary '''
    def page_rank(self):
        prev_rank = {}
        self.ids_to_rank = {}

        for id in self.ids_to_titles.keys():
            prev_rank[id] = 0
            self.ids_to_rank[id] = 1/len(self.ids_to_titles)
           
        my_weight = self.calc_weight()
        while self.distance(prev_rank, self.ids_to_rank) > 0.001: 
            prev_rank = self.ids_to_rank.copy()
            for j in self.ids_to_titles.keys():
                self.ids_to_rank[j] = 0
                for k in self.ids_to_titles.keys():
                        self.ids_to_rank[j] = self.ids_to_rank[j] + my_weight[k][j] * prev_rank[k]
        return self.ids_to_rank
    
    
    '''This method updates the ids_to_max_counts dictionary for a word and page id that are passed in'''
    def update_frequency(self, word: str, page_id : int):
         if page_id not in self.ids_to_max_counts:
            self.ids_to_max_counts[page_id] = 0
         self.ids_to_max_counts[page_id] = max(self.ids_to_max_counts[page_id], self.words_to_doc_frequency[word][page_id])
         
    '''This method combines each word's idf and tf to determine its relevancy for each document it appears in'''
    def calc_relevance(self):
        for word in self.words_ids_to_tf:
            if word == "":
                continue
            self.words_to_doc_relevances[word] = {}
            for id in self.words_ids_to_tf[word]:
                self.words_to_doc_relevances[word][id] = self.words_ids_to_tf[word][id] * self.words_idf[word]
        return self.words_to_doc_relevances
        
    '''This method is used to calculate the term frequency for each word for each of its documents. It is used to calculate a word's 
    relevancy'''
    def calc_tf(self):
        for word in self.words_to_doc_frequency.keys():
            self.words_ids_to_tf[word] = {}
            for id in self.words_to_doc_frequency[word]:
                frequency = self.words_to_doc_frequency[word][id]
                self.words_ids_to_tf[word][id] = frequency/self.ids_to_max_counts[id]
       
    '''This method is used to calculate the inverse document frequency for each word. Used in calculating a word's relevancy'''
    def calc_idf(self):
        for word in self.words_to_doc_frequency:
            self.words_idf[word] = math.log(len(self.ids_to_titles)/len(self.words_to_doc_frequency[word]))
        
        
'''This main method allows us to access the Index class through the terminal.'''
    # need to write main method something like 
if __name__ == "__main__":

    if len(sys.argv) == 5:
        Index(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    else:
        print("not enough arguments")
