import pandas
from ete3 import NCBITaxa
import transform_written_species_to_ncbi_species
import os
import sys



def return_taxid_panda_for_species_set(temp_species_set):
    ncbi=NCBITaxa()
    #ncbi.update_taxonomy_database()

    dict_to_make_panda={'species':list(),'tax_id':list()}

    for temp_element in temp_species_set:
        returned_dict=ncbi.get_name_translator([temp_element])

        if len(returned_dict[temp_element])>1:
            print(returned_dict)
            hold=input('check dict')

        dict_to_make_panda['species'].append(temp_element)
        dict_to_make_panda['tax_id'].append(returned_dict[temp_element][0])

    species_taxid_mapping_panda=pandas.DataFrame.from_dict(dict_to_make_panda)
    print(species_taxid_mapping_panda)
    hold=input('check output panda')

    return species_taxid_mapping_panda





if __name__=="__main__":

    min_fold_change=sys.argv[1]
    #min_fold_change=snakemake.params.min_fold_change
    #note that, unusually, we refer to a much earlier panda
    input_panda_address='../results/'+str(min_fold_change)+'/step_1_species_transformed/binvestigate_species_transformed.bin'
    output_panda_address='../results/'+str(min_fold_change)+'/step_10_create_species_taxid_mapping/species_tax_id_mapping.bin'
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_10_create_species_taxid_mapping/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_10_create_species_taxid_mapping/dummy.txt')
     
    
    
    #input_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/intermediate_step_transforms/binvestigate_species_transformed.bin'
    #species_tax_id_mapping_output_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/species_organ_maps/species_tax_id.bin'



    binvestigate_panda=pandas.read_pickle(input_panda_address)

    all_species_set=transform_written_species_to_ncbi_species.get_all_strings_in_list_across_panda_column(binvestigate_panda,'species')
    print(all_species_set)

    output_panda=return_taxid_panda_for_species_set(all_species_set)

    
    output_panda.to_pickle(output_panda_address)