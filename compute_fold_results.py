import numpy as np
import pandas
import time
import os
import sys
import multiprocessing
from itertools import repeat

def extract_from_and_to_sets(temp_panda):
    from_list=temp_panda.loc[temp_panda['from_to']=='from']['triplets'].to_list()
    to_list=temp_panda.loc[temp_panda['from_to']=='to']['triplets'].to_list()

    return from_list,to_list

def one_df_transform_fold(temp_df):
    '''
    given an numpy array, chooses what the aggregate value is
    '''
    conditions=[
        #np.isnan(temp_df).any(),
        #(temp_df==np.inf).all(),
        #(temp_df==-np.inf).all(),
        (temp_df<0).any() and (temp_df>0).any(),
        #(temp_df==0).any(),
        (temp_df>0).all(),
        (temp_df<0).all()
    ]
    
    choices=[
        #np.nan,
        #np.inf,
        #-np.inf,
        0,
        #0,
        temp_df.min(),
        temp_df.max()
    ]
    return float(np.select(conditions,choices))


def one_df_transform_sig(temp_df):
    '''
    given an numpy array, chooses what the aggregate value is
    '''
    conditions=[
        #np.isnan(temp_df).any(),
        #(temp_df==np.inf).all(),
        #(temp_df==-np.inf).all(),
        #(temp_df<0).any() and (temp_df>0).any(),
        #(temp_df==0).any(),
        (temp_df>0).all()
        #(temp_df<0).all()
    ]
    
    choices=[
        #np.nan,
        #np.inf,
        #-np.inf,
        #0,
        #0,
        #temp_df.min(),
        temp_df.max()
    ]
    return float(np.select(conditions,choices))

def prepare_list_of_results(temp_triplet_panda,temp_fold_panda,temp_matrix_type):

    from_list=temp_triplet_panda['from'].to_list()
    to_list=temp_triplet_panda['to'].to_list()
    temp_results_list=list()
    current_from_triplets=from_list[0]
    temp_view=temp_fold_panda.loc[temp_fold_panda.index.isin(current_from_triplets),:]

    if 'fold' in temp_matrix_type:
        for i in range(len(from_list)):
            if (from_list[i] != current_from_triplets):
                current_from_triplets=from_list[i]
                temp_view=temp_fold_panda.loc[temp_fold_panda.index.isin(current_from_triplets),:]
            temp_temp_view=temp_view.loc[:,temp_fold_panda.columns.isin(to_list[i])]
            temp_results_list.append(one_df_transform_fold(temp_temp_view.values))
    elif 'signifigance' in temp_matrix_type:
        for i in range(len(from_list)):
            if (from_list[i] != current_from_triplets):
                current_from_triplets=from_list[i]
                temp_view=temp_fold_panda.loc[temp_fold_panda.index.isin(current_from_triplets),:]
            temp_temp_view=temp_view.loc[:,temp_fold_panda.columns.isin(to_list[i])]
            temp_results_list.append(one_df_transform_sig(temp_temp_view.values))

    return temp_results_list


def perform_fold_analysis(temp_file_list,temp_matrix_type):
    for temp_file in temp_file_list:
        start_time=time.time()
        
        #put here because we rename columns at the end of the loop
        triplet_panda=pandas.read_pickle(input_triplet_panda_address)
        
        input_panda_address=input_base_address+temp_file
        input_panda=pandas.read_pickle(input_panda_address)
        output_address=output_base_address+'calc_results_'+temp_file

        results_list=prepare_list_of_results(triplet_panda,input_panda,temp_matrix_type)
        triplet_panda['results']=results_list
        #print(triplet_panda)
        #print(triplet_panda['results'].value_counts())
        
        #print(temp_file[:-4])
        compound_name=temp_file[:-4]
        triplet_panda['compound']=[compound_name for i in range(len(triplet_panda.index))]
        #print(triplet_panda)
        #hold=input('hold')
        
        triplet_panda=triplet_panda.reindex(
            columns=['from','to','compound','results'],
        )

        #print(triplet_panda)
        triplet_panda=triplet_panda.rename(
            columns={
                'from':'from_triplets',
                'to':'to_triplets'
            }#,
            #inplace=True,
            #axis='columns'
        )
        #print(triplet_panda)
        triplet_panda.to_pickle(output_address)
        end_time=time.time()
        print(end_time-start_time)



if __name__ == "__main__":

    hold=input('step 18 hold')
    min_fold_change=sys.argv[1]
    num_processes=int(sys.argv[2])



    os.system('touch ../results/'+str(min_fold_change)+'/step_18_compute_fold_results/dummy.txt')

    input_triplet_panda_address='../results/'+str(min_fold_change)+'/step_17_precompute_comparison_triplets/unique_triplets.bin'


    matrices_to_compute=[
        'fold_change_matrix_average',
        'fold_change_matrix_median',
        'signifigance_matrix_mannwhitney',
        'signifigance_matrix_welch'
    ]


    for temp_matrix_type in matrices_to_compute:
        print(temp_matrix_type)

        os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_18_compute_fold_results/all_matrices/'+temp_matrix_type+'/')
        input_base_address='../results/'+str(min_fold_change)+'/step_13_swap_fold_matrix_multiindex/all_matrices/'+temp_matrix_type+'/'
        output_base_address='../results/'+str(min_fold_change)+'/step_18_compute_fold_results/all_matrices/'+temp_matrix_type+'/'
        file_list=os.listdir('../results/'+str(min_fold_change)+'/step_13_swap_fold_matrix_multiindex/all_matrices/'+temp_matrix_type+'/')

        #get the list of compounds that we keep
        compounds_to_keep=pandas.read_csv('../resources/species_organ_maps/networkx_shrink_compound.txt')
        compounds_to_keep_list=compounds_to_keep['nodes_to_keep'].to_list()
        shortened_file_list=[i for i in file_list if i[:-4] in compounds_to_keep_list]
        file_list=shortened_file_list
        print(file_list)


        #print(file_list)
        #hold=input('hold')
    
        chunk_size=len(file_list)//num_processes
        file_list_list=list()
        for i in range(num_processes):
            if i< num_processes-1:
                file_list_list.append(file_list[i*chunk_size:(i+1)*chunk_size])
            elif i ==(num_processes-1):
                file_list_list.append(file_list[i*chunk_size:])

        temp_iterable=list(zip(file_list_list,repeat(temp_matrix_type)))
        pool = multiprocessing.Pool(processes=num_processes)
        #transformed_chunks=
        pool.starmap(perform_fold_analysis,temp_iterable)
        #transform_organ_column(post_species_transform_panda)
        #recombine_chunks
        #for i in range(len(transformed_chunks)):
        #    post_species_transform_panda.iloc[transformed_chunks[i].index]=transformed_chunks[i]
        #post_species_transform_panda=pd.concat(transformed_chunks)
        pool.close()










    '''
    from_list,to_list=extract_from_and_to_sets(triplet_panda)

    
    print(triplet_panda['from_to'].value_counts())
    print(len(from_list))
    print(len(to_list))

    

    input_fold_panda=pandas.read_pickle(input_fold_panda_address)
    print(input_fold_panda)

    results_list=list()

    for i,to_element in enumerate(to_list):
        print(i)
        #print(to_element)
        temp_view=input_fold_panda.loc[:,input_fold_panda.columns.isin(to_element)]
        #print(temp_view)
        #hold=input('hold')

        for from_element in from_list:
            #print(to_element)
            #print(from_element)
            temp_temp_view=temp_view.loc[input_fold_panda.index.isin(from_element)]
            #print(temp_temp_view)
            results_list.append(one_df_transform(temp_temp_view.values))
            #print(result)
            #hold=input('hold')

    end_time=time.time()

    total_time=end_time-start_time
    print('start time '+str(start_time))
    print('end time '+str(end_time))
    print('total time '+str(total_time))
    '''
