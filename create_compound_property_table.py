'''
the point of this script is to create properties associated with compounds
compounds can be two things - actual bins themselves or classyfire classes
compounds can have a lot of properties
obvious ones are
-english name
-(un)identified
-is bin/is class
-various IDs

'''
import pandas as pd
import networkx as nx
import sys
import os

def build_base_panda(resource_address):
    '''
    strategy is to look at the resource we create from the dash app
    '''
    base_panda=pd.read_csv(resource_address)
    base_panda.rename(columns={"nodes_to_keep":"identifier"},inplace=True)
    base_panda.set_index('identifier',drop=False,inplace=True)
    return base_panda

def get_one_name(temp_row,temp_nx):
    '''
    given a row in our compound table, get the english name
    the classyfire OBO stored names in 'name' and we stored our names in 'common_name'
    '''
    print('hi')
    print(temp_row)
    if 'CHEMONTID' in temp_row['identifier']:
        return temp_nx.nodes[temp_row['identifier']]['name']
    else:
        return temp_nx.nodes[int(temp_row['identifier'])]['common_name']

def determine_english_names(temp_panda,classyfire_networkx_address):
    '''
    strategy is to take the classyfire networkx
    '''
    temp_classyfire_nx=nx.readwrite.gpickle.read_gpickle(classyfire_networkx_address)
    temp_panda['english_name']=temp_panda.apply(get_one_name,args=(temp_classyfire_nx,),axis='columns')
    return temp_panda

# def determine_compound_names():
#     '''
#     strategy is to take from the binvestigate tool
#     '''
#     pass

if __name__ == "__main__":

    min_fold_change=0
    # min_fold_change=sys.argv[1]
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_21_b_create_compound_property_table/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_21_b_create_compound_property_table/dummy.txt')

    all_compounds_resource_address='../resources/species_organ_maps/networkx_shrink_compound.txt'
    classyfire_networkx_address='../results/'+str(min_fold_change)+'/step_7_prepare_compound_hierarchy/classyfire_ont_with_bins_added.bin'
    output_address='../results/'+str(min_fold_change)+'/step_21_b_create_compound_property_table/compound_property_table.bin'


    base_panda=build_base_panda(all_compounds_resource_address)
    base_panda=determine_english_names(base_panda,classyfire_networkx_address)


    #base_panda.drop('identifier',axis='columns',inplace=True)
    base_panda.to_pickle(output_address)
    print(base_panda)