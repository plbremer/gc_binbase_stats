import sys
import os
import networkx as nx
import pandas as pd

if __name__ == "__main__":

    min_fold_change=sys.argv[1]
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_11_organize_files_for_dash_app/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_11_organize_files_for_dash_app/dummy.txt')


    #add non ratio stuff
    non_ratio_dropdown_address='../results/'+str(min_fold_change)+'/step_5_b_make_non_ratio_table/unique_sod_combinations.bin'
    non_ratio_dropdown_address_output='../results/'+str(min_fold_change)+'/step_11_organize_files_for_dash_app/unique_sod_combinations.bin'    
    os.system(f'cp {non_ratio_dropdown_address} {non_ratio_dropdown_address_output}')

    #networkxs
    compound_networkx_address='../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/classyfire_analysis_results.bin'
    compound_networkx_address_output='../results/'+str(min_fold_change)+'/step_11_organize_files_for_dash_app/compounds_networkx.bin'
    #convert_networkx(compound_networkx_address,compound_networkx_address_output,True,matrices_to_compute)
    compound_networkx=nx.readwrite.read_gpickle(compound_networkx_address)
    for temp_node in compound_networkx.nodes:
        compound_networkx.nodes[temp_node].pop('signifigance_matrix_welch')
        compound_networkx.nodes[temp_node].pop('signifigance_matrix_mannwhitney')
        compound_networkx.nodes[temp_node].pop('fold_change_matrix_average')
        compound_networkx.nodes[temp_node].pop('fold_change_matrix_median')
    nx.readwrite.write_gpickle(compound_networkx,compound_networkx_address_output)

    species_networkx_address='../results/'+str(min_fold_change)+'/step_8_b_prepare_species_networkx/species_networkx.bin'
    species_networkx_address_output='../results/'+str(min_fold_change)+'/step_11_organize_files_for_dash_app/species_networkx.bin'    
    os.system(f'cp {species_networkx_address} {species_networkx_address_output}')

    organ_networkx_address='../results/'+str(min_fold_change)+'/step_8_c_prepare_organ_and_disease_networkx/organ_networkx.bin'
    organ_networkx_address_output='../results/'+str(min_fold_change)+'/step_11_organize_files_for_dash_app/organ_networkx.bin'    
    os.system(f'cp {organ_networkx_address} {organ_networkx_address_output}')

    disease_networkx_address='../results/'+str(min_fold_change)+'/step_8_c_prepare_organ_and_disease_networkx/disease_networkx.bin'
    disease_networkx_address_output='../results/'+str(min_fold_change)+'/step_11_organize_files_for_dash_app/disease_networkx.bin'    
    os.system(f'cp {disease_networkx_address} {disease_networkx_address_output}')

    #an index of a fold matrix so that we can choose subsets of S,O,D on the graphical tool
    random_fold_matrix_for_index_directory_file_list=os.listdir('../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/all_matrices/fold_change_matrix_average/')
    random_fold_matrix_for_index_address='../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/all_matrices/fold_change_matrix_average/'+random_fold_matrix_for_index_directory_file_list[0]
    temp=pd.read_pickle(random_fold_matrix_for_index_address)
    output_panda=temp.index.to_frame()
    print(output_panda)
    output_panda.to_pickle('../results/'+str(min_fold_change)+'/step_11_organize_files_for_dash_app/sod_combo.bin')
    #index_panda=output_panda.copy()