from sqlalchemy import create_engine
from sqlalchemy import Table, String
from sqlalchemy.dialects import postgresql
import pandas
from pprint import pprint
import os
import sys
import psycopg2
import numpy as np
#https://stackoverflow.com/questions/50626058/psycopg2-cant-adapt-type-numpy-int64
from psycopg2.extensions import register_adapter, AsIs

from sqlalchemy.sql.sqltypes import TEXT


def make_flipped_results_panda(upper_diagonal_panda,temp_list_of_columns_to_flip,temp_list_of_columns_to_negative):
    '''
    i faced a decision: have the tool do the inverse query (because the results are anti symmetric) and the normal query
    and combine the results
    or have the database have both sets of results
    because the memory overhead for the results actually seems small, i am going have the anti results and results in DB
    this panda makes the anti results from the results, which get appended to the main panda just before that panda is uplaoded
    '''

    #make a copy of the panda
    lower_diagonal=upper_diagonal_panda.copy(deep=True)    
    #swap the data
    for i in temp_list_of_columns_to_flip:
        lower_diagonal[[i[0],i[1]]]=lower_diagonal[[i[1],i[0]]]
    # lower_diagonal.rename()
    #make the particular columns negative
    for i in temp_list_of_columns_to_negative:
        lower_diagonal[i]=-1*lower_diagonal[i]
    #swap the name-a-roos
    #not necessary because the first step swap
    # lower_diagonal_name_map = {lower_diagonal.columns[i]:temp_new_column_name_order[i] for i in range(len(temp_new_column_name_order))}
    # lower_diagonal.rename(lower_diagonal_name_map, axis=1, inplace=True)


    return lower_diagonal



def make_update_table_from_panda(
    temp_panda_address,
    temp_engine,
    temp_table_name,
    temp_columns_to_drop,
    temp_columns_for_primary_key,
    temp_columns_that_are_lists,
    temp_first_iteration,
    temp_dtype_dict=None,
    temp_append_antisymmetric_result=None
):
    '''
    open panda
    check if it exists by name
    if it exists
        pandas to sql with append
    if it doesnt exist
        pandas to sql
    alter table primary key
    '''
    temp_panda=pandas.read_pickle(temp_panda_address)

    if temp_append_antisymmetric_result is not None:
        if temp_append_antisymmetric_result==17:
            lower_diagonal_panda=make_flipped_results_panda(
                temp_panda,
                [('species_headnode_from','species_headnode_to'),('organ_headnode_from','organ_headnode_to'),('disease_headnode_from','disease_headnode_to'),('from_triplets_inter_removed_if_nec','to_triplets_inter_removed_if_nec')],
                []
            )
            temp_panda=pandas.concat(objs=[temp_panda,lower_diagonal_panda],axis='index',join='outer',ignore_index=True)

        elif temp_append_antisymmetric_result==18:
            lower_diagonal_panda=make_flipped_results_panda(
                temp_panda,
                [('from_triplets','to_triplets')],
                ['results']
            )
            #plb 2-18-2022
            #basically noticed that we should not be flipping the significance values
            #so we just mul them by -1
            if 'signifigance' in temp_table_name:
                lower_diagonal_panda['results']=lower_diagonal_panda['results'].mul(-1)
                # print(lower_diagonal_panda.loc[lower_diagonal_panda['results']<0])
                # print(temp_panda.loc[temp_panda['results']<0])
                # hold=input('hold')
            temp_panda=pandas.concat(objs=[temp_panda,lower_diagonal_panda],axis='index',join='outer',ignore_index=True)
            temp_panda.drop_duplicates(subset=['from_triplets','to_triplets','compound'],keep='first',inplace=True)

        # print(temp_panda)
        # print(temp_panda)
        # hold=input('hold')
    
    temp_panda.drop(temp_columns_to_drop,inplace=True,axis='columns')

    for temp_column in temp_columns_that_are_lists:
        # try:
        temp_panda[temp_column]=temp_panda[temp_column].apply(lambda x: x.tolist())
        # except AttributeError:
        #     continue
            

    # temp_cursor=connection.execute(
    #     f'''
    #     SELECT EXISTS (
    #         SELECT FROM information_schema.tables
    #         WHERE table_schema = 'public'
    #         AND table_name = '{temp_table_name}'
    #     );
    #     '''
    # )

    #if the table does not already exist
    # if (temp_cursor.first()[0]) == False:
    #     temp_panda.to_sql(
    #         temp_table_name,
    #         engine,
    #         index=False,
    #         dtype=temp_dtype_dict
    #     )
    #     temp_big_string=', '.join(temp_columns_for_primary_key)
    #     temp_big_string='('+temp_big_string+')'
    #     connection.execute(
    #         f'''
    #         ALTER TABLE {temp_table_name} ADD PRIMARY KEY {temp_big_string};
    #         '''
    #     )
    
    # else:
        
        ###an attempt at upsertion that doesnt work###
        # to_be_upserted='to_be_upserted'
        # temp_panda.to_sql(
        #     to_be_upserted,
        #     engine,
        #     index=False,
        #     dtype=temp_dtype_dict
        # )
        # temp_big_string=', '.join(temp_columns_for_primary_key)
        # temp_big_string='('+temp_big_string+')'
        # connection.execute(
        #     f'''
        #     ALTER TABLE {to_be_upserted} ADD PRIMARY KEY {temp_big_string};
        #     '''
        # )
        # temp_big_string=', '.join(temp_panda.columns)
        # temp_big_string='('+temp_big_string+')'
        # connection.execute(
        #     f'''
        #     INSERT INTO {temp_table_name} 
        #     SELECT * from {to_be_upserted};
        #     '''
        # )
        # connection.execute(
        #     f'''
        #     DROP TABLE {to_be_upserted};
        #     '''
        # )       
    if temp_first_iteration==True:
        #if this is the first time we encounter this table
        #so true for 16,17,19,20 always
        #once for 18

        # try:
        #     connection.execute(
        #         f'''
        #         DROP TABLE {temp_table_name};
        #         '''
        #     )
        # except psycopg2.errors.UndefinedTable:
        #     pass


        temp_panda.to_sql(
            temp_table_name,
            engine,
            index=False,
            dtype=temp_dtype_dict,
            if_exists='replace'
        )
        temp_big_string=', '.join(temp_columns_for_primary_key)
        temp_big_string='('+temp_big_string+')'
        connection.execute(
            f'''
            ALTER TABLE {temp_table_name} ADD PRIMARY KEY {temp_big_string};
            '''
        )    

    elif temp_first_iteration==False:
        temp_panda.to_sql(
            temp_table_name,
            engine,
            index=False,
            dtype=temp_dtype_dict,
            if_exists='append'
        )

#https://stackoverflow.com/questions/50626058/psycopg2-cant-adapt-type-numpy-int64
def adapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)

if __name__ == "__main__":



    matrices_to_compute=[
        'fold_change_matrix_average',
        'fold_change_matrix_median',
        'signifigance_matrix_mannwhitney',
        'signifigance_matrix_welch'
    ]

    #hold=input('hold step 22')

    min_fold_change=sys.argv[1]
    use_aws=(sys.argv[2])
    print(use_aws)

    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_22_upsert_to_database/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_22_upsert_to_database/dummy.txt')

    if use_aws=='False':
        my_server='localhost'
        my_database='binvestigate_first'
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


    connection.execute(
        f'''
        drop view if exists combined_results;
        '''
    )

    table_16_address='../results/'+str(min_fold_change)+'/step_16_calculate_fraction_triplets/triplet_count_panda.bin'
    make_update_table_from_panda(
        table_16_address,
        engine,
        'headnodes_to_triplets',
        ['possible_triplets', 'actual_triplets', 'ratio','triplet_list'],
        ('species_headnode', 'organ_headnode', 'disease_headnode'),
        #['triplet_list'],
        [],
        True,
        temp_dtype_dict={
            'species_headnode': postgresql.TEXT,
            'organ_headnode': postgresql.TEXT,
            'disease_headnode': postgresql.TEXT,
            #'triplet_list': postgresql.ARRAY(postgresql.TEXT)            
        },
    )

    print('16 done')
    
    table_17_address='../results/'+str(min_fold_change)+'/step_17_precompute_comparison_triplets/headnodes_to_triplet_list.bin'
    make_update_table_from_panda(
        table_17_address,
        engine,
        'headnode_pairs_to_triplet_list_pair',
        [],
        #('headnode_triplet_from', 'headnode_triplet_to'),
        ('species_headnode_from','organ_headnode_from','disease_headnode_from','species_headnode_to','organ_headnode_to','disease_headnode_to'),
        [],
        True,
        temp_dtype_dict={
            #'headnode_triplet_from': postgresql.ARRAY(postgresql.TEXT), 
            #'headnode_triplet_to': postgresql.ARRAY(postgresql.TEXT),
            'species_headnode_from': postgresql.TEXT,
            'organ_headnode_from': postgresql.TEXT,
            'disease_headnode_from': postgresql.TEXT,
            'species_headnode_to': postgresql.TEXT,
            'organ_headnode_to': postgresql.TEXT,
            'disease_headnode_to': postgresql.TEXT,
            'from_triplets_inter_removed_if_nec': postgresql.INTEGER,#postgresql.ARRAY(postgresql.TEXT),
            'to_triplets_inter_removed_if_nec': postgresql.INTEGER,#postgresql.ARRAY(postgresql.TEXT)
            'basic_vs_basic': postgresql.BOOLEAN
        },
        temp_append_antisymmetric_result=17
    )

    print('17 done')    


    for temp_matrix_type in matrices_to_compute:
        print(temp_matrix_type)
        table_18_base_address='../results/'+str(min_fold_change)+'/step_18_compute_fold_results/all_matrices/'+temp_matrix_type+'/'
        file_list=os.listdir(table_18_base_address)
        #file_list.remove('dummy.txt')
        #print(file_list)
        #hold=input('hold')
        for i,temp_file in enumerate(file_list):
            print(temp_file)
            #if this is the first "fold result", then we want to 
            #drop the previous table. otherwise, just append
            if i == 0:
                make_update_table_from_panda(
                    table_18_base_address+temp_file,
                    engine,
                    'fold_results_'+temp_matrix_type,
                    [],
                    ('from_triplets', 'to_triplets', 'compound'),
                    [],
                    True,
                    temp_dtype_dict={
                        'from_triplets': postgresql.INTEGER,#postgresql.ARRAY(postgresql.TEXT), 
                        'to_triplets': postgresql.INTEGER,#postgresql.ARRAY(postgresql.TEXT),
                        'compound': postgresql.TEXT,
                        'to_triplets_inter_removed_if_nec': postgresql.FLOAT
                    },
                    temp_append_antisymmetric_result=18
                )
            elif i != 0:
                make_update_table_from_panda(
                    table_18_base_address+temp_file,
                    engine,
                    'fold_results_'+temp_matrix_type,
                    [],
                    ('from_triplets', 'to_triplets', 'compound'),
                    [],
                    False,
                    temp_dtype_dict={
                        'from_triplets': postgresql.INTEGER,#postgresql.ARRAY(postgresql.TEXT), 
                        'to_triplets': postgresql.INTEGER,#postgresql.ARRAY(postgresql.TEXT),
                        'compound': postgresql.TEXT,
                        'to_triplets_inter_removed_if_nec': postgresql.FLOAT
                    },
                    temp_append_antisymmetric_result=18
                )            
    print('18 done')

    #https://stackoverflow.com/questions/50626058/psycopg2-cant-adapt-type-numpy-int64
    register_adapter(np.int64, adapt_numpy_int64)
    
    print('19 starting')
    table_19_address='../results/'+str(min_fold_change)+'/step_19_prepare_count_matrix_2/count_matrix.bin'
    make_update_table_from_panda(
        table_19_address,
        engine,
        'unique_reduced_trip_list_to_properties',
        [],
        (['unique_triplets']),
        [],
        True,
        temp_dtype_dict={
            'unique_triplets': postgresql.INTEGER,#postgresql.ARRAY(postgresql.TEXT), 
            'triplet_count': postgresql.INTEGER, 
            'sample_count_list': postgresql.ARRAY(postgresql.INTEGER),
            'min_sample_count': postgresql.INTEGER, 
            'sum_sample_count': postgresql.INTEGER,
            'unique_triplet_list_real': postgresql.ARRAY(postgresql.TEXT)
        }
    )

    # def make_update_table_from_panda(
    #     temp_panda_address,
    #     temp_engine,
    #     temp_table_name,
    #     temp_columns_to_drop,
    #     temp_columns_for_primary_key,
    #     temp_columns_that_are_lists,
    #     temp_dtype_dict=None
    # ):

    print('19 done')
    table_20_base_address='../results/'+str(min_fold_change)+'/step_20_build_hierarchy_filter_tables/'
    file_list=os.listdir(table_20_base_address)
    file_list.remove('dummy.txt')
    file_list.remove('table_disease_dash.bin')
    file_list.remove('table_species_dash.bin')
    file_list.remove('table_organ_dash.bin')
    print(file_list)
    #hold=input('hold')
    


    for temp_file in file_list:
        make_update_table_from_panda(
            table_20_base_address+temp_file,
            engine,
            'hierarchy_filter_'+temp_file[:-4],
            [],
            (['node_id']),
            [],
            True,
            temp_dtype_dict={
                'node_id': postgresql.TEXT, 
                'we_map_to': postgresql.TEXT, 
                'distance_from_root': postgresql.INTEGER
            }
        )

    print('20 done')



    table_21_a_address='../results/'+str(min_fold_change)+'/step_21_b_create_compound_sod_property_tables/compound_property_table.bin'
    make_update_table_from_panda(
        table_21_a_address,
        engine,
        'compound_properties',
        [],
        (['identifier']),
        [],
        True,
        temp_dtype_dict={
            'identifier': postgresql.TEXT,
            'english_name': postgresql.TEXT
        }
    )

    table_21_b_address='../results/'+str(min_fold_change)+'/step_21_b_create_compound_sod_property_tables/species_property_table.bin'
    make_update_table_from_panda(
        table_21_b_address,
        engine,
        'species_properties',
        [],
        (['identifier']),
        [],
        True,
        temp_dtype_dict={
            'identifier': postgresql.TEXT,
            'english_name': postgresql.TEXT
        }
    )
    table_21_c_address='../results/'+str(min_fold_change)+'/step_21_b_create_compound_sod_property_tables/organ_property_table.bin'
    make_update_table_from_panda(
        table_21_c_address,
        engine,
        'organ_properties',
        [],
        (['identifier']),
        [],
        True,
        temp_dtype_dict={
            'identifier': postgresql.TEXT,
            'english_name': postgresql.TEXT
        }
    )
    table_21_d_address='../results/'+str(min_fold_change)+'/step_21_b_create_compound_sod_property_tables/disease_property_table.bin'
    make_update_table_from_panda(
        table_21_d_address,
        engine,
        'disease_properties',
        [],
        (['identifier']),
        [],
        True,
        temp_dtype_dict={
            'identifier': postgresql.TEXT,
            'english_name': postgresql.TEXT
        }
    )

    print('21 done')


    table_5_address='../results/'+str(min_fold_change)+'/step_5_b_make_non_ratio_table/non_ratio_table.bin'
    make_update_table_from_panda(
        table_5_address,
        engine,
        'non_ratio_table',
        [],
        (['bin','species','organ','disease']),
        [],
        True,
        temp_dtype_dict={
            'bin':postgresql.INTEGER,
            'compound':postgresql.TEXT,
            'species':postgresql.TEXT,
            'organ':postgresql.TEXT,
            'disease':postgresql.TEXT,
            'intensity_average':postgresql.FLOAT,
            'intensity_median':postgresql.FLOAT,
            'percent_present':postgresql.FLOAT
        }
    )
    print('5 done')

    connection.execute(
        f'''
        CREATE OR REPLACE VIEW public.combined_results
        AS SELECT foo_2.compound,
            foo_2.from_triplets,
            foo_2.to_triplets,
            foo_2.fold_average,
            foo_2.fold_median,
            foo_2.sig_mannwhit,
            frsmw.results AS sig_welch
        FROM ( SELECT foo_1.compound,
                    foo_1.from_triplets,
                    foo_1.to_triplets,
                    foo_1.fold_average,
                    foo_1.fold_median,
                    frsmm.results AS sig_mannwhit
                FROM ( SELECT frfcma.compound,
                            frfcma.from_triplets,
                            frfcma.to_triplets,
                            frfcma.results AS fold_average,
                            frfcmm.results AS fold_median
                        FROM fold_results_fold_change_matrix_average frfcma
                            JOIN fold_results_fold_change_matrix_median frfcmm ON frfcma.compound = frfcmm.compound AND frfcma.from_triplets = frfcmm.from_triplets AND frfcma.to_triplets = frfcmm.to_triplets) foo_1
                    JOIN fold_results_signifigance_matrix_mannwhitney frsmm ON foo_1.compound = frsmm.compound AND foo_1.from_triplets = frsmm.from_triplets AND foo_1.to_triplets = frsmm.to_triplets) foo_2
            JOIN fold_results_signifigance_matrix_welch frsmw ON foo_2.compound = frsmw.compound AND foo_2.from_triplets = frsmw.from_triplets AND foo_2.to_triplets = frsmw.to_triplets;
        '''
    )

    # def make_update_table_from_panda(
    #     temp_panda_address,
    #     temp_engine,
    #     temp_table_name,
    #     temp_columns_to_drop,
    #     temp_columns_for_primary_key,
    #     temp_columns_that_are_lists,
    #     temp_dtype_dict=None
    # ):

    #print('19 done')





    #connection.execute(
    #    'CREATE TABLE test (var INTEGER);'
    #)

    #reveal all tables
    #delete all tables
    #upsert the four pandas

    # temp_cursor=connection.execute(
    #     'SELECT * FROM pg_catalog.pg_tables;'
    # )

    #print(temp_cursor)
    #for element in temp_cursor:
    #    print(element)
    # print(temp_cursor.all())
    # print(temp_cursor.keys())
    '''
    temp_cursor2=connection.execute(
        'SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \'pg_catalog\';'
    )

    #print(temp_cursor)
    for element in temp_cursor2:
        print(element)
    '''

    # temp_cursor=connection.execute(
    #     '''SELECT * FROM information_schema.tables
    #         WHERE table_schema NOT IN (\'information_schema\',\'pg_catalog\') AND
    #             TABLE_TYPE = \'BASE_TABLE\'
    #     '''
    # )
    #print(temp_cursor)
    #at the moment, all prints nothing which i think makes sense because i have no tables that i made myself
    # pprint(temp_cursor.all())
    # pprint(temp_cursor.keys())

    # nothing=connection.execute(
    #     '''
    #     DROP TABLE my_step_16
    #     '''
    # )


    # my_table_name='my_step_16'
    # temp_cursor=connection.execute(
    #     f'''
    #     SELECT EXISTS (
    #         SELECT FROM information_schema.tables
    #         WHERE table_schema = 'public'
    #         AND table_name = '{my_table_name}'
    #     );
    #     '''
    # )
    # print(temp_cursor.first()[0])
    # hold=input('hold')

    # if (temp_cursor.first()[0]) == False:
    #     #if the table name doesnt already exist
    #     #use pandas to sql
    #     step_16=pandas.read_pickle(table_16_address)
    #     step_16.drop(['possible_triplets', 'actual_triplets', 'ratio'],axis='columns',inplace=True)
    #     print(step_16)
    #     print('------------------------------------------------------------------------------------------')
        
    #     #df['column_name'] = df['column_name'].apply(lambda x: x.tolist())
        
    #     step_16['triplet_list']=step_16['triplet_list'].apply(lambda x: x.tolist())
    #     step_16.to_sql(
    #         my_table_name,
    #         engine,
    #         index=False,
    #         dtype={
    #             'species_headnode': postgresql.TEXT,
    #             'organ_headnode': postgresql.TEXT,
    #             'disease_headnode': postgresql.TEXT,
    #             #'triplet_list': postgresql.TEXT[][]
    #             'triplet_list': postgresql.ARRAY(postgresql.TEXT)
    #         }
    #     )


    #     # '''
    #     #     SELECT * FROM information_schema.tables
    #     #     WHERE table_schema = 'PUBLIC'
    #     #     AND table_name = '{my_table_name}';
       
    #     # '''

    # hold=input('hold')

    # # -- Firstly, remove PRIMARY KEY attribute of former PRIMARY KEY
    # # ALTER TABLE <table_name> DROP CONSTRAINT <table_name>_pkey;
    # # -- Then change column name of  your PRIMARY KEY and PRIMARY KEY candidates properly.
    # # ALTER TABLE <table_name> RENAME COLUMN <primary_key_candidate> TO id;
    # # -- Lastly set your new PRIMARY KEY
    # # ALTER TABLE <table_name> ADD PRIMARY KEY (id);



    # connection.execute(
    #     f'''
    #     ALTER TABLE {my_table_name} ADD PRIMARY KEY (species_headnode, organ_headnode, disease_headnode)
    #     '''
    # )

    # #)
    # #print(temp_cursor.all())
    # #print(temp_cursor.keys())
    # #print(temp_cursor.first()[0])


