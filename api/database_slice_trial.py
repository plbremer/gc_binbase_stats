from sqlalchemy import create_engine
from sqlalchemy import Table, String
from sqlalchemy.dialects import postgresql

'''
{'additional_slider': [1, 5], 
'additional_toggleswitch': [True, True], 
'aggregate_on_page_rangeslider': None, 
'aggregate_on_page_spinners': 2, 
'compounds': [['CHEMONTID:0000001', '2', '12'], ['CHEMONTID:0000001', '2', '12']], 
'from_disease': [['C06.405.469.491.307', 'C06.301.623', 'C06.689.667', 'C06.405.469.860.180', 'C06.405.249.411.307.180', 'C06.552.697.160', 'C06.301.371.411.307.180', 'C06.301.371.411.307', 'C06.301.761', 'C06.405.469.158.356', 'C06.405.469.158.356.180', 'C06.405.249.411.307', 'C06', 'C06.301.623.160', 'C06.405.469.491.307.180', 'C06.552.697', 'No', 'disease'], ['C06.405.469.491.307', 'C06.301.623', 'C06.689.667', 'C06.405.469.860.180', 'C06.405.249.411.307.180', 'C06.552.697.160', 'C06.301.371.411.307.180', 'C06.301.371.411.307', 'C06.301.761', 'C06.405.469.158.356', 'C06.405.469.158.356.180', 'C06.405.249.411.307', 'C06', 'C06.301.623.160', 'C06.405.469.491.307.180', 'C06.552.697', 'No', 'disease']], 
'from_organ': [['A11.872', 'A11.872.700.250', 'A11.872.700.250.875', 'A11.872.378', 'A11.872.040.500', 'A11.872.700.500', 'A11.872.590.500'], ['A11.872', 'A11.872.700.250', 'A11.872.700.250.875', 'A11.872.378', 'A11.872.040.500', 'A11.872.700.500', 'A11.872.590.500']], 
'from_species': [['9606'], ['9606']], 
'to_disease': [['C06.405.469.491.307', 'C06.301.623', 'C06.689.667', 'C06.405.469.860.180', 'C06.405.249.411.307.180', 'C06.552.697.160', 'C06.301.371.411.307.180', 'C06.301.371.411.307', 'C06.301.761', 'C06.405.469.158.356', 'C06.405.469.158.356.180', 'C06.405.249.411.307', 'C06', 'C06.301.623.160', 'C06.405.469.491.307.180', 'C06.552.697', 'No', 'disease'], ['C06.405.469.491.307', 'C06.301.623', 'C06.689.667', 'C06.405.469.860.180', 'C06.405.249.411.307.180', 'C06.552.697.160', 'C06.301.371.411.307.180', 'C06.301.371.411.307', 'C06.301.761', 'C06.405.469.158.356', 'C06.405.469.158.356.180', 'C06.405.249.411.307', 'C06', 'C06.301.623.160', 'C06.405.469.491.307.180', 'C06.552.697', 'No', 'disease']], 
'to_organ': [['A11.872', 'A11.872.700.250', 'A11.872.700.250.875', 'A11.872.378', 'A11.872.040.500', 'A11.872.700.500', 'A11.872.590.500'], ['A11.872', 'A11.872.700.250', 'A11.872.700.250.875', 'A11.872.378', 'A11.872.040.500', 'A11.872.700.500', 'A11.872.590.500']], 
'to_species': [['10090'], ['10117', '10116', '10114']]}
'''

def build_single_from_to_filter(temp_compounds, temp_from_s,temp_from_o,temp_from_d,temp_to_s,temp_to_o,temp_to_d,temp_fold_min):

    

    temp_compound_string=temp_compounds.join('')
    # temp_from_s_string
    # temp_from_o_string
    # temp_from_d_string
    # temp_to_s_string
    # temp_to_o_string
    # temp_to_d_string
    # temp_fold_min_string

    temp_query_string='''
    select from_head_spec, from_head_org, from_head_dis, to_head_spec, to_head_org, to_head_dis, comp, from_triplets_inter_removed_if_nec, to_triplets_inter_removed_if_nec, results from (

        (

            select from_head_spec, from_head_org, from_head_dis, to_head_spec, to_head_org, to_head_dis, comp, from_triplets_inter_removed_if_nec, to_triplets_inter_removed_if_nec from 
            (
                (
                    (
                        
                        select from_head_spec,from_head_org,from_head_dis,to_head_spec,to_head_org,to_head_dis from (
                            (
                                unnest(array['1129']) as from_head_spec 
                                cross join 
                                unnest(array['A11']) as from_head_org
                                cross join
                                unnest(array['No']) as from_head_dis
                            ) unnest_result_from

                            inner join 
                            
                            headnodes_to_triplets AS htt_from
                                on
                                from_head_spec=htt_from.species_headnode
                                AND
                                from_head_org=htt_from.organ_headnode
                                AND
                                from_head_dis=htt_from.disease_headnode
                        ) trips_from

                        cross join 

                        (
                            (
                                unnest(array['2093','1783272']) as to_head_spec 
                                cross join 
                                unnest(array['A11']) as to_head_org
                                cross join
                                unnest(array['No']) as to_head_dis
                            ) unnest_result_to 
                            inner join 
                            headnodes_to_triplets AS htt_to
                                on
                                to_head_spec=htt_to.species_headnode
                                AND
                                to_head_org=htt_to.organ_headnode
                                AND
                                to_head_dis=htt_to.disease_headnode
                        ) trips_to

                    ) triplets_from_and_to

                    cross join

                    unnest(array['CHEMONTID:0000001', '2', '12'] ) as comp
                ) from_and_to_and_comp
                
                inner join
                
                headnode_pairs_to_triplet_list_pair 
                on
                species_headnode_from = from_head_spec AND
                organ_headnode_from = from_head_org AND
                disease_headnode_from = from_head_dis AND
                species_headnode_to = to_head_spec AND
                organ_headnode_to = to_head_org AND
                disease_headnode_to = to_head_dis
            ) 
        ) from_and_to_and_comp_to_triplets

        inner join

        fold_results
        on
        from_triplets_inter_removed_if_nec = from_triplets AND
        to_triplets_inter_removed_if_nec = to_triplets AND
        comp = compound
    )

    where

    results > 50
    '''




if __name__ == "__main__":

    additional_slider: [1, 5], 
    additional_toggleswitch: [True, True], 
    #aggregate_on_page_rangeslider: None, 
    #aggregate_on_page_spinners: 2, 
    compounds: [['CHEMONTID:0000001', '2', '12'], ['CHEMONTID:0000001', '2', '12']], 
    from_disease: [['C06.405.469.491.307', 'C06.301.623', 'C06.689.667', 'C06.405.469.860.180', 'C06.405.249.411.307.180', 'C06.552.697.160', 'C06.301.371.411.307.180', 'C06.301.371.411.307', 'C06.301.761', 'C06.405.469.158.356', 'C06.405.469.158.356.180', 'C06.405.249.411.307', 'C06', 'C06.301.623.160', 'C06.405.469.491.307.180', 'C06.552.697', 'No', 'disease'], ['C06.405.469.491.307', 'C06.301.623', 'C06.689.667', 'C06.405.469.860.180', 'C06.405.249.411.307.180', 'C06.552.697.160', 'C06.301.371.411.307.180', 'C06.301.371.411.307', 'C06.301.761', 'C06.405.469.158.356', 'C06.405.469.158.356.180', 'C06.405.249.411.307', 'C06', 'C06.301.623.160', 'C06.405.469.491.307.180', 'C06.552.697', 'No', 'disease']], 
    from_organ: [['A11.872', 'A11.872.700.250', 'A11.872.700.250.875', 'A11.872.378', 'A11.872.040.500', 'A11.872.700.500', 'A11.872.590.500'], ['A11.872', 'A11.872.700.250', 'A11.872.700.250.875', 'A11.872.378', 'A11.872.040.500', 'A11.872.700.500', 'A11.872.590.500']], 
    from_species: [['9606'], ['9606']], 
    to_disease: [['C06.405.469.491.307', 'C06.301.623', 'C06.689.667', 'C06.405.469.860.180', 'C06.405.249.411.307.180', 'C06.552.697.160', 'C06.301.371.411.307.180', 'C06.301.371.411.307', 'C06.301.761', 'C06.405.469.158.356', 'C06.405.469.158.356.180', 'C06.405.249.411.307', 'C06', 'C06.301.623.160', 'C06.405.469.491.307.180', 'C06.552.697', 'No', 'disease'], ['C06.405.469.491.307', 'C06.301.623', 'C06.689.667', 'C06.405.469.860.180', 'C06.405.249.411.307.180', 'C06.552.697.160', 'C06.301.371.411.307.180', 'C06.301.371.411.307', 'C06.301.761', 'C06.405.469.158.356', 'C06.405.469.158.356.180', 'C06.405.249.411.307', 'C06', 'C06.301.623.160', 'C06.405.469.491.307.180', 'C06.552.697', 'No', 'disease']], 
    to_organ: [['A11.872', 'A11.872.700.250', 'A11.872.700.250.875', 'A11.872.378', 'A11.872.040.500', 'A11.872.700.500', 'A11.872.590.500'], ['A11.872', 'A11.872.700.250', 'A11.872.700.250.875', 'A11.872.378', 'A11.872.040.500', 'A11.872.700.500', 'A11.872.590.500']], 
    to_species: [['10090'], ['10117', '10116', '10114']]}



    my_server='localhost'
    my_database='binvestigate_first'
    my_dialect='postgresql'
    my_driver='psycopg2'
    my_username='rictuar'
    my_password='elaine123'

    my_connection=f'{my_dialect}+{my_driver}://{my_username}:{my_password}@{my_server}/{my_database}'

    engine=create_engine(my_connection)#,echo=True)
    connection=engine.connect()



    #first database connection test
    temp_cursor=connection.execute(
        f'''
        
        '''
    )

