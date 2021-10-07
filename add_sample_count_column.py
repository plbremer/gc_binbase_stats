



import pandas
from pprint import pprint
import os

def convert_mapping_panda_to_columns(temp_panda):
    temp_panda=temp_panda.stack()
    
    print(temp_panda)
    print(temp_panda.columns)

    return temp_panda
    

if __name__ == "__main__":

    #count_cutoff=snakemake.params.count_cutoff
    #os.system('mkdir -p /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_19_add_triplet_count_column/')
    #os.system('touch /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_19_add_triplet_count_column/dummy.txt')

    input_result_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/1/step_19_add_triplet_count_column/conglomerate_result_panda_triplets.bin'
    result_panda=pandas.read_pickle(input_result_panda_address)

    input_mapping_min_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/1/step_15_prepare_count_matrix/min_count_matrix.bin'
    mapping_panda_min=pandas.read_pickle(input_mapping_min_panda_address)
    mapping_series_min=convert_mapping_panda_to_columns(mapping_panda_min)
    mapping_dict_min=dict(zip(mapping_panda_min.index,mapping_dict_min.values))


