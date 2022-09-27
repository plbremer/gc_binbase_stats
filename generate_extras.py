import sys
import os
import pandas as pd
import networkx as nx

def choose_all_bins(directory_address):
    full_list=os.listdir(directory_address)
    return full_list

def create_translation_panda_for_compounds(networkx_address,directory_address):
    
    compound_networkx=nx.read_gpickle(networkx_address)
    compound_networkx_nodes_as_str=[str(element) for element in compound_networkx.nodes]
    print(compound_networkx_nodes_as_str)
    print(compound_networkx.nodes)
    full_list=choose_all_bins(directory_address)
    compound_translation_panda=pd.DataFrame.from_dict(
        {
            'compound_identifier':[element[:-4] for i,element in enumerate(full_list)],
            'integer_representation':[i for i,element in enumerate(full_list)]
        }
    )

    bin_type=list()
    for temp_identifier in compound_translation_panda.compound_identifier.to_list():
        #print(temp_identifier)
        if temp_identifier not in compound_networkx_nodes_as_str:
            bin_type.append('unknown')
        else:
            try:
                if compound_networkx.nodes[int(temp_identifier)]['type_of_node']=='from_binvestigate':
                    bin_type.append('known')
                else:
                    bin_type.append('class')
            except ValueError:
                if compound_networkx.nodes[(temp_identifier)]['type_of_node']=='from_binvestigate':
                    bin_type.append('known')
                else:
                    bin_type.append('class')                

    compound_translation_panda['bin_type']=bin_type
    print(compound_translation_panda)
    return compound_translation_panda
    #return {element[:-4]:i for i,element in enumerate(full_list)}

def create_translation_dict_for_triplets(temp_bin_address):
    temp=pd.read_pickle(temp_bin_address)
    #print(temp.index)
    #print(temp.index[0])
    compound_translation_panda=pd.DataFrame.from_dict(
        {
            'triplet_identifier':[temp.index[i] for i in range(len(temp.index))],
            'integer_representation':[i for i in range(len(temp.index))]
        }
    )    
    return compound_translation_panda

if __name__ == "__main__":

    min_fold_change=sys.argv[1]
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_9_generate_extras_for_db_and_api/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_9_generate_extras_for_db_and_api/dummy.txt')

    #make compound translation panda
    compound_networkx_address='../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/classyfire_analysis_results.bin'
    compound_panda_directory_address='../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/all_matrices/fold_change_matrix_average'
    compound_translation_panda=create_translation_panda_for_compounds(compound_networkx_address,compound_panda_directory_address)
    compound_translation_panda.to_pickle('../results/'+str(min_fold_change)+'/step_9_generate_extras_for_db_and_api/compound_translation_panda.bin')
    print(compound_translation_panda)

    #make triplet translation panda
    any_file=os.listdir('../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/all_matrices/fold_change_matrix_average/')[0]
    triplet_translation_panda=create_translation_dict_for_triplets(
        '../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/all_matrices/fold_change_matrix_average/'+any_file
    )
    triplet_translation_panda.to_pickle('../results/'+str(min_fold_change)+'/step_9_generate_extras_for_db_and_api/triplet_translation_panda.bin')
    print(triplet_translation_panda)