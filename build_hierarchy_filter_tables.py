import os
import pandas
import networkx as nx
from reduce_hierarchy_complexity import create_text_for_keep_files
from generate_fold_change_matrices import show_all_organ_species_disease_triplets



def do_everything(temp_nx_address,temp_output_address,temp_hierarchy_type):

    if temp_hierarchy_type=='compound':
        
        temp_nx=nx.readwrite.gpickle.read_gpickle(temp_nx_address)
        temp_panda=create_text_for_keep_files(temp_nx,'compound')
        temp_panda.drop('english_name',inplace=True,axis='columns')

        temp_distance_list=[
            nx.algorithms.shortest_paths.generic.shortest_path_length(temp_nx,source='CHEMONTID:9999999',target=temp_panda.at[i,'node_id']) for i in temp_panda.index
        ]
        print(temp_distance_list)
        print(temp_panda)
        temp_panda['distance_from_root']=temp_distance_list
        print(temp_panda)

    elif temp_hierarchy_type=='species':

        species_set={i[1] for i in organ_species_disease_triplet_list}
        temp_nx=nx.readwrite.gpickle.read_gpickle(temp_nx_address)
        temp_panda=create_text_for_keep_files(temp_nx,'species',species_set)
        temp_panda.drop('english_name',inplace=True,axis='columns')

        temp_distance_list=[
            nx.algorithms.shortest_paths.generic.shortest_path_length(temp_nx,source='1',target=temp_panda.at[i,'node_id']) for i in temp_panda.index
        ]
        temp_panda['distance_from_root']=temp_distance_list

        print(temp_panda)


    elif temp_hierarchy_type=='organ':

        organ_set={i[0] for i in organ_species_disease_triplet_list}
        temp_nx=nx.readwrite.gpickle.read_gpickle(temp_nx_address)
        temp_panda=create_text_for_keep_files(temp_nx,'organ',organ_set)
        temp_panda.drop('english_name',inplace=True,axis='columns')

        temp_distance_list=[
            nx.algorithms.shortest_paths.generic.shortest_path_length(temp_nx,source='organ',target=temp_panda.at[i,'node_id']) for i in temp_panda.index
        ]
        temp_panda['distance_from_root']=temp_distance_list

        print(temp_panda)       

    elif temp_hierarchy_type=='disease':

        disease_set={i[2] for i in organ_species_disease_triplet_list}
        temp_nx=nx.readwrite.gpickle.read_gpickle(temp_nx_address)
        temp_panda=create_text_for_keep_files(temp_nx,'disease',disease_set)
        temp_panda.drop('english_name',inplace=True,axis='columns')

        temp_distance_list=[
            nx.algorithms.shortest_paths.generic.shortest_path_length(temp_nx,source='disease',target=temp_panda.at[i,'node_id']) for i in temp_panda.index
        ]
        temp_panda['distance_from_root']=temp_distance_list

        print(temp_panda)  



if __name__ == "__main__":


    count_cutoff=snakemake.params.count_cutoff
    os.system('mkdir -p /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_20_build_hierarchy_filter_tables/')
    os.system('touch /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_20_build_hierarchy_filter_tables/dummy.txt')


    #count_cutoff=1

    compound_nx_input_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/1/step_14_reduce_hierarchy_complexity/compounds_networkx.bin'
    species_nx_input_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity/species_networkx.bin'
    organ_nx_input_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity/organ_networkx.bin'
    disease_nx_input_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity/disease_networkx.bin'

    compound_output_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_20_build_hierarchy_filter_tables/table_compound.txt'
    species_output_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_20_build_hierarchy_filter_tables/table_species.txt'
    organ_output_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_20_build_hierarchy_filter_tables/table_organ.txt'
    disease_output_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_20_build_hierarchy_filter_tables/table_disease.txt'


    #required for species, organ, and disease
    input_binvestigate_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_11_prepare_species_networkx/binvestigate_species_as_taxid.bin'
    binvestigate_panda=pandas.read_pickle(input_binvestigate_panda_address)
    organ_species_disease_triplet_list=show_all_organ_species_disease_triplets(binvestigate_panda)

    do_everything(compound_nx_input_address,compound_output_address,'compound')
    do_everything(species_nx_input_address,species_output_address,'species')
    do_everything(organ_nx_input_address,organ_output_address,'organ')
    do_everything(disease_nx_input_address,disease_output_address,'disease')