import numpy as np
import pandas
import networkx as nx
from pprint import pprint
from generate_fold_change_matrices import show_all_organ_species_disease_triplets
from itertools import chain
import os

def prepare_empty_count_panda(temp_triplet_set,temp_nx):
    '''
    Receives a list of triplets and a compound nx and builds something that looks like
    trip1
    trip2
    ...
    tripn
            bin1 bin2 ... binn class1 class2 ... classn
    '''

    #generate nodes in a depth first post order
    ordered_nodelist=list(nx.algorithms.traversal.depth_first_search.dfs_postorder_nodes(temp_nx,'CHEMONTID:9999999'))
    print(ordered_nodelist)

    pandas_dict={temp_column:[ [] for i in range(len(temp_triplet_set)) ] for temp_column in ordered_nodelist}
    #pprint(pandas_dict)

    empty_dataframe=pandas.DataFrame(data=None,index=temp_triplet_set,columns=ordered_nodelist)
    #empty_dataframe=pandas.DataFrame.from_dict(pandas_dict)
    #print(empty_dataframe)
    #hold=input('empy dataframe')
    #empty_dataframe.set_index(pandas.Index(list(temp_triplet_set)),inplace=True)

    #empty_dataframe.fillna('').apply(list)
    print(empty_dataframe)
    hold=input('empy dataframe')
    return empty_dataframe



def fill_count_panda_bins(empty_panda,binvestigate_panda):
    '''
    Receives an empty panda and fills all of the bin columns

    The bin column values are within the binvestigate panda as 4 parallel lists (species organ disease count)

    We crawl through the 4 lists in parallel, for each index we create a tuple, find the location in the panda, and set it
    '''

    for temp_column in empty_panda.columns:
        #print(temp_column)
        #try:
        if 'CHEM' in str(temp_column):
            continue
        else:
            #print('in try')
            #check if we are dealing with a bin, which has integer values
            #int(temp_column)
            temp_binvestigate_row=binvestigate_panda[binvestigate_panda['id']==temp_column].index[0]
            #print(temp_binvestigate_row)
            temp_organ_list=binvestigate_panda.at[temp_binvestigate_row,'organ']
            #print(temp_organ_list) 
            temp_species_list=binvestigate_panda.at[temp_binvestigate_row,'species']
            #print(temp_species_list)
            temp_disease_list=binvestigate_panda.at[temp_binvestigate_row,'special_property_list']
            #print(temp_disease_list)
            temp_count_list=binvestigate_panda.at[temp_binvestigate_row,'count']
            #print(temp_count_list)

            temp_triplet_list=list(zip(temp_organ_list,temp_species_list,temp_disease_list))
            #print(temp_triplet_list)

            for i,temp_triplet in enumerate(temp_triplet_list):
                #empty_panda.at[temp_triplet,temp_column].append(temp_count_list[i])
                empty_panda.at[temp_triplet,temp_column]=[(temp_count_list[i])]
            #empty_panda[temp_column].fillna(list)
            #empty_panda[temp_column].replace(np.NaN,list(),inplace=True)
            empty_panda[temp_column]=[[0] if x is np.NaN else x for x in empty_panda[temp_column]]
        #print(empty_panda)

        #hold=input('end of loop')
        #except ValueError:
        #    continue
    return empty_panda


def fill_count_panda_classes(empty_panda,temp_nx):
    '''
    now that the bins are full, we can fill the panda's classes

    we can do this recursively using the traveral available from networkx

    iterate through the traversal, if it is a bin skip it, otherwise the values are the 
    '''
    ordered_nodelist=list(nx.algorithms.traversal.depth_first_search.dfs_postorder_nodes(temp_nx,'CHEMONTID:9999999'))

    for temp_node in ordered_nodelist:
        if ('CHEM' not in str(temp_node)):
            continue


        empty_panda[temp_node]=[list() for i in range(0,len(empty_panda.index))]
        #print(empty_panda[temp_node])
        #hold=input('asdf')
        
        #print(temp_node)
        temp_successors=list(temp_nx.successors(temp_node))
        #print(temp_successors)
        

        #print(empty_panda[temp_successors].values)
        #hold=input('test')
        #empty_panda[temp_node]=list(chain(empty_panda[temp_successors]))
        #print(np.concatenate(empty_panda[temp_successors].values))
        #empty_panda[temp_node]=np.concatenate(empty_panda[temp_successors].values)
        #print(empty_panda)
        #empty_panda[temp_node]=[empty_panda[temp_node]+empty_panda[i] for i in temp_successors]
        #print([empty_panda[temp_node]+empty_panda[i] for i in temp_successors])
        #print(empty_panda[temp_successors[0]])
        #empty_panda[temp_node]=[empty_panda[temp_node]+empty_panda[i] for i in temp_successors]
        for i in temp_successors:
            empty_panda[temp_node]=empty_panda[temp_node]+empty_panda[i]
        #print(empty_panda[temp_node])
        #hold=input('end of loop')

    return empty_panda

if __name__ == "__main__":

    count_cutoff=snakemake.params.count_cutoff
    os.system('mkdir -p /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_15_prepare_count_matrix/')
    os.system('touch /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_15_prepare_count_matrix/dummy.txt')
    
    
    
    input_binvestigate_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_11_prepare_species_networkx/binvestigate_species_as_taxid.bin'
    compound_nx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity/compounds_networkx.bin'
    output_address_full_count='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_15_prepare_count_matrix/full_count_matrix.bin'
    output_address_min_count='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_15_prepare_count_matrix/min_count_matrix.bin'
    output_address_sum_count='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_15_prepare_count_matrix/sum_count_matrix.bin'

    compound_nx=nx.readwrite.gpickle.read_gpickle(compound_nx_address)
    binvestigate_panda=pandas.read_pickle(input_binvestigate_panda_address)
    organ_species_disease_triplet_list=show_all_organ_species_disease_triplets(binvestigate_panda)

    #create the empty panda
    empty_panda=prepare_empty_count_panda(organ_species_disease_triplet_list,compound_nx)
    #fill the panda with the count for bins first
    fill_count_panda_bins(empty_panda,binvestigate_panda)
    #traverse through the compound networkx
    full_panda=fill_count_panda_classes(empty_panda,compound_nx)
    #extract the min panda directly from the full panda
    min_panda=full_panda.applymap(func= (lambda x: min(x)))
    #same for the sum
    sum_panda=full_panda.applymap(func= (lambda x: sum(x)))

    #output all three pandas
    full_panda.to_pickle(output_address_full_count)
    min_panda.to_pickle(output_address_min_count)
    sum_panda.to_pickle(output_address_sum_count)