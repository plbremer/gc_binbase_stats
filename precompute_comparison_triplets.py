import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint

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
    hold=input('hold')
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

    count_cutoff=1
    input_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/1/step_16_calculate_fraction_triplets/triplet_count_panda.bin'
    species_nx_input_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity/species_networkx.bin'
    organ_nx_input_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity/organ_networkx.bin'
    disease_nx_input_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity/disease_networkx.bin'
    output_address='/home/rictuar/delete_test_bin_calc/unique_triplets'

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
    hold=input('total_panda')

    
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
    print(total_panda['to_triplets_inter_removed_if_nec'].value_counts())
    print(total_panda['from_triplets_inter_removed_if_nec'].value_counts())
    print(len(total_panda['to_triplets_inter_removed_if_nec'].value_counts()))
    print(len(total_panda['from_triplets_inter_removed_if_nec'].value_counts()))
    print(len(input_panda['triplet_list'].value_counts()))
    #print(len(total_panda['to_triplets_inter_removed_if_nec'].unique()))
    #print(len(total_panda['from_triplets_inter_removed_if_nec'].unique()))
    
    print(total_panda['to_triplets_inter_removed_if_nec'].value_counts().index.to_list())
    output_dict={
        'triplets': (total_panda['from_triplets_inter_removed_if_nec'].value_counts().index.to_list() + total_panda['to_triplets_inter_removed_if_nec'].value_counts().index.to_list()),
        'from_to': (['from' for element in total_panda['from_triplets_inter_removed_if_nec'].value_counts().index.to_list()] + ['to' for element in total_panda['to_triplets_inter_removed_if_nec'].value_counts().index.to_list()])
    }

    output_panda=pd.DataFrame.from_dict(output_dict)

    output_panda.to_pickle(output_address)