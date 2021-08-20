import numpy as np
import pandas
import os
#import transform_written_organs
import multiprocessing
from pprint import pprint

def show_all_organ_species_disease_triplets(temp_panda):
    set_of_organ_species_disease_tuples=set()
    for index, series in temp_panda.iterrows():
        this_bins_triplets=zip(series['organ'],series['species'],series['special_property_list'])
        for this_bins_triplets in this_bins_triplets:
            set_of_organ_species_disease_tuples.add(this_bins_triplets)
    return set_of_organ_species_disease_tuples

def calculate_one_fold_change_matrix(temp_bin,temp_MultiIndex):
    '''
    The general logic for a fold change matrix is -

    get the total set of (species, organ) that exist in binvestigate
    calculate the fold change matrix as the outer product of this list with itself

    We use the total set so that we can just superimpose all matrices and compare values at the same cell location

    each cell in the matrix follows a punnit square logic

                        to
                finite      missing         
        finite  divide      -np.inf   
                (sign +/-)
    from

        missing np.inf      np.nan

    
    '''

    #this is the fold change matrix that we start with
    temp_DataFrame=pandas.DataFrame(data=np.nan,index=temp_MultiIndex,columns=temp_MultiIndex)

    
    #this is possibly the faster, vectorized way to do things
    #however, it will lead to at least a fully calculated matrix which is unnecessary

    #tuple_list=zip(temp_bin['organ'],temp_bin['species'])
    tuple_list=zip(temp_bin['organ'],temp_bin['species'])

    intensity_dict=dict(zip(tuple_list,temp_bin['intensity']))

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
                try:
                    if intensity_dict[temp_column]>from_intensity:
                        temp_DataFrame.at[series.name,temp_column]=intensity_dict[temp_column]/from_intensity
                    else:
                        temp_DataFrame.at[series.name,temp_column]=-from_intensity/intensity_dict[temp_column]
                except KeyError:
                    temp_DataFrame.at[series.name,temp_column]=-np.inf


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

def calculate_one_fold_change_matrix_trip(temp_bin,temp_MultiIndex):
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

    
    '''

    #this is the fold change matrix that we start with
    temp_DataFrame=pandas.DataFrame(data=np.nan,index=temp_MultiIndex,columns=temp_MultiIndex)

    
    #this is possibly the faster, vectorized way to do things
    #however, it will lead to at least a fully calculated matrix which is unnecessary

    #tuple_list=zip(temp_bin['organ'],temp_bin['species'])
    tuple_list=zip(temp_bin['organ'],temp_bin['species'],temp_bin['special_property_list'])

    intensity_dict=dict(zip(tuple_list,temp_bin['intensity']))

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
                try:
                    if intensity_dict[temp_column]>from_intensity:
                        temp_DataFrame.at[series.name,temp_column]=intensity_dict[temp_column]/from_intensity
                    else:
                        temp_DataFrame.at[series.name,temp_column]=-from_intensity/intensity_dict[temp_column]
                except KeyError:
                    temp_DataFrame.at[series.name,temp_column]=-np.inf


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

def calculate_all_fold_change_matrices(temp_panda,temp_organ_species_tuple_list):
    '''
    merely a wrapper for the single fold change matrix function
    '''
    
    temp_panda['fold_change_matrix']='pre_analysis'

    #all fold change matrices have the same row/column labels (see single for further logic)
    temp_organ_species_tuple_list.sort(key=lambda temp_tup: temp_tup[0])
    #we use multiindex so that we can do cute things switching the ordering later
    my_MultiIndex=pandas.MultiIndex.from_tuples(tuples=temp_organ_species_tuple_list,sortorder=None,names=['organ','species'])

    for index,series in temp_panda.iterrows():
        #we print merely to see how long this is taking
        print(index)
        print(series['name'])
        temp_panda.at[index,'fold_change_matrix']=calculate_one_fold_change_matrix(series,my_MultiIndex)

def calculate_all_fold_change_matrices_trip(temp_panda):
    '''
    '''

    temp_organ_species_disease_tuple_list=organ_species_disease_tuple_list

    #temp_organ_species_disease_tuple_list=

    temp_panda['fold_change_matrix']='pre_analysis'

    #we use multiindex so that we can do cute things switching the ordering later
    my_MultiIndex=pandas.MultiIndex.from_tuples(tuples=temp_organ_species_disease_tuple_list,sortorder=None,names=['organ','species','disease'])

    for index,series in temp_panda.iterrows():
        #we print merely to see how long this is taking
        print(index)
        print(series['name'])
        temp_panda.at[index,'fold_change_matrix']=calculate_one_fold_change_matrix_trip(series,my_MultiIndex)    

    return temp_panda


if __name__ == "__main__":
    
    count_cutoff=snakemake.params.count_cutoff
    input_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_5_panda_cleaned/binvestigate_ready_for_analysis.bin'
    output_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_6_generate_fold_matrices/binvestigate_with_fold_matrices.bin'
    os.system('mkdir -p /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_6_generate_fold_matrices/')
    os.system('touch /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_6_generate_fold_matrices/dummy.txt')

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
    num_processes = multiprocessing.cpu_count()
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
    transformed_chunks=pool.map(calculate_all_fold_change_matrices_trip,panda_chunks)
    #recombine_chunks
    for i in range(len(transformed_chunks)):
        input_panda.loc[transformed_chunks[i].index]=transformed_chunks[i]
    input_panda=pandas.concat(transformed_chunks)
    ####

    #create the total pairwise fold change dataframe for each bin
    #calculate_all_fold_change_matrices(input_panda,organ_species_tuple_list)
    #calculate_all_fold_change_matrices_trip(input_panda,organ_species_disease_tuple_list)

    #output as pickle
    input_panda.to_pickle(output_panda_address)