from gecko import Gene
import csv


def open_file():
    """
    Opens a file and saves the information in a list
    :return: file_information_list: a list containing the gene names, filenames, and counts

    """
    filename = 'Merged_FPKM.tsv'
    with open(filename) as tsvfile:
        file_information_list = []
        reader = csv.reader(tsvfile, dialect='excel-tab')
        for row in reader:
            file_information_list.append(row[1:])
    return file_information_list


def create_dict(file_information_list):
    """
    Creates a list of files containing Gene objects
    :param file_information_list: a list containing the gene names, filenames, and counts
    :return: gene_list: a list containing gene objects
    """
    filenames_temp = file_information_list[0]
    file_names = filenames_temp[1:]
    gene_list = []
    gen_number = get_gennummer()
    gen_family = family()

    for i in file_information_list[1:]:
        gene_name = i[0]
        counts_list = i[1:]
        counts_dict = {}

        for index, counts in enumerate(counts_list):
            filename =file_names[index]
            counts_dict.update( {filename : counts})
        gene = Gene.Gene(gen_number, gene_name, counts_dict,gen_family)
        gen_number = gen_number + 1
        gene_list.append(gene)
    return gene_list


def main():
    file_information_list = open_file()
    gene_list = create_dict(file_information_list)
    for i in gene_list:
        print(i.name)
        print(i.number)
        print(i.counts)
    return gene_list


def get_gennummer():
    """
    get the number of genes in the database to determine the new gen_number
    :return: unique_number: the new gen number that will be used to create a new Gene object
    """
    number = 0
    unique_number = number+1
    return unique_number

def family():
    """
    Makes room in the object to add corresponding family
    :return: empty string where family can come
    """
    family = ""
    return family


main()
