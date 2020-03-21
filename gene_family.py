import requests
from prody import *
from matplotlib.pylab import *
import re
from gecko import Gene

#This script will query uniprot for homo sapiens with a given gene symbol
#It then uses the uniprot ID to query pfam to find corresponding families to the gene symbol.


my_genes = []
for i in range(1):
    my_genes.append(Gene.Gene("","P53-1321AS","","")) #Make object have a - for splitting
    my_genes.append(Gene.Gene("","BRCA1","",""))
    my_genes.append(Gene.Gene("","ESR1.2","",""))

#function to search uniprot with variable query (given in next function)
def search_uniprot(query,format = 'txt'):
    base_url = 'https://www.uniprot.org/uniprot'
    payload = {'query':query, 'format':format}
    result = requests.get(base_url,params = payload)
    if result.ok:
        return result.content
    else:
        print('Error')

fam_dict = {}

#Split the gene symbols (Remove the parts after - or .)
def gen_symbol():
    symbol_list = []
    for gene in my_genes:
        gen_symbol = re.findall(r"[\w']+", gene.name)[0]
        symbol_list.append(gen_symbol)

    return symbol_list

#Fucntion to query uniprot and use uniprot id to query pfam
def query(fam_dict,symbol_list):
    for gene_symbol in symbol_list:
        query = "organism:homo sapiens and gene_exact: " + gene_symbol
        res = search_uniprot(query) #search uniprot using above query
        info = res.decode()  #bytes before decoding
        uniprot_id = info.strip().split("\n")
        uniprot_id = uniprot_id[1].split()
        uniprot_id = uniprot_id[1].replace(";","")

        #pfam part
        ion()  #turn interactive mode on
        matches = searchPfam(uniprot_id) #query pfam with uniprot ID

        fam_dict[gene_symbol] = []
        for i in matches.keys(): #reaching the keys of dict
            fam = matches[i].get('id') #reaching every element in tuples
            fam_dict[gene_symbol].append(fam)
    return fam_dict


#Add family to each gene symbol
def add_fam(fam_dict,symbol_list):
    for k, v in fam_dict.items():
        for gene in my_genes:
            gen_symbol = re.findall(r"[\w']+", gene.name)[0] #only get the gene symbol part before the - or .
            if k == gen_symbol:
                gene.family = str(v)

    for gene in my_genes:
        print(gene.name + ": " + gene.family) #as a test here print the original gene symbol with the corresponding families.


symbol_list = gen_symbol()
fam_dict = query(fam_dict,symbol_list)
add_fam(fam_dict,symbol_list)
