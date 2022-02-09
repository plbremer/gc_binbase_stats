import networkx as nx
from pprint import pprint
import json
import os
import sys

def convert_networkx(temp_input_address,temp_output_address,temp_is_compound_nx,matrices_to_compute):
    '''
    takes a networkx and outputs it in json format (nested dicitonaries)
    This is so that cytoscape can take these and use them for buttons for subset selections

    if the nx is the compound network, we delete the fold matrices to save memory
    '''
    temp_networkx=nx.readwrite.gpickle.read_gpickle(temp_input_address)

    if temp_is_compound_nx:
        #temp_networkx=nx.DiGraph.reverse(temp_networkx)
        for temp_node in temp_networkx.nodes:
            #plb 2-8-2022
            for temp_matrix_type in matrices_to_compute:
                del temp_networkx.nodes[temp_node][temp_matrix_type]

    my_output=nx.readwrite.json_graph.cytoscape_data(temp_networkx)

    with open(temp_output_address,'w') as temp_file:
        json.dump(my_output,temp_file)    

if __name__ == "__main__":


    matrices_to_compute=[
        'fold_change_matrix_average',
        'fold_change_matrix_median',
        'signifigance_matrix_mannwhitney',
        'signifigance_matrix_welch'
    ]

    min_fold_change=sys.argv[1]
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_21_convert_networkx_to_cyto_format/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_21_convert_networkx_to_cyto_format/dummy.txt')



    compound_networkx_address='../results/'+str(min_fold_change)+'/step_14_reduce_hierarchy_complexity_post_dash/compounds_networkx.bin'
    compound_networkx_address_output='../results/'+str(min_fold_change)+'/step_21_convert_networkx_to_cyto_format/cyto_format_compound.json'
    convert_networkx(compound_networkx_address,compound_networkx_address_output,True,matrices_to_compute)
    
    species_networkx_address='../results/'+str(min_fold_change)+'/step_14_reduce_hierarchy_complexity_post_dash/species_networkx.bin'
    species_networkx_address_output='../results/'+str(min_fold_change)+'/step_21_convert_networkx_to_cyto_format/cyto_format_species.json'
    convert_networkx(species_networkx_address,species_networkx_address_output,False,matrices_to_compute)

    organ_networkx_address='../results/'+str(min_fold_change)+'/step_14_reduce_hierarchy_complexity_post_dash/organ_networkx.bin'
    organ_networkx_address_output='../results/'+str(min_fold_change)+'/step_21_convert_networkx_to_cyto_format/cyto_format_organ.json'
    convert_networkx(organ_networkx_address,organ_networkx_address_output,False,matrices_to_compute)

    disease_networkx_address='../results/'+str(min_fold_change)+'/step_14_reduce_hierarchy_complexity_post_dash/disease_networkx.bin'
    disease_networkx_address_output='../results/'+str(min_fold_change)+'/step_21_convert_networkx_to_cyto_format/cyto_format_disease.json'
    convert_networkx(disease_networkx_address,disease_networkx_address_output,False,matrices_to_compute)    
    

    
    '''
    print(compound_networkx)
    for temp_node in compound_networkx.nodes:
        print(compound_networkx.nodes[temp_node].keys())
        #print(temp_node)
        del compound_networkx.nodes[temp_node]['fold_change_matrix']

    
    my_output=nx.readwrite.json_graph.cytoscape_data(compound_networkx)
    
    print(type(my_output))
    
    for temp_key in my_output['elements'].keys():
        print(my_output['elements'][temp_key])
        print(temp_key)
        hold=input('hold')
    #pprint(my_output)
    print(my_output.keys())
    pprint(my_output)

    with open(compound_networkx_address_output,'w') as temp_file:
        json.dump(my_output,temp_file)
    '''
