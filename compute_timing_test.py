import numpy as np
import pandas
import time


def extract_from_and_to_sets(temp_panda):
    from_list=temp_panda.loc[temp_panda['from_to']=='from']['triplets'].to_list()
    to_list=temp_panda.loc[temp_panda['from_to']=='to']['triplets'].to_list()

    return from_list,to_list

def one_df_transform(temp_df):
    '''
    given an numpy array, chooses what the aggregate value is
    '''
    conditions=[
        np.isnan(temp_df).any(),
        (temp_df==np.inf).all(),
        (temp_df==-np.inf).all(),
        (temp_df<0).any() and (temp_df>0).any(),
        (temp_df==0).any(),
        (temp_df>0).all(),
        (temp_df<0).all()
    ]
    
    choices=[
        np.nan,
        np.inf,
        -np.inf,
        0,
        0,
        temp_df.min(),
        temp_df.max()
    ]
    return np.select(conditions,choices)


if __name__ == "__main__":

    start_time=time.time()

    input_fold_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/1/step_13_swap_fold_matrix_multiindex/each_compounds_fold_matrix/2.bin'
    input_triplet_panda_address='/home/rictuar/delete_test_bin_calc/unique_triplets'
    output_address='/home/rictuar/delete_test_bin_calc/calculation_results'

    triplet_panda=pandas.read_pickle(input_triplet_panda_address)
    #print(triplet_panda)
    #triplet_panda=triplet_panda.loc[triplet_panda['triplets'] != {}]
    #print(triplet_panda)
    #hold=input('hold')

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