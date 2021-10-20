import pandas
import os
'''
The purpose of this file is to take the disparate information storage pandas and 
compile them into pandas, where each panda represents a table in our final app database

'''


def make_headnode_properties_table(temp_input_address,temp_output_address):
    '''
    at the moment, the input matches exactly, so we simply copy the file
    '''

    temp=pandas.read_pickle(temp_input_address)
    temp.write_pickle(temp_output_address)


def make_triplet_properties_table():
    '''
    for the moment this makes a fake table because we cant make the real one until gert does his thinge
    '''

    print('hi')



if __name__ == "__main__":


    headnode_properties_table_input_1_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/1/step_16_calculate_fraction_triplets/triplet_count_panda.bin'
    headnode_properties_table_output_address='/home/rictuar/delete_test_bin_calc/files_for_database/headnode_triplet_properties/headnode_triplet_properties.bin'
    make_headnode_properties_table(headnode_properties_table_input_1_address,headnode_properties_table_output_address)


    triplet_list_properties_table_output_address='/home/rictuar/delete_test_bin_calc/files_for_database/triplet_list_properties/triplet_list_properties.bin'
    #make_triplet_properties_table()

    
    fold_results_base_address='/home/rictuar/delete_test_bin_calc/fold_results/'
    #make_results_table()

