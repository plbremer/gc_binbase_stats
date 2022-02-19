import numpy as np
import pandas
import os
#import transform_written_organs
import multiprocessing
from pprint import pprint
import sys
from itertools import repeat


def show_all_organ_species_disease_triplets(temp_panda):
    set_of_organ_species_disease_tuples=set()
    for index, series in temp_panda.iterrows():
        this_bins_triplets=zip(series['organ'],series['species'],series['special_property_list'])
        for this_bins_triplets in this_bins_triplets:
            set_of_organ_species_disease_tuples.add(this_bins_triplets)
    return set_of_organ_species_disease_tuples


def calculate_one_fold_change_matrix_trip(temp_bin,temp_MultiIndex,fold_change_type):
    '''
    The general logic for a fold change matrix is -

    get the total set of (species, organ, disease) that exist in binvestigate
    calculate the fold change matrix as the outer product of this list with itself

    We use the total set so that we can just superimpose all matrices and compare values at the same cell location

    each cell in the matrix follows a punnit square logic

                        to
                finite      missing         
        finite  divide      -np.inf   
                (sign +/-)
    from

        missing np.inf      np.nan
    plb edit 2-6-2022
    the above matrix is basically a moot point now because all compounds for all sod have a non-zero 
    average or median intensity
    '''

    #this is the fold change matrix that we start with
    temp_DataFrame=pandas.DataFrame(data=np.nan,index=temp_MultiIndex,columns=temp_MultiIndex)
    tuple_list=zip(temp_bin['organ'],temp_bin['species'],temp_bin['special_property_list'])
    intensity_dict=dict(zip(tuple_list,temp_bin[fold_change_type]))

    #we iterate through the rows in the fold change matrix
    #we couldnt do neat .apply or other vectorized approaches because the data required
    #were in lists for each bin (series)
    for index,series in temp_DataFrame.iterrows():

        try:
            from_intensity=intensity_dict[series.name]
            for temp_column in temp_DataFrame.columns:
                #if we are on a diagonal
                if index == temp_column:
                    temp_DataFrame.at[series.name,temp_column]=np.nan
                    continue
                
                #plb edit 2-18-2022
                #we are going to make this all a lot faster i think and switch to the superior fold change approach
                #which is simply the log of the dividing
                #ok after taking a look at this it might not be faster. it could be vectorized fairly easily probably
                #but i have better things to do
                else:
                    temp_DataFrame.at[series.name,temp_column]=np.log2(intensity_dict[temp_column]/from_intensity)

                # try:
                #     if intensity_dict[temp_column]>from_intensity:
                #         temp_DataFrame.at[series.name,temp_column]=intensity_dict[temp_column]/from_intensity
                #     else:
                #         temp_DataFrame.at[series.name,temp_column]=-from_intensity/intensity_dict[temp_column]
                # #plb edit 2-6-2022
                # #i dont think that we will ever see key errors at this point
                # #because every sod has a distribution because data come form carrot
                # #i think that this applies to all key errors here
                # except KeyError:
                #     temp_DataFrame.at[series.name,temp_column]=-np.inf

        except KeyError:
            for temp_column in temp_DataFrame.columns:
                #if we are on a diagonal
                if index == temp_column:
                    temp_DataFrame.at[series.name,temp_column]=np.nan
                    continue
                try:
                    if (intensity_dict[temp_column]):
                        temp_DataFrame.at[series.name,temp_column]=np.inf
                except KeyError:
                    continue

    return temp_DataFrame


def calculate_all_fold_change_matrices_trip(temp_panda,fold_change_type):
    '''
    '''

    temp_organ_species_disease_tuple_list=organ_species_disease_tuple_list

    temp_panda['fold_change_'+fold_change_type]='pre_analysis'

    #we use multiindex so that we can do cute things switching the ordering later
    my_MultiIndex=pandas.MultiIndex.from_tuples(tuples=temp_organ_species_disease_tuple_list,sortorder=None,names=['organ','species','disease'])

    for index,series in temp_panda.iterrows():
        #we print merely to see how long this is taking
        print(index)
        print(series['name'])
        temp_panda.at[index,'fold_change_'+fold_change_type]=calculate_one_fold_change_matrix_trip(series,my_MultiIndex,fold_change_type)    



    return temp_panda


if __name__ == "__main__":
    
    #2-06-2022 plb
    #deleted the "non trip version" of the functions as they only seemed to handle species/organ

    #min_fold_change=snakemake.params.min_fold_change
    min_fold_change=sys.argv[1]
    cores_available=int(sys.argv[2])
    input_panda_address='../results/'+str(min_fold_change)+'/step_5_panda_cleaned/binvestigate_ready_for_analysis.bin'
    output_panda_address='../results/'+str(min_fold_change)+'/step_6_generate_fold_matrices/binvestigate_with_fold_matrices.bin'
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_6_generate_fold_matrices/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_6_generate_fold_matrices/dummy.txt')

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
    

    
    ####
    #num_processes = multiprocessing.cpu_count()
    temp_fold_change_type='total_intensity'
    num_processes=cores_available
    chunk_size = len(input_panda.index)//num_processes
    panda_chunks=list()
    for i in range(0,num_processes):
        if i<(num_processes-1):
            panda_chunks.append(input_panda.iloc[i*chunk_size:(i+1)*chunk_size])
        elif i==(num_processes-1):
            panda_chunks.append(input_panda.iloc[i*chunk_size:])
    print(panda_chunks)
    hold=input('check chunks')
    pool = multiprocessing.Pool(processes=num_processes)
    temp_iterable=list(zip(panda_chunks,repeat(temp_fold_change_type)))
    transformed_chunks=pool.starmap(calculate_all_fold_change_matrices_trip,temp_iterable)
    #recombine_chunks
    pool.close()
    pool.join()
    for i in range(len(transformed_chunks)):
        input_panda.loc[transformed_chunks[i].index]=transformed_chunks[i]
    input_panda=pandas.concat(transformed_chunks)
    ####


    ####
    #num_processes = multiprocessing.cpu_count()
    temp_fold_change_type='median_intensity'
    num_processes=cores_available
    chunk_size = len(input_panda.index)//num_processes
    panda_chunks=list()
    for i in range(0,num_processes):
        if i<(num_processes-1):
            panda_chunks.append(input_panda.iloc[i*chunk_size:(i+1)*chunk_size])
        elif i==(num_processes-1):
            panda_chunks.append(input_panda.iloc[i*chunk_size:])
    print(panda_chunks)
    hold=input('check chunks')
    pool = multiprocessing.Pool(processes=num_processes)
    temp_iterable=list(zip(panda_chunks,repeat(temp_fold_change_type)))
    transformed_chunks=pool.starmap(calculate_all_fold_change_matrices_trip,temp_iterable)
    #recombine_chunks
    pool.close()
    pool.join()
    for i in range(len(transformed_chunks)):
        input_panda.loc[transformed_chunks[i].index]=transformed_chunks[i]
    input_panda=pandas.concat(transformed_chunks)
    ####


    #output as pickle
    input_panda.to_pickle(output_panda_address)