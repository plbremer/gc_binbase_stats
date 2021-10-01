
import pandas
import networkx as nx
import os
#we get the triplet printing function
import generate_fold_change_matrices
#so we get the visualization function and the contraction function
import prepare_species_networkx
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

##basically the design that i will use to simplify the organ hierarchy
#cut network to those nodes related to a fold branch
def remove_branches_unrelated_to_binvestigate_set(temp_nx,temp_organ_set):
    '''
    iterate over all nodes 

    if the node itself's mesh_label is not in temp_organ set, nor any of its descendents
    then we remove that node from the network
    '''

    nodes_to_remove=list()

    for i, temp_node in enumerate(temp_nx.nodes):
        
        #print(type(temp_node))
        #hold=input('check type')
        #if type(temp_node) != str:
            #print('found float')
            #hold=input('pre continue')
        #    continue
            #hold=input('post continue')
        #print(temp_node)
        temp_descendent_list=nx.algorithms.dag.descendants(temp_nx,temp_node)
        #print(temp_descendent_list)
        ###hold=input('hold')
        #descendent_mesh_label_list=[i['mesh_label'] for ]
        
        #go through all descendents. if we fail to find a mesh label in the organ set
        #then move on, implicitly not adding the temp_node to nodes_to_remove
        ##for temp_descendent in temp_descendent_list:
            #print(temp_nx.nodes[temp_descendent]['mesh_label'])
        ##    if temp_nx.nodes[temp_descendent]['mesh_label'] in temp_organ_set:
        ##        continue
        #add descendents as well as original label
        temp_mesh_label_list=[temp_nx.nodes[x]['mesh_label'] for x in temp_descendent_list]+[temp_nx.nodes[temp_node]['mesh_label']]
        ###print(temp_mesh_label_list)
        found_organ=any([element in temp_organ_set for element in temp_mesh_label_list])
        ###print(found_organ)
        if found_organ:
            continue
        #finally we check the node itself. if we still dont find anything, remove this node from the graph
        #ultimately we will find the descedents, so we let that minor inefficiency go
        ##if (temp_nx.nodes[temp_node]['mesh_label'] not in temp_organ_set):
        else:
            nodes_to_remove.append(temp_node)
        ###hold=input('hold')
        #print(temp_node)
        #hold=input('hold')
        #temp_ancestor_list=nx.algorithms.dag.ancestors(temp_nx,temp_node)
        
        #has_numerical_value_in_ancestors=False

        #for temp_ancestor in temp_ancestor_list:
        #    if type(temp_ancestor) != str:
                #print('found float')
                #hold=input('found float')
        #        has_numerical_value_in_ancestors=True
        #        break
        
        #if has_numerical_value_in_ancestors==False:
        #    nodes_to_remove.append(temp_node)

        #print(temp_ancestor_list)
        #print(nodes_to_remove)
        #print(has_numerical_value_in_ancestors)
        #print(temp_node)
        #hold=input('one iteration')

    temp_nx.remove_nodes_from(nodes_to_remove)

def remove_branches_unrelated_to_a_given_heading(temp_nx,temp_heading):
    '''
    this function was strictly for debugging
    '''
    nodes_to_remove=list()

    #print(len(temp_nx.nodes))
    #hold=input('hold')
    for i, temp_node in enumerate(temp_nx.nodes):

        temp_ancestor_list=nx.algorithms.dag.ancestors(temp_nx,temp_node)

        if (temp_heading not in temp_ancestor_list) or (temp_node != temp_heading):
            nodes_to_remove.append(temp_node)

    temp_nx.remove_nodes_from(nodes_to_remove)

    #n#x.draw(temp_nx,with_labels=True)
    #plt.show()

    pos = graphviz_layout(temp_nx, prog="dot")
    nx.draw(temp_nx, pos,with_labels=True)
    plt.show()
    
def contract_irrelevant_nodes(temp_nx,temp_binvestigate_entries_set):
    #add node to list if (its name is NOT in the species taxid panda) AND (it has <2 children)
    #when those two conditions are met, then the node's species results can be inferred as being exactly that of the child

    #the contract function takes pairs of nodes
    #we find the predeccessor dynamically because the graph changes with evey contraction 
    #binvestigate_taxid_list=temp_panda['tax_id'].astype(str).to_list()
    #print(temp_nx.nodes)
    #print(len(temp_nx.nodes))
    #hold=input('hold')
    #print(temp_binvestigate_entries_set)
    #hold=input('hold')
    #print([temp_nx.nodes[element]['mesh_label'] for element in temp_nx.nodes])
    #hold=input('hold')
    nodes_to_contract=list()

    for temp_node in temp_nx.nodes:
        if (temp_nx.nodes[temp_node]['mesh_label'] not in temp_binvestigate_entries_set) and (len(list(temp_nx.successors(temp_node)))<2) and (len(list(temp_nx.predecessors(temp_node)))!=0):
            nodes_to_contract.append(temp_node)

    #create an edge between the successor and predecessor of the node to be removed
    #then remove the node itself
    for temp_node in nodes_to_contract:
        temp_edge=temp_nx.add_edge(list(temp_nx.predecessors(temp_node))[0],list(temp_nx.successors(temp_node))[0])
        temp_nx.remove_node(temp_node)

    #remove all self loops. artifact that has no meaning
    #for temp_node in temp_nx.nodes:
    #    try:
    #        temp_nx.remove_edge(temp_node,temp_node)
    #    except nx.exception.NetworkXError:
    #        continue


if __name__ == "__main__":
    count_cutoff=10
    #probably could use the step_5 one if the "with fold matrices" version gets too massive for ram
    input_binvestigate_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_11_prepare_species_networkx/binvestigate_species_as_taxid.bin'
    input_complete_organ_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_2a_create_organ_and_disease_networkx/mesh_organ_networkx.bin'
    input_complete_disease_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_2a_create_organ_and_disease_networkx/mesh_disease_networkx.bin'
    output_organ_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_12_prepare_organ_and_disease_networkx/organ_networkx.bin'
    output_disease_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_12_prepare_organ_and_disease_networkx/disease_networkx.bin'
    os.system('mkdir -p /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_12_prepare_organ_and_disease_networkx/')
    os.system('touch /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_12_prepare_organ_and_disease_networkx/dummy.txt')



    #overall workflow
    #read in the binvestigate panda and organ/disease networkx
    #remove branches unrelated to anything
    #contract nodes that are neither explicitly listed or a branch
    
    binvestigate_panda=pandas.read_pickle(input_binvestigate_panda_address)
    organ_networkx=nx.readwrite.gpickle.read_gpickle(input_complete_organ_networkx_address)
    disease_networkx=nx.readwrite.gpickle.read_gpickle(input_complete_disease_networkx_address)


    #get the set of organs in this networkx
    organ_species_disease_triplet_list=generate_fold_change_matrices.show_all_organ_species_disease_triplets(binvestigate_panda)
    organ_set={i[0] for i in organ_species_disease_triplet_list}
    #remove branches that are totally unrelated
    remove_branches_unrelated_to_binvestigate_set(organ_networkx,organ_set)
    #visualize
    prepare_species_networkx.visualize_nodes_on_a_list(organ_networkx,organ_set,'mesh_label')
    #contract nodes
    contract_irrelevant_nodes(organ_networkx,organ_set)
    #visualize
    prepare_species_networkx.visualize_nodes_on_a_list(organ_networkx,organ_set,'mesh_label')
    #add custom connection from each head node to a master headnode
    #for custom subset
    organ_headnodes_list=['A15','A12','A04','A18']
    #organ_headnodes_list=['A01','A08','A11','A15','A12','A05','A04','A18']
    #for real entire dataset
    #organ_headnodes_list=['J01','A01','A02','A08','A13','D27','G07','E07','B01','A11','A15','J02','A12','D20','A07','A10','A03','A16','B05','A17','A14','A06','A05','A04','A09','A18','A19']
    #organ_headnode='organ'
    organ_networkx.add_node('organ',mesh_label='organ')
    temp_organ_edges=[('organ',temp_node) for temp_node in organ_headnodes_list]
    organ_networkx.add_edges_from(temp_organ_edges)
    #visualize
    prepare_species_networkx.visualize_nodes_on_a_list(organ_networkx,organ_set,'mesh_label')
   






    #get the set of diseases in this networkx
    disease_species_disease_triplet_list=generate_fold_change_matrices.show_all_organ_species_disease_triplets(binvestigate_panda)
    disease_set={i[2] for i in disease_species_disease_triplet_list}
    #remove branches that are totally unrelated
    remove_branches_unrelated_to_binvestigate_set(disease_networkx,disease_set)
    #visualize
    prepare_species_networkx.visualize_nodes_on_a_list(disease_networkx,disease_set,'mesh_label')
    #contract nodes
    contract_irrelevant_nodes(disease_networkx,disease_set)
    #visualize
    prepare_species_networkx.visualize_nodes_on_a_list(disease_networkx,disease_set,'mesh_label')
    #add a node for "no" to disease
    disease_networkx.add_node('No', mesh_label='No')
    prepare_species_networkx.visualize_nodes_on_a_list(disease_networkx,disease_set,'mesh_label')
    #disease_headnodes_list=['C06','C04','C14','C19','C08','C15','C13','C18','C16','C20','C17','C12','C10','No']
    disease_headnodes_list=['C04','C08','No']
    disease_networkx.add_node('disease',mesh_label='disease')
    temp_disease_edges=[('disease',temp_node) for temp_node in disease_headnodes_list]
    disease_networkx.add_edges_from(temp_disease_edges)
    #visualize
    prepare_species_networkx.visualize_nodes_on_a_list(disease_networkx,disease_set,'mesh_label')

    nx.readwrite.gpickle.write_gpickle(organ_networkx,output_organ_networkx_address)
    nx.readwrite.gpickle.write_gpickle(disease_networkx,output_disease_networkx_address)



    print(organ_networkx.nodes)
    print(disease_networkx.nodes)