# Gene-to-Gene-Co-Citation-Literature-Network
This project shows the correlation between a pair of genes in terms of how many research paper abstracts they were both found in.
I wrote a Python script for querying the National Center for Biotechnology Information's Pubmed Entrez API to fetch XML documents for the search query "Non Small Cell Lung Cancer" and stored them in my local MongoDB database. Then I performed a search operation for 1255 genes in the retrieved paper abstracts (Genotype Mining) and stored their respective Pubmed Ids(PMIDs). Next, I calculated the number of common PMIDs between every pair of genes and recorded them as weighted edges of an undirected graph.
Finally, I visualised this large scale graph using Cytoscape Network Visualisation Tool and published it on the Network Data Exchange Website for lucid visualisation and analysis

Pubmed:
https://pubmed.ncbi.nlm.nih.gov/
Entrez:
https://www.ncbi.nlm.nih.gov/Web/Search/entrezfs.html
