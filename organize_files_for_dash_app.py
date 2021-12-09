import sys
import pandas
import os

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
    output_address='../results/'+str(min_fold_change)+'/step_23_organize_files_for_dash_app/index_panda.bin'
    output_panda.to_pickle(output_address)