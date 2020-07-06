# import pymongo
##db.pubmed_records_new.find({"MedlineCitation.MeshHeadingList.DescriptorName":{$in:["Neoplasms","Cancer","Mutation"]}}).count()


#This program reads the list of all genes and searches each of these genes along with its aliases in the MongoDB database.
# It records the unique PMIDS of the records in which the gene or its alias was found in the AbstractText of the publication.
# Then it stores these results in a dictionary with the gene's main name as the key and the PMIDS as values.
#This dictionary is written to a GeneSearch Results csv file.

import pymongo
import time
import re

start_time = time.time()
import csv

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["PierianDx"]
mycol = mydb["GeneNetwork"]


def genelist():
    genes = list()

    try:
        f=open("AllGenes.csv")
    except:
        print("")
    for line in f:
            line=line.rstrip()
            line=line.split(',')
            line = list(filter(None,line))
            genes.append(line)
    f.close()
    return genes

def mysearch(genes):

    id_list = []
    genesearch={}


    w = csv.writer(open("GeneSearchResults.csv", "w"))

    for i in genes:
        ids=list()
        g=list()
        for j in i:
            filter1 = {"$text": {"$search": j}}
            filter2 = {"MedlineCitation.Article.Abstract.AbstractText": 1}
            filter3 = {"MedlineCitation.PMID": 1,"_id":0}


            mydoc = mycol.find(filter1, filter2)

            id_list = mycol.find(filter1, filter3)

            for id in id_list:
                if id not in ids:
                    ids.append(id)
            g.append(j)

        aliases=','.join(g)

        genesearch.setdefault(g[0], [])

        for x in ids:
            #print(x)
            clx=re.findall('\d+',str(x))
            #print(clx)

            for c in clx:
                c=int(c)
                genesearch[g[0]].append(c)

    w.writerow(["GeneName","PMID"])
    for a,b in genesearch.items():
         w.writerow([a,b])



if __name__ == '__main__':
    genes = genelist()
    mysearch(genes)


    # Printing time required for search operation
    print("--- %s seconds ---" % (time.time() - start_time))
