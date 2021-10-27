from sqlalchemy import create_engine
from sqlalchemy import Table, String
from sqlalchemy.dialects import postgresql
import pandas
from pprint import pprint
import os

from sqlalchemy.sql.sqltypes import TEXT


def make_update_table_from_panda(
    temp_panda_address,
    temp_engine,
    temp_table_name,
    temp_columns_to_drop,
    temp_columns_for_primary_key,
    temp_columns_that_are_lists,
    temp_dtype_dict=None
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
    
    temp_panda.drop(temp_columns_to_drop,inplace=True,axis='columns')

    for temp_column in temp_columns_that_are_lists:
        # try:
        temp_panda[temp_column]=temp_panda[temp_column].apply(lambda x: x.tolist())
        # except AttributeError:
        #     continue
            

    temp_cursor=connection.execute(
        f'''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = '{temp_table_name}'
        );
        '''
    )

    #if the table does not already exist
    if (temp_cursor.first()[0]) == False:
        temp_panda.to_sql(
            temp_table_name,
            engine,
            index=False,
            dtype=temp_dtype_dict
        )
        temp_big_string=', '.join(temp_columns_for_primary_key)
        temp_big_string='('+temp_big_string+')'
        connection.execute(
            f'''
            ALTER TABLE {temp_table_name} ADD PRIMARY KEY {temp_big_string};
            '''
        )
    else:
        to_be_upserted='to_be_upserted'
        temp_panda.to_sql(
            to_be_upserted,
            engine,
            index=False,
            dtype=temp_dtype_dict
        )
        temp_big_string=', '.join(temp_columns_for_primary_key)
        temp_big_string='('+temp_big_string+')'
        connection.execute(
            f'''
            ALTER TABLE {to_be_upserted} ADD PRIMARY KEY {temp_big_string};
            '''
        )
        temp_big_string=', '.join(temp_panda.columns)
        temp_big_string='('+temp_big_string+')'
        connection.execute(
            f'''
            INSERT INTO {temp_table_name} 
            SELECT * from {to_be_upserted};
            '''
            #SELECT {temp_big_string} FROM {to_be_upserted};
        )
        connection.execute(
            f'''
            DROP TABLE {to_be_upserted};
            '''
        )       
    
        # INSERT INTO "{table_name}" ({headers_sql_txt}) 
        # SELECT {headers_sql_txt} FROM "{temp_table_name}"



if __name__ == "__main__":


    
    my_server='localhost'
    my_database='binvestigate_first'
    my_dialect='postgresql'
    my_driver='psycopg2'
    my_username='rictuar'
    my_password='elaine123'


    my_connection=f'{my_dialect}+{my_driver}://{my_username}:{my_password}@{my_server}/{my_database}'


    engine=create_engine(my_connection)#,echo=True)
    connection=engine.connect()

    table_16_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/1/step_16_calculate_fraction_triplets/triplet_count_panda.bin'
    # make_update_table_from_panda(
    #     table_16_address,
    #     engine,
    #     'headnodes_to_triplets',
    #     ['possible_triplets', 'actual_triplets', 'ratio'],
    #     ('species_headnode', 'organ_headnode', 'disease_headnode'),
    #     ['triplet_list'],
    #     temp_dtype_dict={
    #         'species_headnode': postgresql.TEXT,
    #         'organ_headnode': postgresql.TEXT,
    #         'disease_headnode': postgresql.TEXT,
    #         'triplet_list': postgresql.ARRAY(postgresql.TEXT)            
    #     }
    # )




    
    # table_17_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/1/step_17_precompute_comparison_triplets/headnodes_to_triplet_list.bin'
    # make_update_table_from_panda(
    #     table_17_address,
    #     engine,
    #     'headnode_pairs_to_triplet_list_pair',
    #     [],
    #     ('headnode_triplet_from', 'headnode_triplet_to'),
    #     [],
    #     temp_dtype_dict={
    #         'headnode_triplet_from': postgresql.ARRAY(postgresql.TEXT), 
    #         'headnode_triplet_to': postgresql.ARRAY(postgresql.TEXT),
    #         'from_triplets_inter_removed_if_nec': postgresql.ARRAY(postgresql.TEXT),
    #         'to_triplets_inter_removed_if_nec': postgresql.ARRAY(postgresql.TEXT)
    #     }
    # )
    

    table_18_base_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/1/step_18_compute_fold_results/'
    file_list=os.listdir(table_18_base_address)
    file_list.remove('dummy.txt')
    print(file_list)
    #hold=input('hold')



    for temp_file in file_list:
        make_update_table_from_panda(
            table_18_base_address+temp_file,
            engine,
            'fold_results',
            [],
            ('from_triplets', 'to_triplets', 'compound'),
            [],
            temp_dtype_dict={
                'from_triplets': postgresql.ARRAY(postgresql.TEXT), 
                'to_triplets': postgresql.ARRAY(postgresql.TEXT),
                'compound': postgresql.TEXT,
                'to_triplets_inter_removed_if_nec': postgresql.FLOAT
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


