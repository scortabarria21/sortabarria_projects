from ast import Assert
import pytest
from index import *
from query import *

# indexer3 = Index("example.xml", "titles.txt", "doc.txt", "words.txt")

def test_page_rank():
    # testing page rank on PageRankExample1 file
    indexer = Index("PageRankExample1.xml", "titles.txt", "doc.txt", "words.txt")
    my_dict = {1: 0.4326, 2 : 0.2340, 3 : 0.3333}
    test_dict = indexer.page_rank()
    for id in my_dict:
        assert -0.0001 < test_dict[id] - my_dict[id] < 0.0001


    #testing page rank on PageRankExample2 file
    indexer2 = Index("PageRankExample2.xml", "titles.txt", "doc.txt", "words.txt")
    dict2 = {1: 0.2018, 2: 0.0375, 3: 0.3740, 4: 0.3867}
    test_dict2 = indexer2.page_rank()
    for id in dict2:
        assert -0.0001 < test_dict2[id] - dict2[id] < 0.0001

    #testing page rank on PageRankExample3 file
    indexer3 = Index("PageRankExample3.xml", "titles.txt", "doc.txt", "words.txt")
    dict3 = {1: 0.0524, 2: 0.0524, 3: 0.4476, 4: 0.4476}
    test_dict3 = indexer3.page_rank()
    for id in dict3:
        assert -0.0001 < test_dict3[id] - dict3[id] < 0.0001

    #testing page rank on PageRankExample4 file
    indexer4 = Index("PageRankExample4.xml", "titles.txt", "doc.txt", "words.txt")
    dict4 = {1: 0.0375, 2: 0.0375, 3: 0.4625, 4: 0.4625}
    test_dict4 = indexer4.page_rank()
    for id in dict4:
        assert -0.0001 < test_dict4[id] - dict4[id] < 0.0001


def test_relevances():
    #testing relevance on example1 we created (larger/more complicated file)
    indexer1 = Index("example.xml", "titles.txt", "doc.txt", "words.txt")
    rel_dict1 = {'unreferenc': {0: 0.69314718},
    'date': {0: 0.69314718},
    'may': {0: 0.693147180},
    '2010': {0: 0.6931471805},
    'macro': {0: 0.6931471805, 1: 0.346573590},
    'histor': {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0},
    'histori': {0: 0.69314718, 1: 0.346573590},
    'anoth': {0: 0.693147180},
    'exampl': {0: 0.1438410362,
    1: 0.28768207,
    3: 0.28768207},
    'anatop': {1: 0.69314718055},
    'philosophi': {2: 0.69314718},
    'dog': {3: 1.3862943611},
    'cri': {3: 1.3862943611},
    'psychohistori': {3: 1.3862943611}}
    test_dict1 = indexer1.calc_relevance()
    for word in rel_dict1.keys():
        for id in rel_dict1[word].keys():
            assert -0.001 < test_dict1[word][id] - rel_dict1[word][id] < 0.001
    


    #testing relevances on our example2 file (file that handles examples with links and pipes)
    indexer2 = Index("example2.xml", "titles.txt", "doc.txt", "words.txt")
    rel_dict2 = {'dog': {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0},
    'bit': {0: 0.3465735, 2: 0.1732867},
    'man': {0: 0.3465735, 3: 0.3465735},
    'ate': {1: 0.23104906, 2: 0.1732867},
    'chees': {1: 0.69314718, 2: 0.6931471},
    'bad': {3: 1.386294361}}
    test_dict2 = indexer2.calc_relevance()
    for word in rel_dict2.keys():
        for id in rel_dict2[word].keys():
            assert -0.001 < test_dict2[word][id] - rel_dict2[word][id] < 0.001

    #testing relevance with example 3 (file that has no stop words)
    indexer3 = Index("example3.xml", "titles.txt", "doc.txt", "words.txt")
    rel_dict3 = {'thesi': {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0},
    'dog': {0: 0.28768207,
    1: 0.14384103,
    3: 0.28768207},
    'bit': {0: 0.34657359, 2: 0.231049},
    'man': {0: 0.34657359, 3: 0.3465735},
    'ate': {1: 0.6931471805},
    'chees': {1: 0.69314718, 2: 0.6931471},
    'bad': {3: 1.3862943}}
    test_dict3 = indexer3.calc_relevance()
    for word in rel_dict3.keys():
        for id in rel_dict3[word].keys():
            assert -0.001 < test_dict3[word][id] - rel_dict3[word][id] < 0.001

    #testing relevance with example 4 (wfile where)
    indexer4 = Index("example4.xml", "titles.txt", "doc.txt", "words.txt")
    rel_dict4 = {'thesi': {0: 0.0, 1: 0.0, 2: 0.0},
    'dog': {0: 0.203, 1: 0.405},
    'bit': {0: 0.203, 2: 0.203},
    'man': {0: 0.549},
    'ate': {1: 1.099},
    'chees': {1: 0.405, 2: 0.405}}
    test_dict4 = indexer4.calc_relevance()
    for word in rel_dict4.keys():
        for id in rel_dict4[word].keys():
            assert -0.001 < test_dict4[word][id] - rel_dict4[word][id] < 0.001
    
    indexer5 = Index("myPractice2.xml", "titles.txt", "doc.txt", "words.txt")
    rel_dict5 = {'categori': {0: 0.0, 1: 0.0},
    'hello': {0: 0.69314718},
    'comput': {1: 0.346573590},
    'scienc': {1: 0.34657359},
    'b': {1: 0.346573590}}
    test_dict5 = indexer5.calc_relevance()
    for word in rel_dict5.keys():
        for id in rel_dict5[word].keys():
            assert -0.001 < test_dict5[word][id] - rel_dict5[word][id] < 0.001



def test_tf():
    Indexer1 = Index("example.xml", "titles.txt", "doc.txt", "words.txt")
    for word in Indexer1.words_ids_to_tf:
        for id in Indexer1.words_ids_to_tf[word]:
            assert Indexer1.words_ids_to_tf[word][id] == Indexer1.words_to_doc_frequency[word][id]/Indexer1.ids_to_max_counts[id]

    Indexer2 = Index("example2.xml", "titles.txt", "doc.txt", "words.txt")
    for word in Indexer2.words_ids_to_tf:
        for id in Indexer2.words_ids_to_tf[word]:
            assert Indexer2.words_ids_to_tf[word][id] == Indexer2.words_to_doc_frequency[word][id]/Indexer2.ids_to_max_counts[id]
    
    Indexer3 = Index("example3.xml", "titles.txt", "doc.txt", "words.txt")
    for word in Indexer3.words_ids_to_tf:
        for id in Indexer3.words_ids_to_tf[word]:
            assert Indexer3.words_ids_to_tf[word][id] == Indexer3.words_to_doc_frequency[word][id]/Indexer3.ids_to_max_counts[id]
    
    Indexer4 = Index("example4.xml", "titles.txt", "doc.txt", "words.txt")
    for word in Indexer4.words_ids_to_tf:
        for id in Indexer4.words_ids_to_tf[word]:
            assert Indexer4.words_ids_to_tf[word][id] == Indexer4.words_to_doc_frequency[word][id]/Indexer4.ids_to_max_counts[id]


def test_idf():
    indexer1 = Index("example.xml", "titles.txt", "doc.txt", "words.txt")
    for word in indexer1.words_idf:
        assert indexer1.words_idf[word] == math.log(len(indexer1.ids_to_titles)/len(indexer1.words_to_doc_frequency[word]))

    indexer2 = Index("example2.xml", "titles.txt", "doc.txt", "words.txt")
    for word in indexer2.words_idf:
        assert indexer2.words_idf[word] == math.log(len(indexer2.ids_to_titles)/len(indexer2.words_to_doc_frequency[word]))

    indexer3 = Index("example3.xml", "titles.txt", "doc.txt", "words.txt")
    for word in indexer3.words_idf:
        assert indexer3.words_idf[word] == math.log(len(indexer3.ids_to_titles)/len(indexer3.words_to_doc_frequency[word]))

    indexer4 = Index("example4.xml", "titles.txt", "doc.txt", "words.txt")
    for word in indexer4.words_idf:
        assert indexer4.words_idf[word] == math.log(len(indexer4.ids_to_titles)/len(indexer4.words_to_doc_frequency[word]))