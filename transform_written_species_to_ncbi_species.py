import numpy as np
import pandas
from ete3 import NCBITaxa
import os
import multiprocessing
import sys
from sqlalchemy import create_engine
from sqlalchemy import Table, String
from sqlalchemy.dialects import postgresql

def get_all_strings_in_list_across_panda_column(temp_panda,temp_column_name):
    '''
    in the binvestigate panda, each row is a bin
    each bin is associated with organs and species that are saved as lists
    
    this function iterates over each rows lists and attempts to add all elements to a cumulative set
    '''
    total_elements=set()

    for index, series in temp_panda.iterrows():

        temp_set=set(series[temp_column_name])

        total_elements.update(temp_set)

    return total_elements

def identify_elements_not_in_ncbi(temp_set):
    '''
    takes a set of strings and returns a set that do not map to exactly 1 taxonomical identification
    '''

    #creat an ncbi taxonomy object. theres a sql database hidden in the home directory that this references
    ncbi=NCBITaxa()
    #ncbi.update_taxonomy_database()

    has_0_id_set=set()
    has_more_than_1_id_set=set()

    #we scroll over each instead of sending the entire set because those that do not map are not returned in the dict
    for temp_element in temp_set:

        returned_dict=ncbi.get_name_translator([temp_element])

        #if the dict is emtpy
        if not any(returned_dict):
            has_0_id_set.add(temp_element)

        #if the string returns more than 1 element
        elif len(returned_dict[temp_element]) > 1:
            has_more_than_1_id_set.add(temp_element)

        #otherwise do nothing, we only care about problems

    return has_0_id_set, has_more_than_1_id_set

def print_some_set(temp_set):
    '''
    prints elements of a set, 1 element per line
    '''
    for temp_element in temp_set:
        print(temp_element)

def transform_species_column(temp_bin_panda):
    '''
    This function takes the binvestigate panda and the address to a mapping .tsv

    It applies the rules from the mapping tsv to the binvestigate panda

    There are two types of rules: drop rules and transform rules
    Drop rules exist because we dont want all "species" in our final analysis. that is because
    the species is something nonsensical like "nist standards" or "delete me"
    In drop rules, we find the index of all species equal to the original, then drop the species at those indices
    and the corresponding organs at those indices

    in transfomrs, we take the original text and map it to the most specific thing that we can that is in the ncbi database
    '''
    temp_mapping_address=species_mapping_address
    mapping_panda=pandas.read_csv(temp_mapping_address,sep='\t')

    #apply each transformation to each row
    for mapping_index, mapping_series in mapping_panda.iterrows():
        print(mapping_index)

        #declare mapping rule
        #drop rules work differently. must get all indices and then drop from mapping as well as organs
        if mapping_series['most_specific'] == 'drop':
            
            for bin_index, bin_series in temp_bin_panda.iterrows():
                indices_to_drop=[i for i in range(0,len(bin_series['species'])) if bin_series['species'][i] == mapping_series['list_of_species_that_had_zero_ncbi_id']]
                species_list_with_indices_removed=list(np.delete(bin_series['species'],indices_to_drop))
                organ_list_with_indices_removed=list(np.delete(bin_series['organ'],indices_to_drop))
                total_intensity_list_with_indices_removed=list(np.delete(bin_series['total_intensity'],indices_to_drop))
                median_intensity_list_with_indices_removed=list(np.delete(bin_series['median_intensity'],indices_to_drop))
                count_list_with_indices_removed=list(np.delete(bin_series['count'],indices_to_drop))
                annotation_distribution_list_with_indices_removed=list(np.delete(bin_series['annotation_distribution'],indices_to_drop))

                temp_bin_panda.at[bin_index,'species']=species_list_with_indices_removed
                temp_bin_panda.at[bin_index,'organ']=organ_list_with_indices_removed
                temp_bin_panda.at[bin_index,'total_intensity']=total_intensity_list_with_indices_removed
                temp_bin_panda.at[bin_index,'median_intensity']=median_intensity_list_with_indices_removed
                temp_bin_panda.at[bin_index,'count']=count_list_with_indices_removed
                temp_bin_panda.at[bin_index,'annotation_distribution']=annotation_distribution_list_with_indices_removed

        #if we have a transformation
        elif mapping_series['most_specific'] != 'drop':

            for bin_index, bin_series in temp_bin_panda.iterrows():

                for i in range(0,len(bin_series['species'])):
                    if (bin_series['species'][i] == mapping_series['list_of_species_that_had_zero_ncbi_id']):
                        bin_series['species'][i] = mapping_series['most_specific']

                temp_bin_panda.at[bin_index,'species']=bin_series['species']

    return temp_bin_panda





if __name__ == "__main__":


    min_fold_change=sys.argv[1]
    cores_available=int(sys.argv[2])
    #start_from_aws=(sys.argv[3])
    start_from_aws='False'
    binvestigate_pickle_address='../results/'+str(min_fold_change)+'/step_0_c_complete_pipeline_input/pipeline_input_group_properties_added.bin'
    #binvestigate_pickle_address='../resources/binvestigate_pull/shortened_file_for_test.bin'
    species_mapping_address='../resources/species_organ_maps/species_map.txt'
    output_pickle_address='../results/'+str(min_fold_change)+'/step_1_species_transformed/binvestigate_species_transformed.bin'
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_1_species_transformed/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_1_species_transformed/dummy.txt')
    

    if start_from_aws=='False':
        print('hello')
        binvestigate_panda=pandas.read_pickle(binvestigate_pickle_address)
    elif start_from_aws=='True':
        my_server='info-from-binvestigate.czbab8f7pgfj.us-east-2.rds.amazonaws.com'
        my_database='binvestigate'
        my_dialect='postgresql'
        my_driver='psycopg2'
        my_username='postgres'
        my_password='elaine123'
        my_connection=f'{my_dialect}+{my_driver}://{my_username}:{my_password}@{my_server}/{my_database}'
        engine=create_engine(my_connection)#,echo=True)
        connection=engine.connect()
        binvestigate_panda=pandas.read_sql_table(table_name='pseudo_carrot', con=my_connection)

    #identify species names that do not map to the NCBI database
    #this is done one time not as part of the "informatics pipeline" but rather
    #so that we can build the "species_mapping.txt"
    all_species_set=get_all_strings_in_list_across_panda_column(binvestigate_panda,'species')
    #we want species to map to exactly 1 place in the taxonomy. sometimes
    #species map to 0 and sometimes they map to >1
    #the "id" in this case is a number associated with the ncbi taxonomy
    has_0_id_set,has_more_than_1_id_set=identify_elements_not_in_ncbi(all_species_set)

    print_some_set(all_species_set)
    hold=input('copy and paste the all species set if necessary')
    print_some_set(has_0_id_set)
    hold=input('copy and paste the has 0 id if necessary')
    print_some_set(has_more_than_1_id_set)
    hold=input('copy and paste the has multiple id if necessary')

    
    #later, after doing a curatin of this list, we put the transform file in the 
    #'species_mapping_address' location
    #translate species names according to some transform list and drop things that either have no translation or are identified with a translation 'drop'
    #num_processes = multiprocessing.cpu_count()
    num_processes= cores_available
    chunk_size = len(binvestigate_panda.index)//num_processes
    panda_chunks=list()
    for i in range(0,num_processes):
    #chunks = [post_species_transform_panda.iloc[post_species_transform_panda[i:i + chunk_size]] for i in range(0, post_species_transform_panda.shape[0], chunk_size)]
        if i<(num_processes-1):
            panda_chunks.append(binvestigate_panda.iloc[i*chunk_size:(i+1)*chunk_size])
        elif i==(num_processes-1):
            panda_chunks.append(binvestigate_panda.iloc[i*chunk_size:])
    print(panda_chunks)
    hold=input('check chunks')
    pool = multiprocessing.Pool(processes=num_processes)
    transformed_chunks=pool.map(transform_species_column,panda_chunks)
    #recombine_chunks
    for i in range(len(transformed_chunks)):
        binvestigate_panda.iloc[transformed_chunks[i].index]=transformed_chunks[i]
    binvestigate_panda=pandas.concat(transformed_chunks)
    

    #confirm that has_0_id_set,has_more_than_1_id_set are empty
    all_species_set=get_all_strings_in_list_across_panda_column(binvestigate_panda,'species')
    has_0_id_set,has_more_than_1_id_set=identify_elements_not_in_ncbi(all_species_set)
    print_some_set(has_0_id_set)
    hold=input('confirm 0 set empty')
    print_some_set(has_more_than_1_id_set)
    hold=input('confirm multiple set empty')

    #output the result
    binvestigate_panda.to_pickle(output_pickle_address)