import sys
import pandas
import os
import itertools

if __name__ == "__main__":


    min_fold_change=sys.argv[1]
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_23_organize_files_for_dash_app/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_23_organize_files_for_dash_app/dummy.txt')

    os.system('cp ../results/'+str(min_fold_change)+'/step_14_reduce_hierarchy_complexity_post_dash/* ../results/'+str(min_fold_change)+'/step_23_organize_files_for_dash_app/')
    os.system('cp ../results/'+str(min_fold_change)+'/step_21_convert_networkx_to_cyto_format/* ../results/'+str(min_fold_change)+'/step_23_organize_files_for_dash_app/')


    #add step 14 stuff
    os.system('cp ../results/'+str(min_fold_change)+'/step_20_build_hierarchy_filter_tables/table_species_dash.bin ../results/'+str(min_fold_change)+'/step_23_organize_files_for_dash_app/')
    os.system('cp ../results/'+str(min_fold_change)+'/step_20_build_hierarchy_filter_tables/table_organ_dash.bin ../results/'+str(min_fold_change)+'/step_23_organize_files_for_dash_app/')
    os.system('cp ../results/'+str(min_fold_change)+'/step_20_build_hierarchy_filter_tables/table_disease_dash.bin ../results/'+str(min_fold_change)+'/step_23_organize_files_for_dash_app/')

    random_fold_matrix_for_index_address='../results/'+str(min_fold_change)+'/step_13_swap_fold_matrix_multiindex/each_compounds_fold_matrix/2.bin'
    temp=pandas.read_pickle(random_fold_matrix_for_index_address)
    output_panda=temp.index.to_frame()
    index_panda=output_panda.copy()
    #output_address='../results/'+str(min_fold_change)+'/step_23_organize_files_for_dash_app/index_panda.bin'
    #output_panda.to_pickle(output_address)


    #right now the panda format iso
    #organ species disease
    #Xylem 29760 No
    #we want to replace xylem and no with their organ species hierarchy paths


    #read in the organ map panda
    #make a dict mapping where one element is like
    #'Cells': [A11, A11.188] etc
    #use pandas map on that dict
    #explode the panda
    #index_panda=pandas.read_pickle('../results/'+str(min_fold_change)+'/step_23_organize_files_for_dash_app/index_panda.bin')
    
    organ_map_panda=pandas.read_pickle('../results/'+str(min_fold_change)+'/step_20_build_hierarchy_filter_tables/table_organ_dash.bin')
    keys=set(organ_map_panda.english_name.to_list())
    organ_mapping_dict={temp_key:list() for temp_key in keys}
    zipped_list_for_values=list(zip(organ_map_panda.english_name.to_list(),organ_map_panda.node_id.to_list()))
    [organ_mapping_dict[temp_tup[0]].append(temp_tup[1]) for temp_tup in zipped_list_for_values]
    index_panda=index_panda.assign(organ=index_panda['organ'].map(organ_mapping_dict))
    index_panda=index_panda=index_panda.explode('organ')

    disease_map_panda=pandas.read_pickle('../results/'+str(min_fold_change)+'/step_20_build_hierarchy_filter_tables/table_disease_dash.bin')
    keys=set(disease_map_panda.english_name.to_list())
    disease_mapping_dict={temp_key:list() for temp_key in keys}
    zipped_list_for_values=list(zip(disease_map_panda.english_name.to_list(),disease_map_panda.node_id.to_list()))
    [disease_mapping_dict[temp_tup[0]].append(temp_tup[1]) for temp_tup in zipped_list_for_values]
    index_panda=index_panda.assign(disease=index_panda['disease'].map(disease_mapping_dict))
    index_panda=index_panda=index_panda.explode('disease')
    index_panda.to_pickle('../results/'+str(min_fold_change)+'/step_23_organize_files_for_dash_app/index_panda.bin')
    



