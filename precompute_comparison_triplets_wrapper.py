import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint
import time
import os
import sys

import multiprocessing

def identify_species_descendants(temp_headnode):
    #print('here')
    #print(type(temp_headnode))
    return nx.algorithms.dag.descendants(species_nx,temp_headnode)

def identify_organ_descendants(temp_headnode):
    return nx.algorithms.dag.descendants(organ_nx,temp_headnode)

def identify_disease_descendants(temp_headnode):
    return nx.algorithms.dag.descendants(disease_nx,temp_headnode)

def build_total_test_panda(temp_panda,temp_lowerbound,temp_upperbound):

    total_panda_dict={
        'species_headnode_from':[],
        'organ_headnode_from':[],
        'disease_headnode_from':[],
        'species_headnode_to':[],
        'organ_headnode_to':[],
        'disease_headnode_to':[],
        #'higher_species_headnode':[],
        #'higher_organ_headnode':[],
        #'higher_disease_headnode':[]
        'from_triplets':[],
        'to_triplets':[]
    }

    #species_set_subtraction_hashmap=build_set_subtraction_hashmap(temp_panda['species_headnode'],species_nx)


    index_length=len(temp_panda.index)
    print(index_length)
    #hold=input('hold')
    for index, series in temp_panda.iterrows():
        print(index)
        if index<temp_lowerbound:
            continue
        if index>=temp_upperbound:
            break

        #pprint(series['species_headnode'])
        total_panda_dict['species_headnode_from']=total_panda_dict['species_headnode_from']+[series['species_headnode'] for j in range(index+1,index_length)]
        #total_panda_dict['organ_headnode_from']
        #total_panda_dict['disease_headnode_from']
        total_panda_dict['organ_headnode_from']=total_panda_dict['organ_headnode_from']+[series['organ_headnode'] for j in range(index+1,index_length)]
        total_panda_dict['disease_headnode_from']=total_panda_dict['disease_headnode_from']+[series['disease_headnode'] for j in range(index+1,index_length)]


        #total_panda_dict['species_headnode_to']=total_panda_dict['species_headnode_to']
        #total_panda_dict['organ_headnode_to']=total_panda_dict['organ_headnode_to']
        #total_panda_dict['disease_headnode_to']=total_panda_dict['disease_headnode_to']


        #pprint(total_panda_dict)
        total_panda_dict['species_headnode_to']=total_panda_dict['species_headnode_to']+(temp_panda['species_headnode'][index+1:].to_list())
        total_panda_dict['organ_headnode_to']=total_panda_dict['organ_headnode_to']+(temp_panda['organ_headnode'][index+1:].to_list())
        total_panda_dict['disease_headnode_to']=total_panda_dict['disease_headnode_to']+(temp_panda['disease_headnode'][index+1:].to_list())
        #print(temp_panda['species_headnode'][index+1:].to_list())
        #print(temp_panda['species_headnode'][index+1:].to_list())
        #print(index)
        #print(len(temp_panda['species_headnode'][index+1:].to_list()))
        #print(len(total_panda_dict['species_headnode_from']))
        #print(series)
        
        total_panda_dict['from_triplets']=total_panda_dict['from_triplets']+[series['triplet_list'] for j in range(index+1,index_length)]
        total_panda_dict['to_triplets']=total_panda_dict['to_triplets']+(temp_panda['triplet_list'][index+1:].to_list())
        
        #hold=input('hold '+str(index_length))

        #
    
    #print(total_panda_dict['species_headnode_to'])
    
    total_panda=pd.DataFrame.from_dict(total_panda_dict)
    return total_panda


def identify_if_from_or_to_are_descendants_species(temp_from,temp_to,temp_species_set_subtraction_hashmap):
    if temp_from in temp_species_set_subtraction_hashmap[temp_to]:
        return 'from_descendant_of_to'
    elif temp_to in temp_species_set_subtraction_hashmap[temp_from]:
        return 'to_descendant_of_from'
    else:
        return 'neither'

def identify_if_from_or_to_are_descendants_organ(temp_from,temp_to,temp_organ_set_subtraction_hashmap):
    if temp_from in temp_organ_set_subtraction_hashmap[temp_to]:
        return 'from_descendant_of_to'
    elif temp_to in temp_organ_set_subtraction_hashmap[temp_from]:
        return 'to_descendant_of_from'
    else:
        return 'neither'
  
def identify_if_from_or_to_are_descendants_disease(temp_from,temp_to,temp_disease_set_subtraction_hashmap):
    if temp_from in temp_disease_set_subtraction_hashmap[temp_to]:
        return 'from_descendant_of_to'
    elif temp_to in temp_disease_set_subtraction_hashmap[temp_from]:
        return 'to_descendant_of_from'
    else:
        return 'neither'
    


def typecast_ndarray_to_set(temp_array):
    return {tuple(element) for element in temp_array}

#def remove_intersection_if_necessary_to(a,b,c,d,e,f,from_triplets,to_triplets,descendants_species,descendants_organ,descendants_disease):#
def remove_intersection_if_necessary_to(from_triplets,to_triplets,descendants_species,descendants_organ,descendants_disease):
    #print(from_triplets)
    #print(to_triplets)
    if (descendants_species=='from_descendant_of_to' or descendants_organ=='from_descendant_of_to' or descendants_disease=='from_descendant_of_to'):
        #print('interseciton removed')
        #hold=input('hold')
        #print(to_triplets.difference(from_triplets))
        #if len(to_triplets.difference(from_triplets))==0:
            #print(a)
            #print(b)
            #print(c)
            #print(d)
            #print(e)
            #print(f)
            #print(from_triplets)
            #print(to_triplets)
            #print(descendants_species)
            #print(descendants_organ)
            #print(descendants_disease)
            #hold=input('hold')
        
        return to_triplets.difference(from_triplets)
    else:
        #print('intersection not removed')
        return to_triplets

def remove_intersection_if_necessary_from(from_triplets,to_triplets,descendants_species,descendants_organ,descendants_disease):#
    if (descendants_species=='to_descendant_of_from' or descendants_organ=='to_descendant_of_from' or descendants_disease=='to_descendant_of_from'):
        return from_triplets.difference(to_triplets)
    else:
        return from_triplets

def pseudo_main(chunk_counter):

    this_executions_lower_bound=chunk_counter*1000
    this_executions_upper_bound=(chunk_counter*1000)+1000

    #min_fold_change=1
    input_panda_address='../results/'+str(min_fold_change)+'/step_16_calculate_fraction_triplets/triplet_count_panda.bin'
    species_nx_input_address='../results/'+str(min_fold_change)+'/step_14_reduce_hierarchy_complexity_post_dash/species_networkx.bin'
    organ_nx_input_address='../results/'+str(min_fold_change)+'/step_14_reduce_hierarchy_complexity_post_dash/organ_networkx.bin'
    disease_nx_input_address='../results/'+str(min_fold_change)+'/step_14_reduce_hierarchy_complexity_post_dash/disease_networkx.bin'
    unique_triplets_output_address='../results/'+str(min_fold_change)+'/step_17_precompute_comparison_triplets/chunks/unique/unique_triplets'+str(this_executions_lower_bound)+'.bin'
    triplet_headnode_to_triplet_tuple_ouput_address='../results/'+str(min_fold_change)+'/step_17_precompute_comparison_triplets/chunks/mapping/headnodes_to_triplet_list'+str(this_executions_lower_bound)+'.bin'

    species_nx=nx.readwrite.gpickle.read_gpickle(species_nx_input_address)
    organ_nx=nx.readwrite.gpickle.read_gpickle(organ_nx_input_address)
    disease_nx=nx.readwrite.gpickle.read_gpickle(disease_nx_input_address)


    #read in panda
    input_panda=pd.read_pickle(input_panda_address)

    input_panda=input_panda.loc[input_panda['actual_triplets'].gt(0)].copy()

    #remove superfluous columns
    input_panda.drop(['actual_triplets','ratio'],inplace=True,axis='columns')
    input_panda.reset_index(inplace=True)
    print(input_panda)

    print(type(input_panda.at[9,'triplet_list']))

    #input_panda['triplet_list']=input_panda['triplet_list'].astype(set)
    input_panda['triplet_list']=input_panda['triplet_list'].apply(typecast_ndarray_to_set)
    #input_panda['species_headnode']=input_panda['species_headnode'].astype(str)

    print(input_panda['species_headnode'])


    #nx.draw(species_nx,with_labels=True)
    #plt.show()
    total_panda=build_total_test_panda(input_panda,this_executions_lower_bound,this_executions_upper_bound)
    
   
    
    
    print(total_panda)
    #total_panda.to_pickle('/home/rictuar/delete_test_bin_calc/panda')

    species_set_subtraction_hashmap_values=input_panda['species_headnode'].apply(identify_species_descendants)
    species_set_subtraction_hashmap=dict(zip(input_panda['species_headnode'],species_set_subtraction_hashmap_values))
    
    total_panda['descendants_species']=total_panda.apply(
        lambda x: identify_if_from_or_to_are_descendants_species(x['species_headnode_from'],x['species_headnode_to'],species_set_subtraction_hashmap),
        axis='columns'
    )
    print(species_set_subtraction_hashmap)

    print(total_panda['descendants_species'].value_counts())
    


    organ_set_subtraction_hashmap_values=input_panda['organ_headnode'].apply(identify_organ_descendants)
    organ_set_subtraction_hashmap=dict(zip(input_panda['organ_headnode'],organ_set_subtraction_hashmap_values))
    
    total_panda['descendants_organ']=total_panda.apply(
        lambda x: identify_if_from_or_to_are_descendants_organ(x['organ_headnode_from'],x['organ_headnode_to'],organ_set_subtraction_hashmap),
        axis='columns'
    )
    print(organ_set_subtraction_hashmap)

    print(total_panda['descendants_organ'].value_counts())




    disease_set_subtraction_hashmap_values=input_panda['disease_headnode'].apply(identify_disease_descendants)
    disease_set_subtraction_hashmap=dict(zip(input_panda['disease_headnode'],disease_set_subtraction_hashmap_values))
    
    total_panda['descendants_disease']=total_panda.apply(
        lambda x: identify_if_from_or_to_are_descendants_disease(x['disease_headnode_from'],x['disease_headnode_to'],disease_set_subtraction_hashmap),
        axis='columns'
    )
    print(disease_set_subtraction_hashmap)

    print(total_panda['descendants_disease'].value_counts())
    
    print(total_panda)
    
    total_panda['to_triplets_inter_removed_if_nec']=total_panda.apply(
        lambda x: remove_intersection_if_necessary_to(

            x['from_triplets'],
            x['to_triplets'],
            x['descendants_species'],
            x['descendants_organ'],
            x['descendants_disease']
        ),
        axis='columns'
    )

    total_panda['from_triplets_inter_removed_if_nec']=total_panda.apply(
        lambda x: remove_intersection_if_necessary_from(
            x['from_triplets'],
            x['to_triplets'],
            x['descendants_species'],
            x['descendants_organ'],
            x['descendants_disease']
        ),
        axis='columns'
    )

    

    total_panda['to_triplets_inter_removed_if_nec']=total_panda['to_triplets_inter_removed_if_nec'].transform(list)
    total_panda['from_triplets_inter_removed_if_nec']=total_panda['from_triplets_inter_removed_if_nec'].transform(list)


    total_panda['to_triplets_inter_removed_if_nec']=total_panda['to_triplets_inter_removed_if_nec'].apply(lambda x: sorted(x))
    total_panda['from_triplets_inter_removed_if_nec']=total_panda['from_triplets_inter_removed_if_nec'].apply(lambda x: sorted(x))

    total_panda['to_triplets_inter_removed_if_nec']=total_panda['to_triplets_inter_removed_if_nec'].transform(tuple)
    total_panda['from_triplets_inter_removed_if_nec']=total_panda['from_triplets_inter_removed_if_nec'].transform(tuple)


    test_view=total_panda.loc[(total_panda['to_triplets_inter_removed_if_nec'] != ()) & (total_panda['from_triplets_inter_removed_if_nec'] != ())].copy()
    test_view.reset_index(inplace=True)
    print(test_view)


    test_view['headnode_triplet_from']=tuple(zip(test_view['species_headnode_from'],test_view['organ_headnode_from'],test_view['disease_headnode_from']))
    test_view['headnode_triplet_to']=tuple(zip(test_view['species_headnode_to'],test_view['organ_headnode_to'],test_view['disease_headnode_to']))



    #test_view[['headnode_triplet_from','headnode_triplet_to','from_triplets_inter_removed_if_nec','to_triplets_inter_removed_if_nec']].to_pickle(triplet_headnode_to_triplet_tuple_ouput_address)
    test_view[['species_headnode_from','organ_headnode_from','disease_headnode_from','species_headnode_to','organ_headnode_to','disease_headnode_to','from_triplets_inter_removed_if_nec','to_triplets_inter_removed_if_nec']].to_pickle(triplet_headnode_to_triplet_tuple_ouput_address)
    
    test_view['combo_column']=(list(zip(
        test_view['to_triplets_inter_removed_if_nec'],#.transform(tuple),#.unique(),
        test_view['from_triplets_inter_removed_if_nec']#.transform(tuple)#.unique()
    )))
    #print(test_view)
    #print(test_view['combo_column'])

    print(len(test_view['combo_column'].unique()))
    print(len(test_view['to_triplets_inter_removed_if_nec'].unique()))
    print(len(test_view['from_triplets_inter_removed_if_nec'].unique()))

    output_series=pd.DataFrame(test_view['combo_column'].unique())
    output_series=output_series.assign(**dict(zip('ft', output_series[0].str)))
    print(output_series)
    output_series.drop(0,axis='columns',inplace=True)
    print(output_series)

    #hold=input('hold2')
    output_series.rename({'f': 'from','t':'to'},axis='columns',inplace=True)
    


    print(output_series)

    output_series.sort_values(by='from',inplace=True)
    print(output_series)
    output_series.to_pickle(unique_triplets_output_address)





if __name__=="__main__":
    min_fold_change=sys.argv[1]
    num_processes=int(sys.argv[2])
    #defined here to provide globals##
    species_nx_input_address='../results/'+str(min_fold_change)+'/step_14_reduce_hierarchy_complexity_post_dash/species_networkx.bin'
    organ_nx_input_address='../results/'+str(min_fold_change)+'/step_14_reduce_hierarchy_complexity_post_dash/organ_networkx.bin'
    disease_nx_input_address='../results/'+str(min_fold_change)+'/step_14_reduce_hierarchy_complexity_post_dash/disease_networkx.bin'
    #unique_triplets_output_address='../results/'+str(min_fold_change)+'/step_17_precompute_comparison_triplets/chunks/unique_triplets'+str(this_executions_lower_bound)+'.bin'
    #triplet_headnode_to_triplet_tuple_ouput_address='../results/'+str(min_fold_change)+'/step_17_precompute_comparison_triplets/chunks/headnodes_to_triplet_list'+str(this_executions_lower_bound)+'.bin'

    species_nx=nx.readwrite.gpickle.read_gpickle(species_nx_input_address)
    organ_nx=nx.readwrite.gpickle.read_gpickle(organ_nx_input_address)
    disease_nx=nx.readwrite.gpickle.read_gpickle(disease_nx_input_address)
    ###


    

    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_17_precompute_comparison_triplets/chunks/unique/')
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_17_precompute_comparison_triplets/chunks/mapping/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_17_precompute_comparison_triplets/dummy.txt')
 
    input_panda_address='../results/'+str(min_fold_change)+'/step_16_calculate_fraction_triplets/triplet_count_panda.bin'
    temp=pd.read_pickle(input_panda_address)
    row_count=len(temp.index)
    print(temp)

    
    #list_of_starting_indices_and_ending_indices=list()
    #print(row_count)
    #print(row_count//1000)
    list_of_starting_index_counters=[i for i in range(1+(row_count//1000))]

    #for i in range(row_count//1000):
    #    list_of_starting_indices_and_ending_indices.append((i*1000,(i*1000)+1000))
    #print(list_of_starting_indices_and_ending_indices)
    #list_of_starting_indices_and_ending_indices.append( ((row_count//1000)*1000,row_count)  )
    #print(list_of_starting_indices_and_ending_indices)
    
    ###multiprocessing sending starting and ending indices to precompute

    
    #chunk_size = list_of_starting_index_counters//num_processes
    #panda_chunks=list()
    #for i in range(0,num_processes):
    #chunks = [post_species_transform_panda.iloc[post_species_transform_panda[i:i + chunk_size]] for i in range(0, post_species_transform_panda.shape[0], chunk_size)]
        #if i<(num_processes-1):
            #panda_chunks.append(post_species_transform_panda.iloc[i*chunk_size:(i+1)*chunk_size])
        #elif i==(num_processes-1):
            #panda_chunks.append(post_species_transform_panda.iloc[i*chunk_size:])
    #print(panda_chunks)
    #hold=input('check chunks')
    pool = multiprocessing.Pool(processes=num_processes)
    #transformed_chunks=
    pool.map(pseudo_main,list_of_starting_index_counters)
    #transform_organ_column(post_species_transform_panda)
    #recombine_chunks
    #for i in range(len(transformed_chunks)):
    #    post_species_transform_panda.iloc[transformed_chunks[i].index]=transformed_chunks[i]
    #post_species_transform_panda=pd.concat(transformed_chunks)

    pool.close()

    unique_base_address='../results/'+str(min_fold_change)+'/step_17_precompute_comparison_triplets/chunks/unique/'
    unique_result_chunk_list=os.listdir(unique_base_address)
    unique_result_panda=pd.read_pickle(unique_base_address+unique_result_chunk_list[0])
    for i in range(1,len(unique_result_chunk_list)):
        temp_panda=pd.read_pickle(unique_base_address+unique_result_chunk_list[i])
        unique_result_panda=pd.concat([unique_result_panda,temp_panda],axis='index',ignore_index=True)
        unique_result_panda=unique_result_panda.drop_duplicates(ignore_index=True)
    unique_result_panda.to_pickle('../results/'+str(min_fold_change)+'/step_17_precompute_comparison_triplets/unique_triplets.bin')


    mapping_base_address='../results/'+str(min_fold_change)+'/step_17_precompute_comparison_triplets/chunks/mapping/'
    mapping_result_chunk_list=os.listdir(mapping_base_address)
    mapping_result_panda=pd.read_pickle(mapping_base_address+mapping_result_chunk_list[0])
    for i in range(1,len(mapping_result_chunk_list)):
        temp_panda=pd.read_pickle(mapping_base_address+mapping_result_chunk_list[i])
        mapping_result_panda=pd.concat([mapping_result_panda,temp_panda],axis='index',ignore_index=True)
        #mapping_result_panda=mapping_result_panda.drop_duplicates(ignore_index=True)
    mapping_result_panda.to_pickle('../results/'+str(min_fold_change)+'/step_17_precompute_comparison_triplets/headnodes_to_triplet_list.bin')
