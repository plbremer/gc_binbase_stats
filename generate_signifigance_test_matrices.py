import numpy as np
import pandas
import os
#import transform_written_organs
import multiprocessing
from pprint import pprint
import sys
from itertools import repeat
import scipy.stats


def show_all_organ_species_disease_triplets(temp_panda):
    set_of_organ_species_disease_tuples=set()
    for index, series in temp_panda.iterrows():
        this_bins_triplets=zip(series['organ'],series['species'],series['special_property_list'])
        for this_bins_triplets in this_bins_triplets:
            set_of_organ_species_disease_tuples.add(this_bins_triplets)
    return set_of_organ_species_disease_tuples


def calculate_one_signifigance_matrix_trip(temp_bin,temp_MultiIndex,signifigance_type):
    '''
    asdf
    '''

    #this is the fold change matrix that we start with
    temp_DataFrame=pandas.DataFrame(data=np.nan,index=temp_MultiIndex,columns=temp_MultiIndex)
    tuple_list=zip(temp_bin['organ'],temp_bin['species'],temp_bin['special_property_list'])
    distribution_dict=dict(zip(tuple_list,temp_bin['annotation_distribution']))

    #we iterate through the rows in the fold change matrix
    #we couldnt do neat .apply or other vectorized approaches because the data required
    #were in lists for each bin (series)
    #plb edit 2-7-2022
    #we put the if statement on the outside so we do it once not 1 billion times
    if signifigance_type=='mannwhitney':
        for index,series in temp_DataFrame.iterrows():
            from_distribution=distribution_dict[series.name]
            for temp_column in temp_DataFrame.columns:
                #if we are on a diagonal
                if index == temp_column:
                    temp_DataFrame.at[series.name,temp_column]=np.nan
                    continue
                else:
                    #placeholder while scipy is down
                    _,p=scipy.stats.mannwhitneyu(from_distribution,distribution_dict[temp_column],use_continuity=False,alternative='two-sided')
                    temp_DataFrame.at[series.name,temp_column]=p
    elif signifigance_type=='welch':
        for index,series in temp_DataFrame.iterrows():
            from_distribution=distribution_dict[series.name]
            for temp_column in temp_DataFrame.columns:
                #if we are on a diagonal
                if index == temp_column:
                    temp_DataFrame.at[series.name,temp_column]=np.nan
                    continue
                else:
                    #placeholder while scipy is down
                    _,p=scipy.stats.ttest_ind(np.log10(np.array(from_distribution)),np.log10(np.array(distribution_dict[temp_column])),equal_var=False,alternative='two-sided')
                    temp_DataFrame.at[series.name,temp_column]=p
    
    #plb 2-7-2022
    #some of these things are so signifigant that they are numerically incalculable
    #like, the p value is zero
    #therefore, we impute the min p value for that dataframe
    temp=temp_DataFrame.stack().stack().stack()
    impute_value=temp.loc[temp != 0].min()
    temp_DataFrame=temp_DataFrame.applymap(lambda x: impute_value if x==0 else x)
    #print(0 in temp_DataFrame.values)




    return temp_DataFrame


def calculate_all_signifigance_matrices_trip(temp_panda,signifigance_type):
    '''
    asdf
    '''

    temp_organ_species_disease_tuple_list=organ_species_disease_tuple_list

    temp_panda['signifigance_'+signifigance_type]='pre_analysis'

    #we use multiindex so that we can do cute things switching the ordering later
    my_MultiIndex=pandas.MultiIndex.from_tuples(tuples=temp_organ_species_disease_tuple_list,sortorder=None,names=['organ','species','disease'])

    for index,series in temp_panda.iterrows():
        #we print merely to see how long this is taking
        print(index)
        print(series['name'])
        temp_panda.at[index,'signifigance_'+signifigance_type]=calculate_one_signifigance_matrix_trip(series,my_MultiIndex,signifigance_type)    

    return temp_panda


if __name__ == "__main__":
    
    #2-06-2022 plb
    #deleted the "non trip version" of the functions as they only seemed to handle species/organ

    #min_fold_change=snakemake.params.min_fold_change
    min_fold_change=sys.argv[1]
    cores_available=int(sys.argv[2])
    input_panda_address='../results/'+str(min_fold_change)+'/step_6_generate_fold_matrices/binvestigate_with_fold_matrices.bin'
    output_panda_address='../results/'+str(min_fold_change)+'/step_6_b_generate_signifigance_test_matrices/binvestigate_with_signifigance_matrices.bin'
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_6_b_generate_signifigance_test_matrices/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_6_b_generate_signifigance_test_matrices/dummy.txt')

    input_panda=pandas.read_pickle(input_panda_address)
    print(input_panda)
    print(input_panda.index)
    hold=input('hold')
    #obtain total organ-species list
    #organ_species_tuple_list=list(transform_written_organs.show_all_organ_species_pairs(input_panda))
    organ_species_disease_tuple_list=list(show_all_organ_species_disease_triplets(input_panda))
    pprint(organ_species_disease_tuple_list)
    hold=input('hold')
    #all fold change matrices have the same row/column labels (see single for further logic)
    organ_species_disease_tuple_list.sort(key=lambda temp_tup: (temp_tup[0],temp_tup[1],temp_tup[2]))
    pprint(organ_species_disease_tuple_list)
    hold=input('hold')
    

    #update 7-4-22 plb
    #basically, we are only going to do the volcano plot stuff for knowns.
    #so we grab a subset of the entire panda, those with inchikeys, do the comparison for them
    #and then merge
    input_panda_only_identified=input_panda.loc[
        input_panda.inchikey!='@@@@@@@',:
    ]

    
    ####
    #num_processes = multiprocessing.cpu_count()
    temp_signifigance_type='mannwhitney'
    num_processes=cores_available
    chunk_size = len(input_panda_only_identified.index)//num_processes
    panda_chunks=list()
    for i in range(0,num_processes):
        if i<(num_processes-1):
            panda_chunks.append(input_panda_only_identified.iloc[i*chunk_size:(i+1)*chunk_size])
        elif i==(num_processes-1):
            panda_chunks.append(input_panda_only_identified.iloc[i*chunk_size:])
    print(panda_chunks)
    hold=input('check chunks')
    pool = multiprocessing.Pool(processes=num_processes)
    temp_iterable=list(zip(panda_chunks,repeat(temp_signifigance_type)))
    transformed_chunks=pool.starmap(calculate_all_signifigance_matrices_trip,temp_iterable)
    #recombine_chunks
    pool.close()
    pool.join()
    for i in range(len(transformed_chunks)):
        input_panda_only_identified.loc[transformed_chunks[i].index]=transformed_chunks[i]
    input_panda_only_identified=pandas.concat(transformed_chunks)
    ####

    ####
    #num_processes = multiprocessing.cpu_count()
    temp_signifigance_type='welch'
    num_processes=cores_available
    chunk_size = len(input_panda_only_identified.index)//num_processes
    panda_chunks=list()
    for i in range(0,num_processes):
        if i<(num_processes-1):
            panda_chunks.append(input_panda_only_identified.iloc[i*chunk_size:(i+1)*chunk_size])
        elif i==(num_processes-1):
            panda_chunks.append(input_panda_only_identified.iloc[i*chunk_size:])
    print(panda_chunks)
    hold=input('check chunks')
    pool = multiprocessing.Pool(processes=num_processes)
    temp_iterable=list(zip(panda_chunks,repeat(temp_signifigance_type)))
    transformed_chunks=pool.starmap(calculate_all_signifigance_matrices_trip,temp_iterable)
    #recombine_chunks
    pool.close()
    pool.join()
    for i in range(len(transformed_chunks)):
        input_panda_only_identified.loc[transformed_chunks[i].index]=transformed_chunks[i]
    input_panda_only_identified=pandas.concat(transformed_chunks)
    ####

    input_panda_only_identified=input_panda_only_identified.loc[
        :,['inchikey','signifigance_mannwhitney','signifigance_welch']
    ]

    input_panda=input_panda.merge(
        right=input_panda_only_identified,
        left_on='inchikey',
        right_on='inchikey',
        how='left'
    )


    #output as pickle
    input_panda.loc[
        input_panda.inchikey!='@@@@@@@',:
    ].to_pickle(output_panda_address)