'''
the point of this script is to create properties associated with species, organs or disease
right now, the main point of this seems to be translating the encoded nodes into english

'''

from email.mime import base
import pandas as pd
import networkx as nx
import sys
import os
from pprint import pprint

def build_base_panda(resource_address):
    '''
    strategy is to look at the resource we create from the dash app
    '''
    base_panda=pd.read_csv(resource_address)
    base_panda.rename(columns={"nodes_to_keep":"identifier"},inplace=True)
    base_panda.set_index('identifier',drop=False,inplace=True)
    return base_panda

def get_one_name(temp_row,temp_nx,hierarchy_type):
    '''
    given a row in our compound table, get the english name
    the classyfire OBO stored names in 'name' and we stored our names in 'common_name'
    '''
    #print('hi')
    #print(temp_row)
    #pprint(temp_nx.nodes[temp_row['identifier']])
    # if 'CHEMONTID' in temp_row['identifier']:
    #     return temp_nx.nodes[temp_row['identifier']]['name']
    # else:
    #     return temp_nx.nodes[int(temp_row['identifier'])]['common_name']
    if hierarchy_type=='compound':
        if 'CHEMONTID' in temp_row['identifier']:
            return temp_nx.nodes[temp_row['identifier']]['name']
        else:
            #return temp_nx.nodes[int(temp_row['identifier'])]['common_name']      
            #     ##################################################################################
            #temporarily here for testing - leaves us with only 1 compound
            try:
                return temp_nx.nodes[int(temp_row['identifier'])]['common_name']
            except KeyError:
                return 'we_didnt_keep_this_compound'
            ##################################################################################  
    elif hierarchy_type=='species':
        return temp_nx.nodes[str(temp_row['identifier'])]['scientific_name']
    elif hierarchy_type=='organ':
        return temp_nx.nodes[temp_row['identifier']]['mesh_label']
    elif hierarchy_type=='disease':
        return temp_nx.nodes[temp_row['identifier']]['mesh_label']

def determine_english_names(temp_panda,networkx_address,hierarchy_type):
    '''
    strategy is to take the classyfire networkx
    '''
    temp_nx=nx.readwrite.gpickle.read_gpickle(networkx_address)
    temp_panda['english_name']=temp_panda.apply(get_one_name,args=(temp_nx,hierarchy_type),axis='columns')
    return temp_panda


if __name__ == "__main__":

    min_fold_change=0
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_21_b_create_compound_sod_property_tables/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_21_b_create_compound_sod_property_tables/dummy.txt')

    hierarchy_type='compound'
    resource_address='../resources/species_organ_maps/networkx_shrink_compound.txt'
    networkx_address='../results/'+str(min_fold_change)+'/step_7_prepare_compound_hierarchy/classyfire_ont_with_bins_added.bin'
    output_address='../results/'+str(min_fold_change)+'/step_21_b_create_compound_sod_property_tables/compound_property_table.bin'
    base_panda=build_base_panda(resource_address)
    #print(base_panda)
    base_panda=determine_english_names(base_panda,networkx_address,hierarchy_type)
    print(base_panda)
    base_panda.to_pickle(output_address)

    hierarchy_type='species'
    resource_address='../resources/species_organ_maps/networkx_shrink_species.txt'
    networkx_address='../results/'+str(min_fold_change)+'/step_14_reduce_hierarchy_complexity_post_dash/species_networkx.bin'
    output_address='../results/'+str(min_fold_change)+'/step_21_b_create_compound_sod_property_tables/species_property_table.bin'
    base_panda=build_base_panda(resource_address)
    #print(base_panda)
    base_panda=determine_english_names(base_panda,networkx_address,hierarchy_type)
    print(base_panda)
    base_panda.to_pickle(output_address)


    hierarchy_type='organ'
    resource_address='../resources/species_organ_maps/networkx_shrink_organ.txt'
    networkx_address='../results/'+str(min_fold_change)+'/step_14_reduce_hierarchy_complexity_post_dash/organ_networkx.bin'
    output_address='../results/'+str(min_fold_change)+'/step_21_b_create_compound_sod_property_tables/organ_property_table.bin'
    base_panda=build_base_panda(resource_address)
    #print(base_panda)
    base_panda=determine_english_names(base_panda,networkx_address,hierarchy_type)
    print(base_panda)
    base_panda.to_pickle(output_address)

    hierarchy_type='disease'
    resource_address='../resources/species_organ_maps/networkx_shrink_disease.txt'
    networkx_address='../results/'+str(min_fold_change)+'/step_14_reduce_hierarchy_complexity_post_dash/disease_networkx.bin'
    output_address='../results/'+str(min_fold_change)+'/step_21_b_create_compound_sod_property_tables/disease_property_table.bin'
    base_panda=build_base_panda(resource_address)
    #print(base_panda)
    base_panda=determine_english_names(base_panda,networkx_address,hierarchy_type)
    print(base_panda)
    base_panda.to_pickle(output_address)