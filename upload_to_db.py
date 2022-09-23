import sys
import os
from sqlalchemy import create_engine
from sqlalchemy import Table, String
from sqlalchemy.dialects import postgresql
import pandas as pd
import psycopg2
import numpy as np
#https://stackoverflow.com/questions/50626058/psycopg2-cant-adapt-type-numpy-int64
from psycopg2.extensions import register_adapter, AsIs
#https://stackoverflow.com/questions/50626058/psycopg2-cant-adapt-type-numpy-int64
def adapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
import time

def choose_all_bins(directory_address):
    full_list=os.listdir(directory_address)
    return full_list

def prepare_one_bin_for_upload(temp_bin):
    '''
    prepares one bin/class entry for the database
    we open all 4 fold/sig for one compund, stack them, typecast to dataframe, concat, change header names, change header order

    '''
    matrix_type_list=[
        '../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/all_matrices/fold_change_matrix_average/',
        '../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/all_matrices/fold_change_matrix_median/',
        '../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/all_matrices/signifigance_matrix_mannwhitney/',
        '../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/all_matrices/signifigance_matrix_welch/'
    ]
    
    pandas_list=[
        pd.read_pickle(temp_location+temp_bin) for temp_location in matrix_type_list
    ]
    
    for i,panda in enumerate(pandas_list):
        #panda.index.set_names(names=['organ_from','species_from','disease_from'],inplace=True)
        #panda.columns.set_names(names=['organ_to','species_to','disease_to'],inplace=True)
        #print(panda)
        pandas_list[i]=pd.DataFrame(panda.stack().stack().stack())
        pandas_list[i].index.set_names(['organ_from','species_from','disease_from','disease_to','species_to','organ_to'],inplace=True)
    
    pandas_list[0].rename({0:'fold_change_average'},inplace=True,axis='columns')
    pandas_list[1].rename({0:'fold_change_median'},inplace=True,axis='columns')
    pandas_list[2].rename({0:'significance_mwu'},inplace=True,axis='columns')
    pandas_list[3].rename({0:'significance_welch'},inplace=True,axis='columns')
    #print(pandas_list[0])
    total_panda=pd.concat(pandas_list,axis='columns')
    
    total_panda.reset_index(inplace=True)
    
    total_panda.insert(loc=0,column='compound_id',value=temp_bin[:-4])
    
    total_panda=total_panda[[
        'compound_id','species_from', 'organ_from', 'disease_from', 
        'species_to', 'organ_to', 'disease_to','fold_change_average', 'fold_change_median',
        'significance_mwu', 'significance_welch'
    ]]
    
    return total_panda


def upload_fold_change_panda(temp_panda_for_upload,bin_iteration,connection):

    if bin_iteration==0:
        temp_panda_for_upload.to_sql(
            'differential_analysis',
            connection,
            index=False,
            dtype={
                'compound_id':postgresql.TEXT,
                'species_from':postgresql.TEXT,
                'organ_from':postgresql.TEXT,
                'disease_from':postgresql.TEXT,
                'species_to':postgresql.TEXT,
                'organ_to':postgresql.TEXT,
                'disease_to':postgresql.TEXT,
                'fold_change_average':postgresql.FLOAT,
                'fold_change_median':postgresql.FLOAT,
                'significance_mwu':postgresql.FLOAT,
                'significance_welch':postgresql.FLOAT,
            },
            if_exists='replace',
            method='multi',
            chunksize=90000
        )
  
    elif bin_iteration!=0:
        temp_panda_for_upload.to_sql(
            'differential_analysis',
            connection,
            index=False,
            dtype={
                'compound_id':postgresql.TEXT,
                'species_from':postgresql.TEXT,
                'organ_from':postgresql.TEXT,
                'disease_from':postgresql.TEXT,
                'species_to':postgresql.TEXT,
                'organ_to':postgresql.TEXT,
                'disease_to':postgresql.TEXT,
                'fold_change_average':postgresql.FLOAT,
                'fold_change_median':postgresql.FLOAT,
                'significance_mwu':postgresql.FLOAT,
                'significance_welch':postgresql.FLOAT,
            },
            if_exists='append',
            method='multi',
            chunksize=90000
        )

def upload_non_ratio_table(temp_panda,connection):
    temp_panda.to_sql(
        'non_ratio_table',
        connection,
        index=False,
        dtype={
            'bin':postgresql.INTEGER,
            'compound':postgresql.TEXT,
            'species':postgresql.TEXT,
            'organ':postgresql.TEXT,
            'disease':postgresql.TEXT,
            'intensity_average':postgresql.FLOAT,
            'intensity_median':postgresql.FLOAT,
            'percent_present':postgresql.FLOAT
        },
        if_exists='replace',
        method='multi',
        chunksize=90000
    )    
    



if __name__ == "__main__":

    min_fold_change=sys.argv[1]
    use_aws=(sys.argv[2])
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_10_upload_to_db/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_10_upload_to_db/dummy.txt')

    if use_aws=='False':
        my_server='localhost'
        my_database='binvestigate_second'
        my_dialect='postgresql'
        my_driver='psycopg2'
        my_username='rictuar'
        my_password='elaine123'
        my_port='5432'

    elif use_aws=='True':
        my_server='fold-result-database.czbab8f7pgfj.us-east-2.rds.amazonaws.com'
        my_database='foldresults'
        my_dialect='postgresql'
        my_driver='psycopg2'
        my_username='postgres'
        my_password='elaine123'
        my_port='5430'

    my_connection=f'{my_dialect}+{my_driver}://{my_username}:{my_password}@{my_server}:{my_port}/{my_database}'
    engine=create_engine(my_connection)#,echo=True)
    connection=engine.connect()

    #upload non-ratio table
    table_5_address='../results/'+str(min_fold_change)+'/step_5_b_make_non_ratio_table/non_ratio_table.bin'
    non_ratio_panda=pd.read_pickle(table_5_address)
    upload_non_ratio_table(non_ratio_panda,connection)
    start_time=time.time()
    #create our index
    connection.execute(
        f'''
        ALTER TABLE non_ratio_table ADD PRIMARY KEY (bin,species,organ,disease);
        '''
    )      
    end_time=time.time()
    print('time to create non ratio index: '+str(end_time-start_time))








    # #upload the fold change matrices
    # #get list of compounds and classes (listdir on one) (basically just bins)
    # full_list=choose_all_bins('../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/all_matrices/fold_change_matrix_average')
    # #for each bin, prepare each then upload each
    # for i,temp_bin in enumerate(full_list):
    #     start_time=time.time()
        
    #     temp_panda_for_upload=prepare_one_bin_for_upload(temp_bin)
    #     upload_fold_change_panda(temp_panda_for_upload,i,connection)
        
    #     end_time=time.time()
    #     print(temp_bin+': '+str(end_time-start_time))


    # start_time=time.time()
    # #create our index
    # connection.execute(
    #     f'''
    #     ALTER TABLE differential_analysis ADD PRIMARY KEY (compound_id, species_from, organ_from, disease_from, species_to, organ_to, disease_to);
    #     '''
    # )      
    # end_time=time.time()
    # print('time to create complete differential analysis index: '+str(end_time-start_time))