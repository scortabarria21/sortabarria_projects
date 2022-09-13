import sys
from unittest import result

from numpy import array, empty
from py import process
import file_io
import nltk
nltk.download('stopwords')
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

'''In this class, we read through three files (that are passed in) and populate dictionaries. Using these dictionaries, the program takes in a query and prints
out the ten most related document titles.'''
class Query:
    def __init__(self, page_rank : bool, title_path : str, document_path : str, words_path : str):
        self.page_rank = page_rank
        self.is_string = bool
        self.page_id_to_relevance = {}
        self.ids_to_titles = {}
        self.ids_to_ranks = {}
        self.words_to_doc_relevance = {}
        file_io.read_title_file(title_path, self.ids_to_titles)
        file_io.read_docs_file(document_path, self.ids_to_ranks)
        file_io.read_words_file(words_path, self.words_to_doc_relevance)

        self.fix_relevance(page_rank)

        self.STOP_WORDS = set(stopwords.words('english'))
        self.nltk_test = PorterStemmer()
        self.nltk_test.stem("Stemming") # outputs "stem"

        self.make_REPL()
        

    '''This method allows us to ask the user for input into the query. With this input, we are able to determine the most relevant documents. This method also 
    allows us to end the query when necessary'''
    def make_REPL(self):
        user_input = ""
        while True:
            user_input = input("query: ")
            if user_input == "quit":
                break
            self.using_query(user_input)
    

    '''This method handles the bulk of the querying process. It takes in a user input and processes it into words we can use. We then calculate the scores of
    each document to determine the ten most relevant documents.'''
    def using_query(self, user_input):
        stop_words = set(stopwords.words("english"))
        portstemmer = PorterStemmer()

        words = [portstemmer.stem(x) for x in user_input.lower().split(" ") if x not in stop_words]
        id_to_relevance = {}
        for word in words:
            if word in self.words_to_doc_relevance:
                for id, relevance in self.words_to_doc_relevance[word].items():
                    if id not in id_to_relevance:
                        id_to_relevance[id] = 0.0
                    id_to_relevance[id] += relevance

        if not id_to_relevance:
            print("Couldn't find documents! Sorry.")
            return

        results = list(id_to_relevance.keys())
        if self.page_rank:
            results.sort(reverse = True, key =lambda y : id_to_relevance[y] * self.ids_to_ranks[y])
        else:
            results.sort(reverse = True, key =lambda y : id_to_relevance[y])
        self.new_print_results(results)
        return results

    
    '''This method allows us to determine how many titles we're supposed to print. It also prints these results. It takes in a list.'''
    def new_print_results(self,results):
        num = min(len(results), 10)
        for i in range(0,num):
            print(self.ids_to_titles[results[i]])
        pass

    '''This method is used to include the pagerank in our calculations. It takes in a boolean which tells us wether or not pagerank should be included.'''
    def fix_relevance(self, page_rank : bool):
        if page_rank:
            for word in self.words_to_doc_relevance:
                for id in self.words_to_doc_relevance[word]:
                    self.words_to_doc_relevance[word][id] = self.words_to_doc_relevance[word][id] * self.ids_to_ranks[id]


'''This is the main nethod which allows us to use the query class in the terminal. It accounts for errors, such as inputting the wrong number of arguments.'''
if __name__ == "__main__":
    try:
        if len(sys.argv) == 5:
            if sys.argv[1] == "--pagerank":
                q = Query(True, sys.argv[2], sys.argv[3], sys.argv[4])
            else:
                q = Query(False, sys.argv[2], sys.argv[3], sys.argv[4])
        elif len(sys.argv) == 4:
            q = Query(False, sys.argv[1], sys.argv[2], sys.argv[3])
        else: 
            raise ValueError
    except: 
        print("wrong number of arguments")
    
    

    '''ERRORS:
    1. query isnt working perfectly (errors when not two vital words)'''
