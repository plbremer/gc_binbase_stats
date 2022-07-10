import pandas
from pprint import pprint
import os
import sys
import itertools
import numpy as np
import multiprocessing


# def chunks(lst, n):
#     """Yield successive n-sized chunks from lst."""
#     for i in range(0, len(lst), n):
#         yield lst[i:i + n]

def swap_one_results_panda_keys(temp_panda_address_list):

    for temp_panda_address in temp_panda_address_list:    
        print(temp_panda_address)
        temp_panda=pandas.read_pickle(temp_panda_address)
        #temp_panda['from_triplets']=temp_panda['from_triplets'].astype(str).replace(triplet_int_mapping_dict)
        #temp_panda['to_triplets']=temp_panda['to_triplets'].astype(str).replace(triplet_int_mapping_dict)
        temp_panda['from_triplets']=temp_panda['from_triplets'].astype(str).map(triplet_int_mapping_dict.get)
        temp_panda['to_triplets']=temp_panda['to_triplets'].astype(str).map(triplet_int_mapping_dict.get)
        temp_panda.to_pickle(temp_panda_address)



if __name__=="__main__":

    matrices_to_compute=[
        'fold_change_matrix_average',
        'fold_change_matrix_median',
        'signifigance_matrix_mannwhitney',
        'signifigance_matrix_welch'
    ]


    #hold=input('step 20b hold')
    min_fold_change=sys.argv[1]
    num_processes=4 ##int(sys.argv[2])
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

    print(triplet_int_mapping_dict)
    hold=input('mapping dict')

    #go to the step 17 panda and swap the triplet lists with the integer
    step_17_panda_address='../results/'+str(min_fold_change)+'/step_17_precompute_comparison_triplets/headnodes_to_triplet_list.bin'
    step_17_panda=pandas.read_pickle(step_17_panda_address)
    
    print('we got here')
    #hold=input('hold')

    #plb 7-10 
    #replacing on the 55 million row pandas was killing my memory.
    #so we go with a cheesy strategy of breaking the panda into 10 chunks, make a copy of each, replace on each, then concatenate
    # step_17_panda['from_triplets_inter_removed_if_nec']=step_17_panda['from_triplets_inter_removed_if_nec'].astype(str).replace(triplet_int_mapping_dict)
    # print('step 17 swap 1 done')
    # step_17_panda['to_triplets_inter_removed_if_nec']=step_17_panda['to_triplets_inter_removed_if_nec'].astype(str).replace(triplet_int_mapping_dict)
    # print('step 17 swap 2 done')
    # step_17_panda.to_pickle(step_17_panda_address)

    # step_17_slice_list=list(chunks(
    #     range(len(step_17_panda.index)), len(step_17_panda.index)//10
    # ))
    # step_17_panda_list=[
    #     #what  aconvoluted mess
    #     step_17_panda.loc[step_17_slice_list[0][i][0]:step_17_slice_list[0][i][-1],:].copy() for i in range(step_17_slice_list)
    #     #step_17_panda.loc[step_17_slice_list[0][i],:].copy() for i in range(step_17_slice_list)
    # ]
    #n = len(step_17_panda.index)//1000000  #chunk row size
    #step_17_panda_list= [step_17_panda[i:i+n].copy() for i in range(0,step_17_panda.shape[0],n)]
    # step_17_panda_list=list()
    # for i in range(0,step_17_panda.shape[0],n):
    #     print(i)
    #     step_17_panda_list.append(step_17_panda[i:i+n].copy())
    step_17_panda_list=np.array_split(step_17_panda,10)


    del step_17_panda
    for i in step_17_panda_list:
        print(i)
        # i['from_triplets_inter_removed_if_nec']=i['from_triplets_inter_removed_if_nec'].astype(str).replace(triplet_int_mapping_dict)
        # i['to_triplets_inter_removed_if_nec']=i['to_triplets_inter_removed_if_nec'].astype(str).replace(triplet_int_mapping_dict)
        # print('both swaps done for a chunk')
        # series = series.map(dictionary.get)
        i['from_triplets_inter_removed_if_nec']=i['from_triplets_inter_removed_if_nec'].astype(str).map(triplet_int_mapping_dict.get)
        i['to_triplets_inter_removed_if_nec']=i['to_triplets_inter_removed_if_nec'].astype(str).map(triplet_int_mapping_dict.get)
        print(i)
        print('both swaps done for a chunk')

        
    step_17_panda=pandas.concat(
        step_17_panda_list,
        axis='index',
        ignore_index=True
    )
    step_17_panda.to_pickle(step_17_panda_address)








    #go to the stp 18 pandas and swap the triplet lists with the integer
    
    for temp_matrix_type in matrices_to_compute:
        table_18_base_address='../results/'+str(min_fold_change)+'/step_18_compute_fold_results/all_matrices/'+temp_matrix_type+'/'
        simple_file_list=os.listdir(table_18_base_address)
        print(simple_file_list)
        hold=input('hold')
        #since multiple matrix types, we no longer put in same directory as dummy
        #simple_file_list.remove('dummy.txt')
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



