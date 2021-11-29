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
    
    print(temp_panda)
    hold=input('hold')

    temp_panda.drop(temp_columns_to_drop,inplace=True,axis='columns')

    #this is because we expected numpy arrays
    # for temp_column in temp_columns_that_are_lists:
    #     try:
    #         temp_panda[temp_column]=temp_panda[temp_column].apply(lambda x: x.tolist())
    #     except AttributeError:
    #         continue
            

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


    
    my_server='info-from-binvestigate.czbab8f7pgfj.us-east-2.rds.amazonaws.com'
    my_database='binvestigate'
    my_dialect='postgresql'
    my_driver='psycopg2'
    my_username='postgres'
    my_password='elaine123'


    my_connection=f'{my_dialect}+{my_driver}://{my_username}:{my_password}@{my_server}/{my_database}'


    engine=create_engine(my_connection)#,echo=True)
    connection=engine.connect()



    pseudo_carrot_view_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/binvestigate_pull/shortened_file_for_test_protocol_5.bin'
    #table_16_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/1/step_16_calculate_fraction_triplets/triplet_count_panda.bin'
    make_update_table_from_panda(
        pseudo_carrot_view_address,
        engine,
        'pseudo_carrot',
        [],
        ('id',),
        #['triplet_list'],
        ['spectra_mz','spectra_intensity','species','organ','count','intensity'],
        temp_dtype_dict={

            'id' :postgresql.FLOAT,
            'name' : postgresql.TEXT,
            'retentionIndex' :postgresql.FLOAT,
            'kovats': postgresql.FLOAT,
            'quantMass' :postgresql.FLOAT,
            'splash': postgresql.TEXT,
            'purity' :postgresql.FLOAT,
            'uniqueMass' :postgresql.FLOAT,
            'sample' : postgresql.TEXT,
            'spectra_mz': postgresql.ARRAY(postgresql.FLOAT),
            'spectra_intensity':postgresql.ARRAY(postgresql.FLOAT),
            '_id' : postgresql.TEXT,
            'species': postgresql.ARRAY(postgresql.TEXT),
            'organ': postgresql.ARRAY(postgresql.TEXT),
            'count': postgresql.ARRAY(postgresql.FLOAT),
            'intensity' :postgresql.ARRAY(postgresql.FLOAT),
            'group' : postgresql.TEXT,
            'inchikey' : postgresql.TEXT,       
        }
    )
