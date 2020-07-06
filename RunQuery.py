# Author: Sidhee Hande
# Date: 13.06.2020
# Dumping search data in MongoDB

import Bio
from Bio import Entrez
import time
import math
import pymongo
import time
start_time = time.time()

Bio.Entrez.sleep_between_tries = 15;


# function to perform search in Pubmed
def search_result(query, i):
    Entrez.email = "sidheehande@gmail.com"
    handle = Entrez.esearch(db='pubmed', sort='relevance', retstart=i, retmax='100', retmode='xml', term=query,
                            usehistory='y', api_key='58799a12ed34c36e16407a83ba512b139b08')
    results = Entrez.read(handle)
    time.sleep(100)
    return results


# function to fetch details from list of ids
def fetch_details(id_list):
    ids = ','.join(id_list)
    print(len(id_list))
    Entrez.email = "sidheehande@gmail.com"
    handle = Entrez.efetch(db='pubmed', retmode='xml', id=ids)
    results = Entrez.read(handle)
    time.sleep(60)
    return results

# function to insert papers into database
def insert_into_database(papers):
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client['PierianDx']

    # creating collection
    collection = db['GeneNetwork']

    # converting type of papers to instance of dict instead of instance of Bio.Entrez.Parser

    finalpapers = dict(papers)

    # checking type of finalpapers
    print(type(finalpapers))

    # verifying number of records to be inserted at a time
    print(len(papers['PubmedArticle']))

    # inserting in collection
    for i in finalpapers['PubmedArticle']:
        collection.insert_one(i)
        print("Record Inserted")


# main function to call other functions and display results
if __name__ == '__main__':
    itr = 0

    print("Enter MeSH Term you want to search for")
    b = input()
    #print("AND/OR/NOT")
    #operator2 = input()
    #print("Enter the least recent publication date you want papers from in YYYY/MM/DD format")
    #c = input()
    #print("Enter the most recent publication date you want papers from in YYYY/MM/DD format.")
    #print("If the most recent publication date is present, enter 3000")
    #d = input()

    #qu = '(' + '(' + a + ') ' + operator1 + ' (' + b + "[MeSH Terms]" + ')' + ') ' + operator2 + ' (' + '(' + '"' + c + '"' + "[Date - Publication] : " + '"' + d + '"' + "[Date - Publication]" + ')' + ')'
    # qu = '(' + a + ') ' + operator1 + ' (' + b + "[MeSH Terms]" + ')'
    #qu =  '(' + b + "[MeSH Terms]" + ')' + ') ' + operator2 + ' (' + '(' + '"' + c + '"' + "[Date - Publication] : " + '"' + d + '"' + "[Date - Publication]" + ')' + ')'

    qu =   b

    print(qu)
    while (itr <500):
        results = search_result(qu, itr)
        id_list = results['IdList']
        papers = fetch_details(id_list)
        for i, paper in enumerate(papers['PubmedArticle']):
            print("%d) %s" % (i + 1, paper['MedlineCitation']['PMID']))
        insert_into_database(papers)
        itr = itr + 100


    #Printing time required for search operation
    print("--- %s seconds ---" % (time.time() - start_time))
