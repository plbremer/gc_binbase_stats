'''
At some point i realized that many of the results of hiearchical headnodes depended only on whether or not
one or more triplets existed depending on the headnode choice

this script accepts the panda that describes the triplets that are implied by each possible headnode combination
many of these headnode combinations imply zero triplets

this script takes the aforementiond panda
it drops all rows where zero triplets are implied by the headnode combination

we recognize that every headnode combination can be tested against every headnode combination (from vs to)


we start with a list of headnode combinations
for every headnode combination (from), we append append a list of that headnode combination's index to the end of the list of headnode combinations (to)
(we start at the current index for the from because the fold matrix is "anti symmetric" (lower diagonal is negative of upper diagonal))

then, for every single from vs to combinations (# of headnode triplets * ((1/2)*# of headnode triplets)) we do a triplet combination reduction operation

this is motivated by the "except for" clause, which is , if some headnode is above another headnode in a hierarchy, we want to check all triplets except those implied
by the descendant headnode

so, we compare, for each hiearchy in a headnode triplet combination, whether from vs to is a descendant of the other
if, for any hierarchy, one is a descendant of the other, then we remove the set intersection from the node that is higher up (the opposite of a descendant)

then, having done that, we recognize that the number of unique triplet lists pairs (from vs to) is much smaller than the number of rows in the 
headnode triplet vs headnode triplet matrix

so, we opt to use the unique pairings to one anotehr
while the list of from pairs and the list of to pairs is a more compact representation, it is not the case that every from and every to are compared
therefore, we cannot simply maintain two independent lists. the multiple of those two is often longer than the headnode triplet combination list

there is a little finagling at the end, because the triplets were kept in sets (unhashable) and so we have to do some trickerty by typecasting lists and so on
to get the proper list of unique pairs
'''

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint
import time
import os

def identify_species_descendants(temp_headnode):
    #print('here')
    #print(type(temp_headnode))
    return nx.algorithms.dag.descendants(species_nx,temp_headnode)

def identify_organ_descendants(temp_headnode):
    return nx.algorithms.dag.descendants(organ_nx,temp_headnode)

def identify_disease_descendants(temp_headnode):
    return nx.algorithms.dag.descendants(disease_nx,temp_headnode)

def build_total_test_panda(temp_panda):

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


def identify_if_from_or_to_are_descendants_species(temp_from,temp_to):
    if temp_from in species_set_subtraction_hashmap[temp_to]:
        return 'from_descendant_of_to'
    elif temp_to in species_set_subtraction_hashmap[temp_from]:
        return 'to_descendant_of_from'
    else:
        return 'neither'

def identify_if_from_or_to_are_descendants_organ(temp_from,temp_to):
    if temp_from in organ_set_subtraction_hashmap[temp_to]:
        return 'from_descendant_of_to'
    elif temp_to in organ_set_subtraction_hashmap[temp_from]:
        return 'to_descendant_of_from'
    else:
        return 'neither'
  
def identify_if_from_or_to_are_descendants_disease(temp_from,temp_to):
    if temp_from in disease_set_subtraction_hashmap[temp_to]:
        return 'from_descendant_of_to'
    elif temp_to in disease_set_subtraction_hashmap[temp_from]:
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


if __name__ == "__main__":


    count_cutoff=snakemake.params.count_cutoff
    os.system('mkdir -p /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_17_precompute_comparison_triplets/')
    os.system('touch /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_17_precompute_comparison_triplets/dummy.txt')
      

    count_cutoff=1
    input_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/1/step_16_calculate_fraction_triplets/triplet_count_panda.bin'
    species_nx_input_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity/species_networkx.bin'
    organ_nx_input_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity/organ_networkx.bin'
    disease_nx_input_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity/disease_networkx.bin'
    unique_triplets_output_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_17_precompute_comparison_triplets/unique_triplets.bin'
    triplet_headnode_to_triplet_tuple_ouput_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_17_precompute_comparison_triplets/headnodes_to_triplet_list.bin'

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

    #for temp_node in species_nx.nodes:
    #    print(type(temp_node))


    

    #nx.draw(species_nx,with_labels=True)
    #plt.show()
    total_panda=build_total_test_panda(input_panda)
    print(total_panda)
    total_panda.to_pickle('/home/rictuar/delete_test_bin_calc/panda')

    species_set_subtraction_hashmap_values=input_panda['species_headnode'].apply(identify_species_descendants)
    species_set_subtraction_hashmap=dict(zip(input_panda['species_headnode'],species_set_subtraction_hashmap_values))
    
    total_panda['descendants_species']=total_panda.apply(
        lambda x: identify_if_from_or_to_are_descendants_species(x['species_headnode_from'],x['species_headnode_to']),
        axis='columns'
    )
    print(species_set_subtraction_hashmap)

    print(total_panda['descendants_species'].value_counts())
    


    organ_set_subtraction_hashmap_values=input_panda['organ_headnode'].apply(identify_organ_descendants)
    organ_set_subtraction_hashmap=dict(zip(input_panda['organ_headnode'],organ_set_subtraction_hashmap_values))
    
    total_panda['descendants_organ']=total_panda.apply(
        lambda x: identify_if_from_or_to_are_descendants_organ(x['organ_headnode_from'],x['organ_headnode_to']),
        axis='columns'
    )
    print(organ_set_subtraction_hashmap)

    print(total_panda['descendants_organ'].value_counts())




    disease_set_subtraction_hashmap_values=input_panda['disease_headnode'].apply(identify_disease_descendants)
    disease_set_subtraction_hashmap=dict(zip(input_panda['disease_headnode'],disease_set_subtraction_hashmap_values))
    
    total_panda['descendants_disease']=total_panda.apply(
        lambda x: identify_if_from_or_to_are_descendants_disease(x['disease_headnode_from'],x['disease_headnode_to']),
        axis='columns'
    )
    print(disease_set_subtraction_hashmap)

    print(total_panda['descendants_disease'].value_counts())
    

    '''
    #did this way in case crash memory
    #append to and from triplets
    #
    triplet_map_key=list(zip(input_panda['species_headnode'],input_panda['organ_headnode'],input_panda['disease_headnode']))
    print(triplet_map_key)

    triplet_map_dict=dict(zip(triplet_map_key,input_panda['triplet_list']))

    pprint(triplet_map_dict)
    '''
    print(total_panda)
    #hold=input('total_panda')

    
    total_panda['to_triplets_inter_removed_if_nec']=total_panda.apply(
        lambda x: remove_intersection_if_necessary_to(
            
            #x['species_headnode_from'],
            #x['organ_headnode_from'],
            #x['disease_headnode_from'],
            #x['species_headnode_to'],
            #x['organ_headnode_to'],
            #x['disease_headnode_to'],

            
            
            
            
            
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


    #condition_list_from=[
    #    (total_panda['descendants_species']=='from_descendant_of_to' or total_panda['descendants_organ']=='from_descendant_of_to' or total_panda['descendants_disease']=='from_descendant_of_to')
    #]
    #choice_list_from=[
    #    total_panda['from_triplets'].difference(total_panda['to_triplets']),
    #]
    #total_panda['to_triplets_inter_removed_if_nec']=total_panda.apply((lambda x: x['to_triplets'].difference(x['from_triplets'])), axis='columns')
    '''
    print(total_panda.columns)
    total_panda['to_triplets_inter_removed_if_nec']=total_panda['to_triplets']
    #total_panda['to_triplets_inter_removed_if_nec']=total_panda.apply((lambda x: x['to_triplets'].difference(x['from_triplets'])), axis='columns')
    total_panda['to_triplets_inter_removed_if_nec']=total_panda.where(
        cond=((total_panda['descendants_species']!='from_descendant_of_to') & (total_panda['descendants_organ']!='from_descendant_of_to') & (total_panda['descendants_disease']!='from_descendant_of_to')),
        #other=total_panda['to_triplets'].difference(total_panda['from_triplets']),
        other=lambda x: x['to_triplets'].difference(x['from_triplets']),
        axis='columns'
        #other=()
    )
    '''
    #total_panda['to_triplets_inter_removed_if_nec']=total_panda['to_triplets_inter_removed_if_nec'].where(
    #    cond=((total_panda['descendants_species']!='from_descendant_of_to') & (total_panda['descendants_organ']!='from_descendant_of_to') & (total_panda['descendants_disease']!='from_descendant_of_to'))
    #)
    #choicelist_from=

    #total_panda['from_triplets_inter_removed_if_nec']

    print(total_panda)
    print(total_panda.columns)
    #print(total_panda['to_triplets_inter_removed_if_nec'].value_counts())
    #print(total_panda['from_triplets_inter_removed_if_nec'].value_counts())
    
    #start1=time.time()
    #print((total_panda['to_triplets_inter_removed_if_nec'].value_counts()))
    #print((total_panda['from_triplets_inter_removed_if_nec'].value_counts()))
    #end1=time.time()
    

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

    test_view[['headnode_triplet_from','headnode_triplet_to','from_triplets_inter_removed_if_nec','to_triplets_inter_removed_if_nec']].to_pickle(triplet_headnode_to_triplet_tuple_ouput_address)

    #hold=input('hold')



    
    #start2=time.time()
    #print(len(total_panda['to_triplets_inter_removed_if_nec'].transform(tuple).unique()))
    #print(len(total_panda['from_triplets_inter_removed_if_nec'].transform(tuple).unique()))
    '''
    #end2=time.time()
    ##print(end1-start1)
    #print(end2-start2)
    
    #print('check time')

    print(len(input_panda['triplet_list'].transform(tuple).unique()))
    #print(len(total_panda['to_triplets_inter_removed_if_nec'].unique()))
    #print(len(total_panda['from_triplets_inter_removed_if_nec'].unique()))
    
    #print(total_panda['to_triplets_inter_removed_if_nec'].value_counts().index.to_list())
    ##output_dict={
    ##    'triplets': (total_panda['from_triplets_inter_removed_if_nec'].value_counts().index.to_list() + total_panda['to_triplets_inter_removed_if_nec'].value_counts().index.to_list()),
    ##   'from_to': (['from' for element in total_panda['from_triplets_inter_removed_if_nec'].value_counts().index.to_list()] + ['to' for element in total_panda['to_triplets_inter_removed_if_nec'].value_counts().index.to_list()])
    ##}

    output_dict={
        'triplets': (list(total_panda['from_triplets_inter_removed_if_nec'].transform(tuple).unique()) + list(total_panda['to_triplets_inter_removed_if_nec'].transform(tuple).unique())),
        'from_to': (['from' for element in total_panda['from_triplets_inter_removed_if_nec'].transform(tuple).unique()] + ['to' for element in total_panda['to_triplets_inter_removed_if_nec'].transform(tuple).unique()])
    }    

    empty_set_indices=[i for i,value in enumerate(output_dict['triplets']) if len(value)==0]
    print(empty_set_indices)
    #empty_set_indices

    output_dict_cleaned={}
    output_dict_cleaned['triplets']=[element for i,element in enumerate(output_dict['triplets']) if i not in empty_set_indices]
    output_dict_cleaned['from_to']=[element for i,element in enumerate(output_dict['from_to']) if i not in empty_set_indices]

    
    output_panda=pd.DataFrame.from_dict(output_dict_cleaned)
    print(output_panda)
    output_panda.to_pickle(output_address)
    '''





















    
    test_view['combo_column']=(list(zip(
        test_view['to_triplets_inter_removed_if_nec'],#.transform(tuple),#.unique(),
        test_view['from_triplets_inter_removed_if_nec']#.transform(tuple)#.unique()
    )))
    #print(test_view)
    #print(test_view['combo_column'])

    print(len(test_view['combo_column'].unique()))
    print(len(test_view['to_triplets_inter_removed_if_nec'].unique()))
    print(len(test_view['from_triplets_inter_removed_if_nec'].unique()))

    #output_dict={
    #    'combos':[]
    #}
    #output_series=test_view['combo_column'].unique()
    #pprint(output_series)
    #print(len(output_series))
    output_series=pd.DataFrame(test_view['combo_column'].unique())
    output_series=output_series.assign(**dict(zip('ft', output_series[0].str)))
    print(output_series)
    output_series.drop(0,axis='columns',inplace=True)
    print(output_series)

    #hold=input('hold2')
    output_series.rename({'f': 'from','t':'to'},axis='columns',inplace=True)
    
    
    #output_series['species_headnode_from']=test_view['species_headnode_from']
    #output_series['organ_headnode_from']=test_view['organ_headnode_from']
    #output_series['disease_headnode_from']=test_view['disease_headnode_from']
    #output_series['species_headnode_to']=test_view['species_headnode_to']
    #output_series['organ_headnode_to']=test_view['organ_headnode_to']
    #output_series['disease_headnode_to']=test_view['disease_headnode_to']
   
    #output_series['headnode_triplet_from']=tuple(zip(output_series['species_headnode_from'],output_series['organ_headnode_from'],output_series['disease_headnode_from']))
    #output_series['headnode_triplet_to']=tuple(zip(output_series['species_headnode_to'],output_series['organ_headnode_to'],output_series['disease_headnode_to']))


    print(output_series)

    output_series.sort_values(by='from',inplace=True)
    print(output_series)
    output_series.to_pickle(unique_triplets_output_address)
