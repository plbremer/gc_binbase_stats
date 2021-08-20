#the goal of this script is to take the binvestigate panda, organ_mapping, organ_networkx, and disease_networkx
#we take the binvestigate panda and, for each species/organ pair, create a value in organ and disease column
#we then confirm that for each one of these mapped outcomes, it falls somewhere on the organ and disease networkx


import numpy as np
import pandas
import os
import networkx as nx
import multiprocessing
from functools import partial
from pprint import pprint

#thoughts on the way that the organ names work
#these are more complicated. its possible that he organs were used in ways that are not congruent.
#for example, bacterial cell has like 20 different ways of being writen in the organ list
#therefore, we print the entire unique [organ,species] pair list sorted alphabetically by organ

def show_all_organ_species_pairs(temp_panda):
    #for each bin
    #element wise, combine species and organ lists
    #try to add them to a master set
    set_of_organ_species_tuples=set()
    for index, series in temp_panda.iterrows():
        this_bins_pairs=zip(series['organ'],series['species'])
        for pair in this_bins_pairs:
            set_of_organ_species_tuples.add(pair)
    return set_of_organ_species_tuples

def show_all_disease_species_pairs(temp_panda):
    #for each bin
    #element wise, combine species and disease lists
    #try to add them to a master set
    set_of_disease_species_tuples=set()
    for index, series in temp_panda.iterrows():
        this_bins_pairs=zip(series['special_property_list'],series['species'])
        for pair in this_bins_pairs:
            set_of_disease_species_tuples.add(pair)
    return set_of_disease_species_tuples    

def get_all_strings_in_list_across_panda_column(temp_panda,temp_column_name):
    '''
    in the binvestigate panda, each row is a bin
    each bin is associated with organs and species that are saved as lists
    
    this function iterates over each rows lists and attempts to add all elements to a cumulative set
    '''

    total_elements=set()

    for index, series in temp_panda.iterrows():
        #temp_list=series[temp_column_name]
        #print(type(temp_list))
        temp_set=set(series[temp_column_name])
        #print((temp_set))
        total_elements.update(temp_set)
        #print(len(total_elements))
        #hold=input('hold')

    return total_elements

def add_special_property_column(temp_panda,temp_mapping_address):
    '''
    we create a parallel list of positions on an additional hierarchy, the disease hierarchy

    special property started out as something else, but became the disease column

    i think that the computationally fastest way to do this is not the most clear/readable
    the computationall fastest would be to be to build this list at the same time we do the organ transform
    however, because we opted to do each rule over the whole panda, not the whole panda scanning
    each rule, that is not possible

    therefore, we scan through the organ list, check the corresponing "is_tumour" column,
    if yes add true to list, if no add false to list
    '''

    #we create a column that is at first filled with dummy nonsense
    temp_panda['special_property_list']='pre_special_property_workup'

    #we read the organ mapping csv which will contain our transforms
    organ_mapping_panda=pandas.read_csv(temp_mapping_address,sep='\t')

    #we create a mapping dictionary that basically looks like (species,organ): disease
    special_property_mapping_dict=dict(zip(zip(organ_mapping_panda['species'],organ_mapping_panda['organ_initial']),organ_mapping_panda['special_property']))
    #we apply that mapping over each row in the initial panda
    for index, series in temp_panda.iterrows():
        print(index)
        #applying out transform dict as a lambda on the list of organs
        #could have chosen organ, intensity, or species 
        temp_key_list=zip(series['species'],series['organ'])
        temp_panda.at[index,'special_property_list']=list(map(lambda x: special_property_mapping_dict[x], temp_key_list))
     
def transform_organ_column(temp_bin_panda):
    '''
    This function takes input panda and the address to a mapping .tsv

    It applies the rules from the mapping tsv to the input panda

    There are two types of rules: drop rules and transform rules
    Drop rules exist because we dont want all "organs" in our final analysis. that is because
    the organ is something nonsensical like "24" or "delete me"
    In drop rules, we find the index of all organs equal to the original, then drop the organs at those indices
    and the corresponding species at those indices

    in transfomrs, we take the original text and map it to the specified organ
    '''
    temp_mapping_address=organ_mapping_address
    mapping_panda=pandas.read_csv(temp_mapping_address,sep='\t')

    #apply each transformation to each row
    for mapping_index, mapping_series in mapping_panda.iterrows():
        print(mapping_index)

        #declare mapping rule
        #you have to iterate as (n^2) i believe. all rules over all binvestigate rows or vice versa
        #we chose to iterate over all rules first. retrospectively, i think that this was computationally worse
        #because i think it means that we have to access memory spots more often. 
        #drop rules work differently. must get all indices and then drop from mapping as well as organs
        if (mapping_series['organ_final'] == 'drop') or (mapping_series['organ_final'] == 'Drop'):
            
            for bin_index, bin_series in temp_bin_panda.iterrows():
                #the way that organs map is a function of the species, so we include a second condition in the if statement
                indices_to_drop=[i for i in range(0,len(bin_series['organ'])) if (bin_series['organ'][i] == mapping_series['organ_initial']) and (bin_series['species'][i] == mapping_series['species'])]
                organ_list_with_indices_removed=list(np.delete(bin_series['organ'],indices_to_drop))
                species_list_with_indices_removed=list(np.delete(bin_series['species'],indices_to_drop))
                intensity_list_with_indices_removed=list(np.delete(bin_series['intensity'],indices_to_drop))
                count_list_with_indices_removed=list(np.delete(bin_series['count'],indices_to_drop))
                special_property_list_with_indices_removed=list(np.delete(bin_series['special_property_list'],indices_to_drop))

                temp_bin_panda.at[bin_index,'organ']=organ_list_with_indices_removed
                temp_bin_panda.at[bin_index,'species']=species_list_with_indices_removed
                temp_bin_panda.at[bin_index,'intensity']=intensity_list_with_indices_removed
                temp_bin_panda.at[bin_index,'count']=count_list_with_indices_removed
                temp_bin_panda.at[bin_index,'special_property_list']=special_property_list_with_indices_removed


        elif (mapping_series['organ_final'] != 'drop') and (mapping_series['organ_final'] != 'Drop'):

            for bin_index, bin_series in temp_bin_panda.iterrows():
                for i in range(0,len(bin_series['organ'])):
                    if (bin_series['organ'][i] == mapping_series['organ_initial']):
                        bin_series['organ'][i] = mapping_series['organ_final']

                temp_bin_panda.at[bin_index,'organ']=bin_series['organ']

    return temp_bin_panda

def identify_organs_not_mapped_to_anatomy_networkx(temp_nx,temp_organ_set):
    '''
    we create a set of organs from the 'mesh_label' on some networkx
    for each organ in the set that we receive
    we see if it maps to a place in the tempnx that we receive
    '''

    mesh_organ_name_set=set()

    for temp_node in temp_nx.nodes:
        mesh_organ_name_set.add(temp_nx.nodes[temp_node]['mesh_label'])

    print(mesh_organ_name_set)
    hold=input('mesh organ name set')
    not_in_mesh_set=set()
    in_mesh_set=set()
    for temp_organ in temp_organ_set:
        if temp_organ not in mesh_organ_name_set:
            not_in_mesh_set.add(temp_organ)
        elif temp_organ in mesh_organ_name_set:
            in_mesh_set.add(temp_organ)

    print(in_mesh_set)
    hold=input('in mesh_set')

    print(not_in_mesh_set)
    hold=input('not_in_mesh_set')
    return in_mesh_set,not_in_mesh_set

if __name__ == "__main__":

    count_cutoff=snakemake.params.count_cutoff
    post_species_transform_input_pickle_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_1_species_transformed/binvestigate_species_transformed.bin'
    organ_networkx_input_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_2a_create_organ_and_disease_networkx/mesh_organ_networkx.bin'
    disease_networkx_input_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_2a_create_organ_and_disease_networkx/mesh_disease_networkx.bin'
    organ_mapping_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/species_organ_maps/organ_map.txt'
    output_pickle_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_2b_organ_transformed/binvestigate_organ_transformed.bin'
    os.system('mkdir -p /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_2b_organ_transformed/')
    os.system('touch /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_2b_organ_transformed/dummy.txt')

    post_species_transform_panda=pandas.read_pickle(post_species_transform_input_pickle_address)
    
    #this is done one time not so that we can make it part of the pipeline
    #but rather so that we can design organ_mapping.txt
    #just like in the species
    organ_specis_pair_list=show_all_organ_species_pairs(post_species_transform_panda)
    for pair in organ_specis_pair_list:
        print(pair[0]+'@'+pair[1])
    print('we have '+str(len(organ_specis_pair_list))+' pairs')
    hold=input('copy and paste species organ pairs if necessary')
    
    #using the same file, we add an "is cancer" column so that we can do cancer-centered analysis
    #because this is dont last we dont need to delete things in parallel like we do with
    #species, organ, intensity
    add_special_property_column(post_species_transform_panda,organ_mapping_address)
    
    #according to the file that we create using the previous output, we transform the panda's organ lists
    num_processes = multiprocessing.cpu_count()
    chunk_size = len(post_species_transform_panda.index)//num_processes
    panda_chunks=list()
    for i in range(0,num_processes):
    #chunks = [post_species_transform_panda.iloc[post_species_transform_panda[i:i + chunk_size]] for i in range(0, post_species_transform_panda.shape[0], chunk_size)]
        if i<(num_processes-1):
            panda_chunks.append(post_species_transform_panda.iloc[i*chunk_size:(i+1)*chunk_size])
        elif i==(num_processes-1):
            panda_chunks.append(post_species_transform_panda.iloc[i*chunk_size:])
    print(panda_chunks)
    hold=input('check chunks')
    pool = multiprocessing.Pool(processes=num_processes)
    transformed_chunks=pool.map(transform_organ_column,panda_chunks)
    #transform_organ_column(post_species_transform_panda)
    #recombine_chunks
    for i in range(len(transformed_chunks)):
        post_species_transform_panda.iloc[transformed_chunks[i].index]=transformed_chunks[i]
    post_species_transform_panda=pandas.concat(transformed_chunks)
    

    #show all organs map to anatomy networkx
    organ_networkx=nx.readwrite.gpickle.read_gpickle(organ_networkx_input_address)
    organ_set=set()
    organ_specis_pair_list=show_all_organ_species_pairs(post_species_transform_panda)
    for temp_pair in organ_specis_pair_list:
        organ_set.add(temp_pair[0])
    mapped_set,not_mapped_set=identify_organs_not_mapped_to_anatomy_networkx(organ_networkx,organ_set)


    #show all special property map to disease networkx
    disease_networkx=nx.readwrite.gpickle.read_gpickle(disease_networkx_input_address)
    disease_set=set()
    disease_species_pair_list=show_all_disease_species_pairs(post_species_transform_panda)
    for temp_pair in disease_species_pair_list:
        disease_set.add(temp_pair[0])
    mapped_set,not_mapped_set=identify_organs_not_mapped_to_anatomy_networkx(disease_networkx,disease_set)


    #output the result
    post_species_transform_panda.to_pickle(output_pickle_address)
    