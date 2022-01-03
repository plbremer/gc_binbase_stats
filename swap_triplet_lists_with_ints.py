import pandas
from pprint import pprint
import os
import sys
import itertools
import numpy as np
import multiprocessing


def swap_one_results_panda_keys(temp_panda_address_list):

    for temp_panda_address in temp_panda_address_list:    
        print(temp_panda_address)
        temp_panda=pandas.read_pickle(temp_panda_address)
        temp_panda['from_triplets']=temp_panda['from_triplets'].astype(str).replace(triplet_int_mapping_dict)
        temp_panda['to_triplets']=temp_panda['to_triplets'].astype(str).replace(triplet_int_mapping_dict)
        temp_panda.to_pickle(temp_panda_address)



if __name__=="__main__":

    min_fold_change=sys.argv[1]
    num_processes=int(sys.argv[2])
    print(num_processes)

    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_20b_swap_triplet_lists_with_ints/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_20b_swap_triplet_lists_with_ints/dummy.txt')

    #get step 19 panda
    step_19_panda_address='../results/'+str(min_fold_change)+'/step_19_prepare_count_matrix_2/count_matrix.bin'
    step_19_panda=pandas.read_pickle(step_19_panda_address)

    #put original triplets at end
    integer_list=[i for i in range(len(step_19_panda.index))]
    step_19_panda['unique_triplet_list_real']=integer_list
    step_19_panda[['unique_triplets','unique_triplet_list_real']]=step_19_panda[['unique_triplet_list_real','unique_triplets']]
    step_19_panda.to_pickle(step_19_panda_address)


    #make mapping dictionary
    triplet_int_mapping_dict={
        temp_pair[1]:temp_pair[0] for temp_pair in list(zip(step_19_panda['unique_triplets'].to_list(),step_19_panda['unique_triplet_list_real'].astype(str).to_list()))
    }

    #go to the step 17 panda and swap the triplet lists with the integer
    step_17_panda_address='../results/'+str(min_fold_change)+'/step_17_precompute_comparison_triplets/headnodes_to_triplet_list.bin'
    step_17_panda=pandas.read_pickle(step_17_panda_address)
    
    step_17_panda['from_triplets_inter_removed_if_nec']=step_17_panda['from_triplets_inter_removed_if_nec'].astype(str).replace(triplet_int_mapping_dict)
    print('step 17 swap 1 done')
    step_17_panda['to_triplets_inter_removed_if_nec']=step_17_panda['to_triplets_inter_removed_if_nec'].astype(str).replace(triplet_int_mapping_dict)
    print('step 17 swap 2 done')
    step_17_panda.to_pickle(step_17_panda_address)

    #go to the stp 18 pandas and swap the triplet lists with the integer
    table_18_base_address='../results/'+str(min_fold_change)+'/step_18_compute_fold_results/'
    simple_file_list=os.listdir(table_18_base_address)
    simple_file_list.remove('dummy.txt')
    file_list=[table_18_base_address+i for i in simple_file_list]


    chunk_size=len(file_list)//num_processes
    file_list_list=list()
    for i in range(num_processes):
        if i< num_processes-1:
            file_list_list.append(file_list[i*chunk_size:(i+1)*chunk_size])
        elif i ==(num_processes-1):
            file_list_list.append(file_list[i*chunk_size:])

    pool = multiprocessing.Pool(processes=num_processes)
    #transformed_chunks=
    pool.map(swap_one_results_panda_keys,file_list_list)
    #transform_organ_column(post_species_transform_panda)
    #recombine_chunks
    #for i in range(len(transformed_chunks)):
    #    post_species_transform_panda.iloc[transformed_chunks[i].index]=transformed_chunks[i]
    #post_species_transform_panda=pd.concat(transformed_chunks)

    pool.close()



