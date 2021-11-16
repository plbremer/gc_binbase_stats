import json
from pprint import pprint

class ComplicatedQuery():

    def init():
        pass

    def assign_rest_api_net_query(self, temp_data_from_post):
        self.net_query=temp_data_from_post
        #print(self.net_query)
        
    def assign_from_to_metadata(self):
        # self.from_species=self.net_query['from_species']
        # self.from_organ=self.net_query['from_organ']
        # self.from_disease=self.net_query['from_disease']
        # self.to_species=self.net_query['to_species']
        # self.to_organ=self.net_query['to_organ']
        # self.to_disease=self.net_query['to_disease']
        self.from_to_dict={
            'from_species':self.net_query['from_species'],
            'from_organ':self.net_query['from_organ'],
            'from_disease':self.net_query['from_disease'],
            'to_species':self.net_query['to_species'],
            'to_organ':self.net_query['to_organ'],
            'to_disease':self.net_query['to_disease'],
            'min_fold_change':self.net_query['additional_slider_min_fold_change']          
        }

    def create_from_to_query_string(self):
        
        temp_string_dict={
            'from_species':list(),
            'from_organ':list(),
            'from_disease':list(),
            'to_species':list(),
            'to_organ':list(),
            'to_disease':list(),
            'min_fold_change':list()
        }

        pprint(self.from_to_dict)
        
        for temp_key in temp_string_dict.keys():
            #print(temp_key)
            for i in range(len(self.from_to_dict[temp_key])):
                #print(i)
                if temp_key=='min_fold_change':
                    #print(str(self.from_to_dict[temp_key]))
                    temp_string_dict[temp_key].append( str(self.from_to_dict[temp_key][i]) )
                
                #print(self.from_to_dict[temp_key][i])
                else:
                    #print(','.join(['\''+x+'\'' for x in self.from_to_dict[temp_key][i]]))
                    temp_string_dict[temp_key].append( (','.join(['\''+x+'\'' for x in self.from_to_dict[temp_key][i]])) )

        #pprint(temp_string_dict)

        full_query_string=''
        for i in range(len(temp_string_dict['from_species'])):
            temp_from_species=temp_string_dict['from_species'][i]
            temp_from_organ=temp_string_dict['from_organ'][i]
            temp_from_disease=temp_string_dict['from_disease'][i]
            temp_to_species=temp_string_dict['to_species'][i]
            temp_to_organ=temp_string_dict['to_organ'][i]
            temp_to_disease=temp_string_dict['to_disease'][i]            
            temp_min_fold_change=temp_string_dict['min_fold_change'][i]   

            temp_query_string=f'''
                select from_head_spec, from_head_org, from_head_dis, to_head_spec, to_head_org, to_head_dis, comp, from_triplets_inter_removed_if_nec, to_triplets_inter_removed_if_nec, results from (
                    (
                        select from_head_spec, from_head_org, from_head_dis, to_head_spec, to_head_org, to_head_dis, comp, from_triplets_inter_removed_if_nec, to_triplets_inter_removed_if_nec from 
                        (
                            (
                                (
                                    select from_head_spec,from_head_org,from_head_dis,to_head_spec,to_head_org,to_head_dis from (
                                        (
                                            unnest(array[{temp_from_species}]) as from_head_spec 
                                            cross join 
                                            unnest(array[{temp_from_organ}]) as from_head_org
                                            cross join
                                            unnest(array[{temp_from_disease}]) as from_head_dis
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
                                            unnest(array[{temp_to_species}]) as to_head_spec 
                                            cross join 
                                            unnest(array[{temp_to_organ}]) as to_head_org
                                            cross join
                                            unnest(array[{temp_to_disease}]) as to_head_dis
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
                                unnest(array[] ) as comp
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
                ) as temp_{str(i)}
                where
                results > {temp_min_fold_change}
                '''
        
            full_query_string+=temp_query_string

            #if we are on any loop but last
            if (i+1 <(len(temp_string_dict['from_species']))):
                


        #print(full_query_string)

        self.full_query_string=full_query_string




    #self.portion_from_to_metadata=temp_data_from_post

    

if __name__ == "__main__":

    temp_incoming_json_string='{"additional_slider_min_fold_change": [5], "additional_toggleswitch": [true], "aggregate_on_page_rangeslider": null, "aggregate_on_page_spinners": 1, "compounds": [["18"]], "from_disease": [["No"]], "from_organ": [["A18.024.937"]], "from_species": [["161934"]], "to_disease": [["No"]], "to_organ": [["A12.207.152", "A12.207.152.693", "A12.207.152.846"]], "to_species": [["15367", "147368", "204232"]]}'

    temp_incoming_json=json.loads(temp_incoming_json_string)
    pprint(temp_incoming_json)
    print('################################################')

    my_ComplicatedQuery=ComplicatedQuery()
    my_ComplicatedQuery.assign_rest_api_net_query(temp_incoming_json)
    my_ComplicatedQuery.assign_from_to_metadata()
    my_ComplicatedQuery.create_from_to_query_string()

