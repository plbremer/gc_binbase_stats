import sys
import os
import networkx as nx
import pandas as pd


def make_index_panda_for_dash_app():
    starting_point=pd.read_pickle('../results/'+str(min_fold_change)+'/step_11_organize_files_for_dash_app/sod_combo.bin')
    
    #species_networkx=nx.read_gpickle('../results/'+str(min_fold_change)+'/step_8_b_prepare_species_networkx/species_networkx.bin')
    species_mapping_panda=pd.read_pickle('../results/'+str(min_fold_change)+'/step_8_b_prepare_species_networkx/for_index_panda_for_dash_species_translation.bin')

    disease_networkx=nx.read_gpickle('../results/'+str(min_fold_change)+'/step_8_c_prepare_organ_and_disease_networkx/disease_networkx.bin')

    #species_mapping_dict={species_networkx.nodes[temp_node]['scientific_name'].lower():temp_node for temp_node in species_networkx}
    species_mapping_dict=dict(zip(species_mapping_panda.english,species_mapping_panda.ncbi_id))
    print('-'*50)
    print(species_mapping_dict)
    starting_point['species']=starting_point['species'].map(species_mapping_dict.get)

    organ_networkx=nx.read_gpickle('../results/'+str(min_fold_change)+'/step_8_c_prepare_organ_and_disease_networkx/organ_networkx.bin')
    # organ_map_panda=pd.read_pickle('../results/'+str(min_fold_change)+'/step_20_build_hierarchy_filter_tables/table_organ_dash.bin')
    keys=set()
    for temp_node in organ_networkx.nodes:
        keys.add(organ_networkx.nodes[temp_node]['mesh_label'])
    organ_mapping_dict={temp_key:list() for temp_key in keys}
    for temp_node in organ_networkx.nodes:
        organ_mapping_dict[organ_networkx.nodes[temp_node]['mesh_label']].append(temp_node)
    starting_point['organ']=starting_point['organ'].map(organ_mapping_dict.get)
    starting_point=starting_point.explode('organ')
    #keys=set(organ_map_panda.english_name.to_list())
    # organ_mapping_dict={temp_key:list() for temp_key in keys}
    # zipped_list_for_values=list(zip(organ_map_panda.english_name.to_list(),organ_map_panda.node_id.to_list()))
    # [organ_mapping_dict[temp_tup[0]].append(temp_tup[1]) for temp_tup in zipped_list_for_values]
    # index_panda=index_panda.assign(organ=index_panda['organ'].map(organ_mapping_dict))
    # index_panda=index_panda=index_panda.explode('organ')
    disease_networkx=nx.read_gpickle('../results/'+str(min_fold_change)+'/step_8_c_prepare_organ_and_disease_networkx/disease_networkx.bin')
    # disease_map_panda=pd.read_pickle('../results/'+str(min_fold_change)+'/step_20_build_hierarchy_filter_tables/table_disease_dash.bin')
    keys=set()
    for temp_node in disease_networkx.nodes:
        keys.add(disease_networkx.nodes[temp_node]['mesh_label'])
    disease_mapping_dict={temp_key:list() for temp_key in keys}
    for temp_node in disease_networkx.nodes:
        disease_mapping_dict[disease_networkx.nodes[temp_node]['mesh_label']].append(temp_node)
    starting_point['disease']=starting_point['disease'].map(disease_mapping_dict.get)
    starting_point=starting_point.explode('disease')
    # disease_map_panda=pd.read_pickle('../results/'+str(min_fold_change)+'/step_20_build_hierarchy_filter_tables/table_disease_dash.bin')
    # keys=set(disease_map_panda.english_name.to_list())
    # disease_mapping_dict={temp_key:list() for temp_key in keys}
    # zipped_list_for_values=list(zip(disease_map_panda.english_name.to_list(),disease_map_panda.node_id.to_list()))
    # [disease_mapping_dict[temp_tup[0]].append(temp_tup[1]) for temp_tup in zipped_list_for_values]
    # index_panda=index_panda.assign(disease=index_panda['disease'].map(disease_mapping_dict))
    # index_panda=index_panda=index_panda.explode('disease')
    print(starting_point)
    print(starting_point.loc[starting_point.species.isnull()==True])
    starting_point.set_index(keys=['organ','species','disease'],drop=False,inplace=True)
    
    print(starting_point)
    
    #index_panda.set_index()
    starting_point.to_pickle('../results/'+str(min_fold_change)+'/step_11_organize_files_for_dash_app/index_panda.bin')




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

    triplet_mapping_address='../results/'+str(min_fold_change)+'/step_9_generate_extras_for_db_and_api/triplet_translation_panda.bin'
    triplet_mapping_output='../results/'+str(min_fold_change)+'/step_11_organize_files_for_dash_app/triplet_translation_panda.bin' 
    # os.system(f'cp {triplet_mapping_address} {triplet_mapping_output}')

    compound_mapping_address='../results/'+str(min_fold_change)+'/step_9_generate_extras_for_db_and_api/compound_translation_panda.bin'
    compound_mapping_output='../results/'+str(min_fold_change)+'/step_11_organize_files_for_dash_app/compound_translation_panda.bin' 
    # os.system(f'cp {compound_mapping_address} {compound_mapping_output}')


    index_panda=make_index_panda_for_dash_app()



