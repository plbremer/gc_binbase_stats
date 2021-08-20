import pandas
from pprint import pprint
import os
                                        
def rewrite_one_fold_matrix_multiindex(temp_input_address,temp_output_address,translation_panda):
    '''
    we go through the entire multiindex, adding a new tuple for each one

    we then replace the entire mutliindex index and multiindex column with that list
    '''
    
    fold_matrix=pandas.read_pickle(temp_input_address)
    species_taxid_dict={series['species']:str(series['tax_id']) for index,series in translation_panda.iterrows()}
    #temporarily written to swap int to string
    #species_taxid_dict={series['tax_id']:str(series['tax_id']) for index,series in temp_swap_panda.iterrows()}
    
    ##pprint(species_taxid_dict)


    index_list=list()
    for temp_index in fold_matrix.index:
        #if temp_index[1] in species_taxid_dict.keys():
        #    hold=input('hold')
            #new_species=
        index_list.append((temp_index[0],species_taxid_dict[temp_index[1]],temp_index[2]))

    #pprint(index_list)

    fold_matrix.index=pandas.MultiIndex.from_tuples(tuples=index_list,sortorder=None,names=['organ','species','disease'])
    fold_matrix.columns=fold_matrix.index

    #print(fold_matrix)
    #my_MultiIndex=pandas.MultiIndex.from_tuples(tuples=temp_organ_species_tuple_list,sortorder=None,names=['organ','species'])
    
    fold_matrix.to_pickle(temp_output_address)


if __name__ == "__main__":

    #test='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_8_perform_compound_hierarchical_analysis/each_compounds_fold_matrix/all_fold_matrices/2.bin'
    #swap_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_10_create_species_taxid_mapping/species_tax_id_mapping.bin'
    #temp_swap_panda=pandas.read_pickle(swap_panda_address)
    #rewrite_one_fold_matrix_multiindex(test,temp_swap_panda)

    count_cutoff=10
    input_base_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_8_perform_compound_hierarchical_analysis/each_compounds_fold_matrix/all_fold_matrices/'
    #input_binvestigate_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_11_prepare_species_networkx/binvestigate_species_as_taxid.bin'
    #input_complete_organ_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_2a_create_organ_and_disease_networkx/mesh_organ_networkx.bin'
    #input_complete_disease_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_2a_create_organ_and_disease_networkx/mesh_disease_networkx.bin'
    #output_organ_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_12_prepare_organ_and_disease_networkx/organ_networkx.bin'
    #output_disease_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_12_prepare_organ_and_disease_networkx/disease_networkx.bin'
    output_base_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_13_swap_fold_matrix_multiindex/each_compounds_fold_matrix/'
    os.system('mkdir -p /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_13_swap_fold_matrix_multiindex/each_compounds_fold_matrix/')
    os.system('touch /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_13_swap_fold_matrix_multiindex/dummy.txt')

    
    translation_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_10_create_species_taxid_mapping/species_tax_id_mapping.bin'
    translation_panda=pandas.read_pickle(translation_panda_address)

    for i,temp_file in enumerate(os.listdir(input_base_address)):
        print(i)
        #temp_compound=temp_file.split('/')[-1]
        #print(temp_compound)
        temp_input_address=input_base_address+temp_file
        temp_output_address=output_base_address+temp_file
        rewrite_one_fold_matrix_multiindex(temp_input_address,temp_output_address,translation_panda)