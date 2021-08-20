import obonet
import matplotlib.pyplot as plt
import networkx as nx

def poke_around_networkx(temp_nx):
    #parsed_obo.add_node() to add  new nodes to graph
    #DiGraph is a special class for directed graphs (which we have)
    #networkx.drawing

    #i think that you have to add a node then add an edge

    #show that its DAG
    print(nx.is_directed_acyclic_graph(temp_nx))

    #things i want to do
    ##visualize the current network
    ###subgraph
    ###nbunch
    nx.draw(temp_nx)
    plt.show()

    #we have chosen 162 as a simple point

    #get descendants (things downstream of the graph)
    print(nx.descendants(parsed_obo,'CHEMONTID:0000162'))

    #get ancestors (things upstream, but lower in the ontology)
    print(nx.ancestors(parsed_obo,'CHEMONTID:0000162'))

    #try drawing ancestors
    ##get the set
    ##create an nbunchiterator over the set
    ##send that to the drawer
    ancestor_set=nx.ancestors(parsed_obo,'CHEMONTID:0000162')
    subgraph_parsed_obo=parsed_obo.subgraph(ancestor_set)
    nx.draw(subgraph_parsed_obo,with_labels=True)
    #this doesnt include 162 itself, so might want to get the direct parent of 162 then get th3
    #ancestors of 162's parent
    plt.show()

    ##see what attributes each node has
    ##add one node (and edge?) to the graph
    ##add one more
    ##add the proper fold matrices to each node
    ##adjust parent nodes to have the proper correspodning fold matrix and any other proper indicators
    ##i think that the best way to get around the infinity thing is to choose the lowest fold to be
    #the entry in the next parent matrix



if __name__ == "__main__":

    obo_file_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/classyfire_files/ChemOnt_2_1_tester.obo'

    #output_file_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/classyfire_files/chemont_as_networkx.txt'

    parsed_obo=obonet.read_obo(obo_file_address)

    poke_around_networkx(parsed_obo)
    #for each bin assign as a child node of the deepest node that is possible