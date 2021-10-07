import obonet
import matplotlib.pyplot as plt
import networkx as nx
import pandas
import numpy as np
import os
'''
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

    #show node attributes
    print(temp_nx.nodes['CHEMONTID:0000162'])

    ##see what attributes each node has
    ##add one node (and edge?) to the graph
    ##add one more
    ##add the proper fold matrices to each node
    ##adjust parent nodes to have the proper correspodning fold matrix and any other proper indicators
    ##i think that the best way to get around the infinity thing is to choose the lowest fold to be
    #the entry in the next parent matrix
'''

def obtain_deepest_classyfire_class_per_bin(temp_panda):
    '''
    we want to obtain the deepest class possible for each bin to append each bin
    to the classyfire network

    so we scroll through each bin's class listing, starting with the deepest
    and if one is not null, then we set that value to the deepest class column
    '''
    
    temp_panda['deepest_class']='pre_analysis'

    class_list=[
        'direct_parent_5',
        'direct_parent_4',
        'direct_parent_3',
        'direct_parent_2',
        'direct_parent_1',
        'subclass',
        'class',
        'superclass',
        'kingdom'
    ]

    for index, series in temp_panda.iterrows():
        for temp_column in class_list:
            ##only nan is not equal to itself
            if series[temp_column] == series[temp_column]:
                temp_panda.at[index,'deepest_class']=series[temp_column]
                break

def make_class_to_node_name_dict(temp_nx):
    #get all node names
    #put in list
    #for each node name
    #declare the value to be that node's name and the key to be the name
    #because we get the classes (names) from classyfire
    node_name_list=list(temp_nx.nodes)
    class_to_node_dict=dict()
    for temp_node_name in node_name_list:
        class_to_node_dict[temp_nx.nodes[temp_node_name]['name']]=temp_node_name

    return class_to_node_dict

def add_one_node_to_classyfire_network(temp_nx,temp_bin,temp_class_to_node_dict):
    '''

    '''
    #get the class to use as the key for the class:node_name dict
    current_bin_name=temp_bin['deepest_class']

    #get the name of the node that this bin will connect to
    node_to_connect_to=temp_class_to_node_dict[current_bin_name]

    #hold=input('first prints')
    #add this bin as a node in the network
    #the id number is the name of the node
    temp_nx.add_node(
        int(temp_bin['id']),
        inchikey=temp_bin['inchikey'],
        fold_change_matrix=temp_bin['fold_change_matrix'],
        type_of_node='from_binvestigate',
        common_name=temp_bin['name']
    )

    #add a connection between the added node and the class that it is most specifically
    #identified as
    temp_nx.add_edge(temp_bin['id'],node_to_connect_to,'is_a')

def add_all_bins_to_network(temp_nx,temp_panda,temp_class_to_node_dict):
    for index,series in temp_panda.iterrows():
        print(index)
        add_one_node_to_classyfire_network(temp_nx,series,temp_class_to_node_dict)

def visualize_added_classes(temp_nx,temp_original_classyfire_nodecount):
    #add_one_node_to_classyfire_network(parsed_obo,binvestigate_panda.loc[0],class_to_node_dict)
    color_list_original=['#1f78b4' for i in range(0,temp_original_classyfire_nodecount)]
    color_list_new=['#32cd32' for i in range(0,len(temp_nx.nodes)-temp_original_classyfire_nodecount)]
    total_color_list=color_list_original+color_list_new
    nx.draw(temp_nx,with_labels=True,node_color=total_color_list,node_size=50)
    plt.show()    
    


if __name__ == "__main__":
    #count_cutoff=10
    count_cutoff=snakemake.params.count_cutoff
    obo_file_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/classyfire_files/ChemOnt_2_1.obo'
    binvestigate_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_6_generate_fold_matrices/binvestigate_with_fold_matrices.bin'
    output_file_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_7_prepare_compound_hierarchy/classyfire_ont_with_bins_added.bin'
    os.system('mkdir -p /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_7_prepare_compound_hierarchy/')
    os.system('touch /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_7_prepare_compound_hierarchy/dummy.txt')

    parsed_obo=obonet.read_obo(obo_file_address)

    binvestigate_panda=pandas.read_pickle(binvestigate_panda_address)

    #get dict 
    #for this dict, the keys are the classes and the values are the chemontid
    #in this way, we use the cfb tool to get the classes for all inchikeys
    #and get the nodes that they connect to with this dict
    class_to_node_dict=make_class_to_node_name_dict(parsed_obo)
    print(class_to_node_dict)
    hold=input('dict')

    #make a column with the deepest classyfire class possible - in this way we can 
    #find the class to use on the above dict 
    obtain_deepest_classyfire_class_per_bin(binvestigate_panda)

    #draw the network before adding the single node
    print(len(parsed_obo.nodes))
    original_classyfire_node_count=len(parsed_obo.nodes)
    #draw classyfire with no adjustments or anything
    #nx.draw(parsed_obo,node_color=['#1f78b4' for i in range(0,len(parsed_obo.nodes))],node_size=50)
    #plt.show()

    '''
    add_one_node_to_classyfire_network(parsed_obo,binvestigate_panda.loc[0],class_to_node_dict)
    color_list=['#1f78b4' for i in range(0,len(parsed_obo.nodes)-1)]
    color_list.append('#32cd32')
    nx.draw(parsed_obo,with_labels=True,node_color=color_list)
    plt.show()    
    '''

    add_all_bins_to_network(parsed_obo,binvestigate_panda,class_to_node_dict)
    #for each bin assign as a child node of the deepest node that is possible

    #visualize_added_classes(parsed_obo,original_classyfire_node_count)
    nx.readwrite.gpickle.write_gpickle(parsed_obo,output_file_address)
