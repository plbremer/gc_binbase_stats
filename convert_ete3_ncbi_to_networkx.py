#use the gc_binbase_3_point_6 environment

from Bio import Phylo
import networkx
from ete3 import NCBITaxa
from ete3 import Tree


if __name__ == "__main__":

    ncbi_newick_output_location='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/intermediate_step_transforms/ncbi_as_newick.txt'
    ncbi=NCBITaxa()
    #ncbi.update_taxonomy_database()

    print(ncbi)
    #ncbi.write(format=1, outfile=ncbi_newick_output_location)

    #temp_tree=Tree()
    #temp_tree.annotate_tree()
    ##ncbi.annotate_tree(temp_tree,taxid_attr='name')

    #print(temp_tree)
    ##temp_tree.write(format=1, outfile=ncbi_newick_output_location)

    #get the species from the conversion file

    #fetch the numbers from the species
    
    #getch the topology of the numbers with get_topology
    #temp_tree=ncbi.get_topology([9598,9606],intermediate_nodes=True)
    temp_tree=ncbi.get_topology([3648,9606])
    print(temp_tree.get_ascii(attributes=["sci_name"]))

    ncbi.annotate_tree(temp_tree,taxid_attr="name")
    temp_tree.write(format=1, outfile=ncbi_newick_output_location)

    from ete3 import PhyloTree
    tree = PhyloTree('((9606, 9598), 10090);', sp_naming_function=lambda name: name)
    tax2names, tax2lineages, tax2rank = tree.annotate_ncbi_taxa()
    tree.write(format=1, outfile=ncbi_newick_output_location)