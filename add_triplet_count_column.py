# the role of this script is to add two columns to the dataset that
# comes from the fold change analysis and goes into the dash app
# each column involves the number of triplets associated with headnode selections
# one column offers the number of potential combinations that could appear
# it is calculated as the product of the number of species, number of organs, and number of diseases
# implied by a selections
# the other column is the number of combinations that actually exist. it is calculated with
# a multi condition .loc statement

import pandas
from pprint import pprint
import os

if __name__ == "__main__":

    count_cutoff=snakemake.params.count_cutoff
    os.system('mkdir -p /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_19_add_triplet_count_column/')
    os.system('touch /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_19_add_triplet_count_column/dummy.txt')

    input_compiliation_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_18_post_user_library_make_conglomerate_panda/conglomerate_result_panda.bin'
    input_triplet_source_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_16_calculate_fraction_triplets/triplet_count_panda.bin'
    output_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_19_add_triplet_count_column/conglomerate_result_panda_triplets.bin'

    triplet_panda=pandas.read_pickle(input_triplet_source_address)
    fold_change_panda=pandas.read_pickle(input_compiliation_panda_address)

    # algorithm    
    # .loc actual triplets column on triplet panda because anything where that column is zero wont appear
    # then use map
    # to use map we create a tuple from the three headnodes by adding the columns
    # then we use that column of tuples as the key and the "actual triplets" or "possible triplets"
    # as the key

    #make a tuple column that will serve as the linker between these two pandas
    triplet_panda['triplet_tuple']=tuple(zip(triplet_panda['species_headnode'],triplet_panda['organ_headnode'],triplet_panda['disease_headnode']))
    fold_change_panda['triplet_tuple_from']=tuple(zip(fold_change_panda['species_node_from'],fold_change_panda['organ_node_from'],fold_change_panda['disease_node_from']))
    fold_change_panda['triplet_tuple_to']=tuple(zip(fold_change_panda['species_node_to'],fold_change_panda['organ_node_to'],fold_change_panda['disease_node_to']))


    #subset the triplet panda (because in the future it could be very large)
    triplet_panda_non_zero_view=triplet_panda.loc[triplet_panda['actual_triplets'] != 0]

    #make three mapping dicts to apply to our results panda
    actual_triplet_mapping_dict=dict(zip(triplet_panda_non_zero_view['triplet_tuple'],triplet_panda_non_zero_view['actual_triplets']))
    possible_triplet_mapping_dict=dict(zip(triplet_panda_non_zero_view['triplet_tuple'],triplet_panda_non_zero_view['possible_triplets']))
    ratio_triplet_mapping_dict=dict(zip(triplet_panda_non_zero_view['triplet_tuple'],triplet_panda_non_zero_view['ratio']))

    
    #apply the three mappinng dicts to both "from" and "to"
    #from
    fold_change_panda['possible_triplets_from']=fold_change_panda['triplet_tuple_from'].map(possible_triplet_mapping_dict)
    fold_change_panda['actual_triplets_from']=fold_change_panda['triplet_tuple_from'].map(actual_triplet_mapping_dict)
    fold_change_panda['ratio_from']=fold_change_panda['triplet_tuple_from'].map(ratio_triplet_mapping_dict)
    #to
    fold_change_panda['possible_triplets_to']=fold_change_panda['triplet_tuple_to'].map(possible_triplet_mapping_dict)
    fold_change_panda['actual_triplets_to']=fold_change_panda['triplet_tuple_to'].map(actual_triplet_mapping_dict)
    fold_change_panda['ratio_to']=fold_change_panda['triplet_tuple_to'].map(ratio_triplet_mapping_dict)

    print(fold_change_panda)
    #print(fold_change_panda['possible_triplets'].value_counts())

    fold_change_panda.to_pickle(output_address)

