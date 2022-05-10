#this program takes the output from carrot and transforms it into something pretty close to what we got from the orginal 
#binvestigate pull.
#the basic idea is to obtain the total list of compounds and the total list of (species, organ)
#then we check the soc annotation-only files for each species organ compound
#if the file is found we impute whats missing and add to the input panda
#if the file isnt found we impute the entire list using the noise level
#somewhat unfortunately, retrospectively, the information is stored in "parallel lists" for each column for each bin
#so, the length of species, organ, count, median intensity, annotation distribution, etc should be equal 
import sys
import pandas as pd
import numpy as np
import os

def get_compound_properties(compound_properties_panda):

    a=list(zip(
            compound_properties_panda.loc[compound_properties_panda.target_type=='CONFIRMED'].target_id.astype(int),
            compound_properties_panda.loc[compound_properties_panda.target_type=='CONFIRMED'].name
    ))
    unique_bin_and_name=list()
    [unique_bin_and_name.append(x) for x in a if x not in unique_bin_and_name]

    return unique_bin_and_name

    # a=np.sort(
    #     np.array(list(zip(
    #         compound_properties_panda.loc[compound_properties_panda.target_type=='CONFIRMED'].target_id.astype(float),
    #         compound_properties_panda.loc[compound_properties_panda.target_type=='CONFIRMED'].name
    #     ))),axis=0
    # )
    #print(a)

def get_all_species_organs():
    pass

def make_empty_input_panda(pipeline_input_panda_columns,bin_and_name_list):
    temp_dict_of_list={
        temp_column:[np.nan for i in range(len(bin_and_name_list))] for temp_column in pipeline_input_panda_columns
    }

    temp_dict_of_list['id']=[temp[0] for temp in bin_and_name_list]
    temp_dict_of_list['name']=[temp[1] for temp in bin_and_name_list]

    temp_dict_of_list['species']=[list() for temp in bin_and_name_list]
    temp_dict_of_list['organ']=[list() for temp in bin_and_name_list]
    temp_dict_of_list['median_intensity']=[list() for temp in bin_and_name_list]
    temp_dict_of_list['annotation_distribution']=[list() for temp in bin_and_name_list]
    temp_dict_of_list['count']=[list() for temp in bin_and_name_list]
    temp_dict_of_list['total_intensity']=[list() for temp in bin_and_name_list]

    pipeline_input_panda=pd.DataFrame.from_dict(temp_dict_of_list)

    # print(pipeline_input_panda)
    return pipeline_input_panda

def insert_combination(species,organ,compound):
    pass

def impute_annotations_at_least_one_found(temp_annotations_list,temp_so_count):
    percent_present=len(temp_annotations_list)/temp_so_count
    imputed_value=percent_present*min(temp_annotations_list)
    return temp_annotations_list+[imputed_value for i in range(temp_so_count-len(temp_annotations_list))]

def impute_annotations_zero_found(temp_average_fame_intensity,temp_so_count):
    imputed_value=noise_intensity/temp_average_fame_intensity
    return [imputed_value for i in range(temp_so_count)]

def insert_combination_wrapper(pipeline_input_panda,bin_and_name_list,species_organ_pair_list,data_base_address,species_organ_properties_panda,so_to_skip_set):
    #

    for temp_bin_and_name in bin_and_name_list:
        print(temp_bin_and_name)

        for temp_species_organ_pair in species_organ_pair_list:

            #if temp_species_organ_pair in so_to_skip_set:
            #    #print(temp_species_organ_pair)
            #    #hold=input('hold')

            this_species_organ_count=species_organ_properties_panda.loc[
                (species_organ_properties_panda.species==temp_species_organ_pair[0]) &
                (species_organ_properties_panda.organ==temp_species_organ_pair[1])
            ]['count'].item()

            try:
                temp_panda=pd.read_pickle(data_base_address+temp_species_organ_pair[0]+'¬'+temp_species_organ_pair[1]+'¬'+str(temp_bin_and_name[0])+'.bin')
                



                #there is a special case where the annotation is made but the value is still zero
                #why this occurs is a binbase issue
                #if this is the case, then we resort to the noise imputation strategy
                if temp_panda.normalized_intensity.sum()==0:
                    this_species_organ_average_fame_intensity=species_organ_properties_panda.loc[
                        (species_organ_properties_panda.species==temp_species_organ_pair[0]) &
                        (species_organ_properties_panda.organ==temp_species_organ_pair[1])
                    ]['average_fame_intensity'].item()
                    temp_imputed_annotations_list=impute_annotations_zero_found(this_species_organ_average_fame_intensity,this_species_organ_count)

                else:
                    #in general, the lists can have the property where some annotation has a magnitude of zero
                    #the "all zero"        strategy is different, so we keep it by itself above'
                    temp_panda.drop(labels=temp_panda.index[temp_panda.normalized_intensity==0], axis='index',inplace=True)
                    temp_panda.reset_index(inplace=True,drop=True)
                    temp_imputed_annotations_list=impute_annotations_at_least_one_found(temp_panda['normalized_intensity'].to_list(),this_species_organ_count)



                # print(temp_panda['normalized_intensity'].to_list())
                # print(temp_imputed_annotations_list)
                # print(this_species_organ_count)
                # print(len(temp_panda['normalized_intensity'].to_list()))
                # print(len(temp_imputed_annotations_list))
                
            except FileNotFoundError:
                this_species_organ_average_fame_intensity=species_organ_properties_panda.loc[
                    (species_organ_properties_panda.species==temp_species_organ_pair[0]) &
                    (species_organ_properties_panda.organ==temp_species_organ_pair[1])
                ]['average_fame_intensity'].item()

                temp_imputed_annotations_list=impute_annotations_zero_found(this_species_organ_average_fame_intensity,this_species_organ_count)

                
                # print(temp_imputed_annotations_list)
                # print(this_species_organ_count)
                # print(this_species_organ_average_fame_intensity)
                # hold=input('hold')

            pipeline_input_panda.at[temp_bin_and_name[0],'species'].append(temp_species_organ_pair[0])
            pipeline_input_panda.at[temp_bin_and_name[0],'organ'].append(temp_species_organ_pair[1])
            pipeline_input_panda.at[temp_bin_and_name[0],'count'].append(this_species_organ_count)
            pipeline_input_panda.at[temp_bin_and_name[0],'median_intensity'].append(np.median(temp_imputed_annotations_list))
            pipeline_input_panda.at[temp_bin_and_name[0],'annotation_distribution'].append(temp_imputed_annotations_list)
            pipeline_input_panda.at[temp_bin_and_name[0],'total_intensity'].append(sum(temp_imputed_annotations_list))


    return pipeline_input_panda            


if __name__=="__main__":

    min_fold_change=sys.argv[1]
    #output_pickle_address='../results/'+str(min_fold_change)+'/step_0_b_shape_aws_pull_to_pipeline_input/binvestigate_species_transformed.bin'
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_0_b_shape_aws_pull_to_pipeline_input/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_0_b_shape_aws_pull_to_pipeline_input/dummy.txt')


    ##when looking at the fames it was discovered that a number of metadata had "bad fame appearance frequency"
    #that is, for whatever reason, the fames only appeared like 50 percent of the time
    #these are the things in the "elbow plot"
    #this file tells us how to skip systematic bias
    so_to_skip_csv_address='../resources/so_to_skip.csv'
    noise_intensity=200
    data_base_address='../results/'+str(min_fold_change)+'/step_0_a_pull_distributions_from_aws/soc_data'
    pipeline_input_panda_columns=['id','name','species','organ','count','total_intensity','median_intensity','group','inchikey','annotation_distribution']
    compound_properties_panda_address='../results/'+str(min_fold_change)+'/step_0_a_pull_distributions_from_aws/so_count_data/all_species_organs_compounds_panda.bin'
    species_organ_properties_panda_address='../results/'+str(min_fold_change)+'/step_0_a_pull_distributions_from_aws/so_count_data/species_organ_sample_count_and_average_fame.bin'
    output_address='../results/'+str(min_fold_change)+'/step_0_b_shape_aws_pull_to_pipeline_input/pipeline_input_version_0.bin'
    

    so_to_skip_panda=pd.read_csv(so_to_skip_csv_address,sep='¬')
    so_to_skip_set=set(zip(so_to_skip_panda['species'],so_to_skip_panda['organ']))


    compound_properties_panda=pd.read_pickle(compound_properties_panda_address)
    species_organ_properties_panda=pd.read_pickle(species_organ_properties_panda_address)
    

    #bin_list=get_all_bins()
    #species_organ_list=get_all_species_organs()

    bin_and_name_list=get_compound_properties(compound_properties_panda)


    species_organ_pair_list=list(zip(species_organ_properties_panda.species,species_organ_properties_panda.organ))
    # print(species_organ_pair_list)

    pipeline_input_panda=make_empty_input_panda(pipeline_input_panda_columns,bin_and_name_list)
    pipeline_input_panda.set_index(keys='id',drop=False,inplace=True)
    # print(pipeline_input_panda)
    # hold=input('hold')
    
    pipeline_input_panda=insert_combination_wrapper(pipeline_input_panda,bin_and_name_list,species_organ_pair_list,data_base_address,species_organ_properties_panda,so_to_skip_set)
    pipeline_input_panda.reset_index(inplace=True,drop=True)

    ##################################################################################
    #temporarily here for testing - leaves us with only 1 compound
    pipeline_input_panda=pipeline_input_panda.loc[pipeline_input_panda.name=='alanine']
    pipeline_input_panda.reset_index(inplace=True,drop=True)
    ##################################################################################

    print(pipeline_input_panda)
    pipeline_input_panda.to_pickle(output_address)
