# this script takes the three hierarchies, species organ and disease
# then, it goes through each combination of the triplets

# for each triplet combination, we assess what the possible number of triplets implied is
# the number of triplets implied is the product of
# the number of species-for-which-we-have-data times
# the number of organs-for-which-we-have-data times
# the number of diseases-for-which-we-have-data

# the number for each of these is not simply the number of leaves - metadata can be mapped
# to non-leaf nodes

# therefore, we aquire the descendants list for a node (UNIQUE descendants)
# count the total number of descendants that appear in the binvestigate triplet list
# we do this for species, organs and disease
# we do this independently for species and organs and diseases

# we assemble a list where you have every conceivable triplet of nodes
# and then put in a column wiht the product 

# then, we make another column where we
# for each triplet of nodes, get all descendants for each node
# and, instead of getting the number of species, the number of organs, the number of disease independently
# we subsequently .loc the binvestigate panda to get the actual number that we have

# then we divide the columns to get the ratio

import os
import networkx as nx
import pandas
from generate_fold_change_matrices import show_all_organ_species_disease_triplets
from reduce_hierarchy_complexity import draw_nx_for_analysis


def convert_organ_node_set_to_mesh_label_set(temp_organ_node_set,temp_organ_nx):
    '''
    note that we return a set, so this produces a UNIQUE set of labels, even if there would
    be redundancies based on the incoming path set
    '''
    temp_mesh_label_set=set()

    for temp_node in temp_organ_nx.nodes:
        if temp_node in temp_organ_node_set:
            temp_mesh_label_set.add(temp_organ_nx.nodes[temp_node]['mesh_label'])

    return temp_mesh_label_set


def convert_disease_node_set_to_mesh_label_set(temp_disease_node_set,temp_disease_nx):
    '''
    note that we return a set, so this produces a UNIQUE set of labels, even if there would
    be redundancies based on the incoming path set
    '''
    temp_mesh_label_set=set()

    for temp_node in temp_disease_nx.nodes:
        if temp_node in temp_disease_node_set:
            temp_mesh_label_set.add(temp_disease_nx.nodes[temp_node]['mesh_label'])

    return temp_mesh_label_set

def identify_nodes_to_which_we_map(temp_node_set,temp_node_type):
    '''
    '''
    #print(organ_species_disease_triplet_panda)
    #print('##########')
    #print(temp_node_set)
    #print(temp_node_type)

    unique_mapping_possibilities=set(organ_species_disease_triplet_panda[temp_node_type].unique())
    #print(unique_mapping_possibilities)
    nodes_to_which_we_map_set={temp for temp in temp_node_set if (temp in unique_mapping_possibilities)}
    #print(nodes_to_which_we_map_set)

    #hold=input('hodl')
    return nodes_to_which_we_map_set

def identify_triplets_we_have_data_for(temp_species_we_map_to,temp_organ_we_map_to,temp_disease_we_map_to):

    #print('$$$$$$$$$$$$$$')
    #print(temp_species_we_map_to)
    #print(organ_species_disease_triplet_panda['species'])
    #print(organ_species_disease_triplet_panda['species'].isin(temp_species_we_map_to))
    
    triplet_length=len(organ_species_disease_triplet_panda.loc[
        organ_species_disease_triplet_panda['species'].isin(temp_species_we_map_to) &
        organ_species_disease_triplet_panda['organ'].isin(temp_organ_we_map_to) &
        organ_species_disease_triplet_panda['disease'].isin(temp_disease_we_map_to)
    ].index)
    return triplet_length

#traverses species organ and disease nodeslist
def evaluate_headnode_combinations(temp_species_nx,temp_organ_nx,temp_disease_nx):
    '''
   
    '''
    result_panda_dict_list={
        'species_headnode':[],
        'organ_headnode':[],
        'disease_headnode':[],
        'possible_triplets':[],
        'actual_triplets':[]
    }
    #print(result_panda_dict_list)

    species_traversal_list=list(nx.algorithms.traversal.depth_first_search.dfs_postorder_nodes(temp_species_nx,source='1'))
    organ_traversal_list=list(nx.algorithms.traversal.depth_first_search.dfs_postorder_nodes(temp_organ_nx,source='organ'))
    disease_traversal_list=list(nx.algorithms.traversal.depth_first_search.dfs_postorder_nodes(temp_disease_nx,source='disease'))

    #iterate through specices
    for temp_species_headnode in species_traversal_list:

        temp_species_descendants=nx.algorithms.dag.descendants(temp_species_nx,temp_species_headnode)
        temp_species_descendants.add(temp_species_headnode)

        print(temp_species_headnode)
        #print(temp_species_descendants)

        temp_species_we_map_to=identify_nodes_to_which_we_map(temp_species_descendants,'species')
        
        for temp_organ_headnode in organ_traversal_list:

            temp_organ_descendants=nx.algorithms.dag.descendants(temp_organ_nx,temp_organ_headnode)
            temp_organ_descendants.add(temp_organ_headnode)

            #print(temp_organ_headnode)
            #print(temp_organ_descendants)

            temp_organ_descendants_mesh=convert_organ_node_set_to_mesh_label_set(temp_organ_descendants,temp_organ_nx)

            #print(temp_organ_descendants_mesh)
            
            temp_organ_we_map_to=identify_nodes_to_which_we_map(temp_organ_descendants_mesh,'organ')
            
            for temp_disease_headnode in disease_traversal_list:

                temp_disease_descendants=nx.algorithms.dag.descendants(temp_disease_nx,temp_disease_headnode)
                temp_disease_descendants.add(temp_disease_headnode)

                #print(temp_disease_headnode)
                #print(temp_disease_descendants)

                temp_disease_descendants_mesh=convert_disease_node_set_to_mesh_label_set(temp_disease_descendants,temp_disease_nx)

                #print(temp_disease_descendants_mesh)

                temp_disease_we_map_to=identify_nodes_to_which_we_map(temp_disease_descendants_mesh,'disease')
            
                #print('--------')
                #print(temp_species_we_map_to)
                #print(temp_organ_we_map_to)
                #print(temp_disease_we_map_to)
                

                temp_possibility_length=len(temp_species_we_map_to)*len(temp_organ_we_map_to)*len(temp_disease_we_map_to)

                #print(temp_possibility_length)    
                
                
                temp_actual_triplet_length=identify_triplets_we_have_data_for(
                    temp_species_we_map_to,
                    temp_organ_we_map_to,
                    temp_disease_we_map_to
                )
                
                #print(temp_species_we_map_to)
                #print(temp_organ_we_map_to)
                #print(temp_disease_we_map_to)
                #print(temp_triplets)
                
                
                result_panda_dict_list['species_headnode'].append(temp_species_headnode)
                result_panda_dict_list['organ_headnode'].append(temp_organ_headnode)
                result_panda_dict_list['disease_headnode'].append(temp_disease_headnode)
                result_panda_dict_list['possible_triplets'].append(temp_possibility_length)
                result_panda_dict_list['actual_triplets'].append(temp_actual_triplet_length)
    
    
    print(result_panda_dict_list)
    result_panda=pandas.DataFrame.from_dict(result_panda_dict_list)
    return result_panda          


                #hold=input('hold')

    





#for a given triplet, aquires all UNIQUE descendants


#idenpendently get lists of species, lists of organs, lists of diseases
#add product to panda



#filter binvestigate
#using triple loc
#add count of remaining to panda





if __name__ == "__main__":


    count_cutoff=snakemake.params.count_cutoff
    os.system('mkdir -p /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_16_calculate_fraction_triplets/')
    os.system('touch /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_16_calculate_fraction_triplets/dummy.txt')
    

    input_binvestigate_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_11_prepare_species_networkx/binvestigate_species_as_taxid.bin'
    species_nx_output_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity/species_networkx.bin'
    organ_nx_output_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity/organ_networkx.bin'
    disease_nx_output_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity/disease_networkx.bin'
    output_triplet_count_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_16_calculate_fraction_triplets/triplet_count_panda.bin'

    binvestigate_panda=pandas.read_pickle(input_binvestigate_panda_address)
    organ_species_disease_triplet_list=list(show_all_organ_species_disease_triplets(binvestigate_panda))
    organ_species_disease_triplet_panda=pandas.DataFrame(organ_species_disease_triplet_list,columns=['organ','species','disease'])

    species_nx=nx.readwrite.gpickle.read_gpickle(species_nx_output_address)
    organ_nx=nx.readwrite.gpickle.read_gpickle(organ_nx_output_address)
    disease_nx=nx.readwrite.gpickle.read_gpickle(disease_nx_output_address)


    #temp_nx,temp_hierarchy_type,set_of_binvestigate_nodes=None
    #draw_nx_for_analysis(species_nx,'species',organ_species_disease_triplet_panda['species'].unique())
    #draw_nx_for_analysis(organ_nx,'species',organ_species_disease_triplet_panda['organ'].unique())
    #draw_nx_for_analysis(disease_nx,'species',organ_species_disease_triplet_panda['disease'].unique())


    result_panda=evaluate_headnode_combinations(species_nx,organ_nx,disease_nx)
    result_panda['ratio']=result_panda['actual_triplets'].div(result_panda['possible_triplets'])
    print(result_panda)
    print(result_panda['possible_triplets'].value_counts())
    print(result_panda['actual_triplets'].value_counts())
    #make empty list-dict of triplet headnodes

    result_panda.to_pickle(output_triplet_count_panda_address)