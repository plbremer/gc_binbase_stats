import numpy as np
import pandas
import os
import sys
#the general thought process for the bin transformation is that we
#add an inchikey
#remove species/organ/intensity/count hierarchy based on count (thought about 
# leaving count in and doing all analyses at the end, but a low count and oddly high value does
# the opposite of a zero value for that analyte)
#later on, if desired, add a class based on a ML technique

def drop_repeats_in_group(temp_panda):
    '''
    there is a column called 'group' which basically accounts for 
    when the same compound is represented by multiple spectra (such as coeluting peaks)
    this drops those  

    it was noticed that the sunburst diagram info was the same for all bins with the same group
    so first we double check this on our own      
    '''
    #get the groups that appear at least one time
    group_value_counts=temp_panda['group'].value_counts()

    #check that all rows are exactly duplicates (except for inchikey and other "names")
    #so basically across all rows, the intensity, organ, species are the same
    for index, value in group_value_counts.iteritems():
        #we cant remove dupes if the group name appears only once
        if value == 1:
            continue

        #in this block we confirm that for each group, all [organ, species, intensity are the same]
        #which we expect because the sunburst diagrams are all the same
        zeroth_index=temp_panda.loc[temp_panda['group'] == index].index[0]
        non_zeroth_indices=temp_panda.loc[temp_panda['group'] == index].index[1:]
        for subset_index, subset_series in temp_panda.loc[temp_panda['group'] == index].iterrows():
            if subset_series['organ'] != temp_panda.loc[temp_panda['group']==index].loc[zeroth_index,'organ']:
                hold=input('there is a difference amongst the organs')
            elif subset_series['species'] != temp_panda.loc[temp_panda['group']==index].loc[zeroth_index,'species']:
                hold=input('there is a difference amongst the speciess')
            elif subset_series['intensity'] != temp_panda.loc[temp_panda['group']==index].loc[zeroth_index,'intensity']:
                hold=input('there is a difference amongst the intensitys')
            
        #for a group, after confirming teh same, we drop that 
        temp_panda.drop(labels=non_zeroth_indices,axis='index',inplace=True)

def print_all_bin_identifiers(temp_panda):
    '''
    for each bin there are at least 5 types of identifiers
    id, _id, group, name, and inchikey

    any of those 5 can contribute to a new column, inchikey_final (people think about them when mapping)

    this function prints a row "if there are words in at least one"
    that is, the 'group' or '_id' or 'inchikey' might have stuff 
    but not the others
    '''

    temp_panda.fillna(value='@@@@@@@',inplace=True)

    '''
    note:
    using the following code, we see that id 126322 (and 126323 if desired) is basically a large space
    therefore, in the curation .tsv, we set the curated inchikey to @@@@@@@ (although we may update that)
    print(temp_panda.loc[temp_panda['id']==126322][['id','inchikey']])
    print('probing test----'+temp_panda.at[5390,'inchikey']+'!!!!')
    hold=input('check na on 126322 row')
    '''
    
    my_mask=list()
    for temp_index, temp_series in temp_panda.iterrows():
        my_mask.append(any([
            any(c.isalpha() for c in str(temp_series['_id'])),
            any(c.isalpha() for c in str(temp_series['group'])),
            any(c.isalpha() for c in str(temp_series['name'])),
            any(c.isalpha() for c in str(temp_series['inchikey']))
        ]))

    print('id¬_id¬group¬name¬inchikey')
    for index,series in temp_panda.loc[my_mask].iterrows():
        print(str(series['id'])+'¬'+str(series['_id'])+'¬'+str(series['group'])+'¬'+str(series['name'])+'¬'+str(series['inchikey']))

def update_inchikey_from_mapping(temp_panda, temp_inchikey_mapping_address):
    '''
    here we add columns for curated inchikey results as some bins have names but no inchikeys

    we match the inchikeys that are incoming to the binvestigate panda using the field "id"
    '''
    temp_panda['inchikey_curated']='pre_curation_file'

    inchikey_mapping_panda=pandas.read_csv(temp_inchikey_mapping_address,sep='\t')

    for index, series in inchikey_mapping_panda.iterrows():
        temp_main_panda_index=temp_panda.index[temp_panda['id']==series['id']]
        temp_panda.at[temp_main_panda_index,'inchikey_curated']=series['inchikey_curated']

def divide_intensities_by_count(temp_panda):
    '''
    when calling rest binvestigate, the intensites are aggregates, whereas the GUI renderings are averages
    so we must make this conversion manaully
    '''
    for index,series in temp_panda.iterrows():
        #print(index)
        #print(np.array(series['intensity']))
        #print(np.array(series['count']))
        new_intensities=list(np.divide(np.array(series['intensity']),np.array(series['count'])))
        temp_panda.at[index,'intensity']=new_intensities
        #hold=input('one iteration')

def transform_count_column(temp_bin_panda,temp_count_cutoff):
    '''
    like the species and the organs, we remove from the quadruplet (species, organ, intensity, count)
    note that there are no transforms in this one, only removals   

    threshold is the hyperparameter count_cutoff
    '''

    for bin_index, bin_series in temp_bin_panda.iterrows():
        #print(bin_index)
        indices_to_drop=[i for i in range(0,len(bin_series['count'])) if bin_series['count'][i] < temp_count_cutoff]
        species_list_with_indices_removed=list(np.delete(bin_series['species'],indices_to_drop))
        organ_list_with_indices_removed=list(np.delete(bin_series['organ'],indices_to_drop))
        intensity_list_with_indices_removed=list(np.delete(bin_series['intensity'],indices_to_drop))
        count_list_with_indices_removed=list(np.delete(bin_series['count'],indices_to_drop))
        special_property_list_with_indices_removed=list(np.delete(bin_series['special_property_list'],indices_to_drop))

        temp_bin_panda.at[bin_index,'species']=species_list_with_indices_removed
        temp_bin_panda.at[bin_index,'organ']=organ_list_with_indices_removed
        temp_bin_panda.at[bin_index,'intensity']=intensity_list_with_indices_removed
        temp_bin_panda.at[bin_index,'count']=count_list_with_indices_removed
        temp_bin_panda.at[bin_index,'special_property_list']=special_property_list_with_indices_removed

def transform_intensity_column(temp_bin_panda):
    '''
    sometimes the binvestigate rest calls provided species/organs with intensities of zero
    this causes nonsense runtime/divide-by-zero errors
    '''
    
    for bin_index, bin_series in temp_bin_panda.iterrows():
        #print(bin_index)
        indices_to_drop=[i for i in range(0,len(bin_series['intensity'])) if bin_series['intensity'][i] == 0.0]
        species_list_with_indices_removed=list(np.delete(bin_series['species'],indices_to_drop))
        organ_list_with_indices_removed=list(np.delete(bin_series['organ'],indices_to_drop))
        intensity_list_with_indices_removed=list(np.delete(bin_series['intensity'],indices_to_drop))
        count_list_with_indices_removed=list(np.delete(bin_series['count'],indices_to_drop))
        special_property_list_with_indices_removed=list(np.delete(bin_series['special_property_list'],indices_to_drop))

        temp_bin_panda.at[bin_index,'species']=species_list_with_indices_removed
        temp_bin_panda.at[bin_index,'organ']=organ_list_with_indices_removed
        temp_bin_panda.at[bin_index,'intensity']=intensity_list_with_indices_removed
        temp_bin_panda.at[bin_index,'count']=count_list_with_indices_removed
        temp_bin_panda.at[bin_index,'special_property_list']=special_property_list_with_indices_removed

def get_list_of_redundancies(temp_organ_list,temp_species_list,temp_properties_list):
    '''
    zip the organs and the species together

    make a dict where the keys are the set of (organ, species)

    values are unique lists

    every time you encounter a pair, indicate the index

    then, those with dupes are those where the len of value is >1 and we have the indices
    '''

    
    key_set=set(zip(temp_organ_list,temp_species_list,temp_properties_list))
    #print(key_set)
    redundancy_dict={i:[] for i in key_set}
    #print(redundancy_dict)

    for i,temp_triplet in enumerate(zip(temp_organ_list,temp_species_list,temp_properties_list)):
        redundancy_dict[temp_triplet].append(i)

    #print(redundancy_dict)
    #hold=input('hold')
    return redundancy_dict

def aggregate_redundancies(temp_panda):
    '''
    The purpose of this function is to aggregate redundancies after the transforms.

    redundancies are "multiple intensity values" that have the "same organ and same species" (and the same special property)

    this can occur, for example, after rattus+rattisimus,liver and rattus,liver both become rattus,liver

    we search all of these and aggregate them
    '''

    for index, series in temp_panda.iterrows():
        print(index)
        #print(series)
        redundancy_dict=get_list_of_redundancies(series['organ'],series['species'],series['special_property_list'])
        #print(redundancy_dict)

        temp_species_list=list()
        temp_organ_list=list()
        temp_count_list=list()
        temp_intensity_list=list()   
        temp_special_property_list=list()


        for temp_triplet in redundancy_dict.keys():
            #if there is only one occurence of a species,organ,property triplet
            #print(temp_triplet)
            if len(redundancy_dict[temp_triplet])==1:
                temp_species_list.append(series['species'][redundancy_dict[temp_triplet][0]])
                temp_organ_list.append(series['organ'][redundancy_dict[temp_triplet][0]])
                temp_count_list.append(series['count'][redundancy_dict[temp_triplet][0]])
                temp_intensity_list.append(series['intensity'][redundancy_dict[temp_triplet][0]])
                temp_special_property_list.append(series['special_property_list'][redundancy_dict[temp_triplet][0]])
                continue

            elif len(redundancy_dict[temp_triplet])>1:
                #we can directly use the aggregate sum because a future file, transform_bins
                #does the division of the intensity by the sum. so we dont need to do a weighted
                #average

                aggregate_count=sum([series['count'][i] for i in redundancy_dict[temp_triplet]])
                aggregate_intensity=sum([series['intensity'][i] for i in redundancy_dict[temp_triplet]])                

                temp_species_list.append(temp_triplet[1])
                temp_organ_list.append(temp_triplet[0])
                temp_special_property_list.append(temp_triplet[2])
                temp_count_list.append(aggregate_count)
                temp_intensity_list.append(aggregate_intensity)

        temp_panda.at[index,'species']=temp_species_list
        temp_panda.at[index,'organ']=temp_organ_list
        temp_panda.at[index,'count']=temp_count_list
        temp_panda.at[index,'intensity']=temp_intensity_list
        temp_panda.at[index,'special_property_list']=temp_special_property_list


if __name__ == "__main__":

    #if snakemake in globals():
    min_fold_change=sys.argv[1]
    initial_pickle_address='../results/'+str(min_fold_change)+'/step_2b_organ_transformed/binvestigate_organ_transformed.bin'
    inchikey_mapping_address='../resources/species_organ_maps/inchikey_mapping.txt'
    output_pickle_address='../results/'+str(min_fold_change)+'/step_3_bins_transformed/binvestigate_bins_transformed.bin'
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_3_bins_transformed/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_3_bins_transformed/dummy.txt')
 
    #read in the initial panda....
    initial_panda=pandas.read_pickle(initial_pickle_address)

    #there is a column called 'group' which basically accounts for 
    #when the same compound is represented by multiple spectra (such as coeluting peaks)
    #this drops those
    drop_repeats_in_group(initial_panda)

    #just like the species and organs, we need to create a list of things that we transform
    #in this case, the transformation is of the inchikeys
    print_all_bin_identifiers(initial_panda)

    #just like the species and organs, based on some external txt
    #we update the inchikeys
    update_inchikey_from_mapping(initial_panda,inchikey_mapping_address)

    #sometimes the binvestigate rest calls provided species/organs with intensities of zero
    #this causes nonsense runtime/divide-by-zero errors
    transform_intensity_column(initial_panda)

    #like the species and the organs, we remove from the quadruplet (species, organ, intensity, count)
    #if there are fewer samples than the cutoff that we specify (cant trust numbers from 1 sample)
    #note that there are no transforms in this one, only removals
    #we assign count_cutoff to be zero to make it so that all triplets are kept
    count_cutoff=0
    transform_count_column(initial_panda,count_cutoff)

    #The purpose of this function is to aggregate redundancies after the transforms.
    #redundancies are "multiple intensity values" that have the "same organ and same species"
    #this can occur, for example, after rattus+rattisimus,liver and rattus,liver both become rattus,liver
    #we search all of these and aggregate them
    aggregate_redundancies(initial_panda)

    #when calling rest binvestigate, the intensites are aggregates, whereas the GUI renderings are averages
    #so we must make this conversion manaully
    divide_intensities_by_count(initial_panda)

    #########################
    #later, we may add a class from a ML algorithm
    #########################

    #print to file
    #print(initial_panda)
    initial_panda.to_pickle(output_pickle_address)