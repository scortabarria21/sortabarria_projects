Names: Santiago Cortabarria and Angela Osei-Ampadu

Bugs: no known bugs in the program

Instructions for use: In the terminal, the user should index the file he wants to parse. They can do this by writing "python3 index.py" followed by the 
file being parsed, a txt file for titles, a txt file for documents, and a txt file for words. After pressing enter, the user must now run the query. To do this,
the user must write "python3 query.py". If the user wants pagerank considered in the scoring of documents, he must follow this with "--pagerank". Following this,
the user must write the same three files that were indexed in the same order. After pressing enter, the user should see the line "query: " in the terminal.
The user should enter any key words they wants to search for and press enter. Once that has been done, the user will see the ten most relevant document titles 
printed out in order in the terminal.

How pieces work together: In the indexer we must parse through the given xml file to determine the relevance of each word to each page. We do this by first
processing all of the text and links and organizing them into dictionaries. Once this is done, we use this information to calculate the relevance of each word to 
each document its in. We also calculate the pagerank using the set of links. Using this information, we write the words.txt, titles.txt, and doc.txt files. 
Once we've finished this process, it's time to query. THe query class accesses the information on the words.txt, titles.txt, and doc.txt files and uses it to
fill up each file's respective dictionary. Once this is done, we can take in a query and look for the documents with the highest relevance to the query. The
query class finishes by printing the titles of the ten most relevant documents.

Additional feauteres:

Description of testing:
In the test.py class we included unit testing for the most important features of our indexer class.

Index Testing:
Testing pagerank:
Our first test is for pagerank which we tested by using the 4 page rank examples provided to us. We 
created instances of the index with with each page rank example file and compared it with the dictionary
values we calculated for the pageRank for each file. Because python's value for page rank is very exact and
goes up many decimal places, we made sure our value was within a 0.0001 range of the actual page rank value 
for each example file

Testing relevance:
We created 4 instances of index and passed in 4 example files, all of which we created. Each example file
contains different edge cases. The first file, example, is our most complex one and contains words in both 
titles and texts and different kinds of links, (links with [[]], colon, and links with pipes)
The example2 file contains the case where there are titles, some stop words such as "the", and links.
The example3 file contains the case where there are no stop words, and there are titles.
The example4 files contains the case where there are no titles. There are also no stop words in this file.
The myPractice2 file contains the case whee we have a colon on the title
In all these examples, our indexer is able to correctly calculate relevance. We assert the value of relevance
dictionary for each file, which we calculated, is equal to calling our calculate relevance method on the instances 
of the indexer we created and that the margin of error is less than .001 between the values we calculated and the actual relevances

Testing tf and idf:
For testing term frequency and idf we created instances of the index class once again using the example files we created
For tf we looped through each word in the words_ids_to_tf dictionary and each id in that dictionary at that word index and 
made sure that that was equal to the words_to_doc_frequency[word][id] over the ids_to_max_counts[id] dicitonary. 
We did this for all our example files.

For idf we followed a similar process and looped through the words in the words_idf dictionary and made sure that the 
dictionary at that word index was equal to the log of the ids_to_titles dictionary over the words_to_doc_frequency dictionary.
We did this for all the example files we created as well.

System Testing for Query:
Small Wiki: 
For testing the small wiki we picked several words to search up in the querier and checked 
that the querier was outputting pages that those words appeared on and tested it both with and 
without page rank. By comand "F" and looking through small wiki manually, the results of the querier
matched very accurately because the word we searched appeared multiple times on the pages of the results of the querier. 
We did this for 10 words.

Some examples of words we searched up and results we got include:
Ex:
input- "writer" and results witout page rank: Anatopism, In&Out, Popular history, Punic language, Antiquarian, Anachronism, Recorded history, Himera, Tertullian, Philosophy of war
and when we manually command F we find this word on 9/10 
results with page rank: Carthage, Tertullian, Anatopism, Germany, Anachronism, United States, Himera, Punic language, Antiquarian, In&Out
without page rank and 8/10 with pagerank

input - "foundation" and results: Ash heap of history, Mezine, International rankings of France, Psychohistory, Motya, Utica, Tunisia, 
Himera, Selinunte, Feud, International rankings of the United States
and by comand F searching "foundation" it appeared on 10/10 of these reults without rank 
and 9/10 with page rank results: Carthage, Utica, Tunisia, Rome, Ash heap of history, Germany, Himera, Civilian casualty ratio ,
Selinunte, United States, Psychohistory

MedWiki:
Using the MedWiki results file provided to us, we compared our answers with words such as
"baseball", "cats", "fire", "United States" and below are the results (10/10) meaning that all 
the words that appeared in our query reults appeared in the top 20 searches answers given in the MedWiki TA Queries doc

baseball (no page rank) 10/10 
baseball (page rank) 10/10
fire (no page rank) 10/10
fire (page rank) 9/10
United States (no page rank) 10/10
United States (page rank) 10/10
untied (page rank) 10/10
united (no page rank) 10/10
computer science (no page rank) 10/10
computer science (page rank) 7/10
search (no page rank) 10/10
search (page rank) 7/10
cats(no page rank) 10/10
cats(page rank) 10/10
watch (no page rank) 10/10
watch (page rank) 10/10
pope (no page rank) 10/10
pope (page rank) 7/10
battle (no page rank) 10/10
battle(page rank) 9/10

BigWiki:
Since our results for medium wiki were very accurate especially, 100% accurate without page rank and 89%
accurate for testing with page rank, we are fairly confident that our query will perform well against big wiki.
We couldn't test big wiki extensively but our results from medWiki make sure confident in our queriers ability
to handle bigWiki well

Edge Case of invalid input:
In all of these files if you try to search up a word that doesnt exist or an empty query, the program will output "Couldn't find documents! Sorry"
