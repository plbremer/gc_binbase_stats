from unittest import result
import pandas as pd
import numpy as np



def convert_fold_to_log_fold(temp_fold):
    '''
    custom conversion to the typical log fold change from ours
    '''
    
    if temp_fold>0:
        return np.log2(temp_fold)
    elif temp_fold<0:
        return np.log2(abs(1/temp_fold))

def coerce_our_structure_to_plotly_volcano(temp_fold_panda,temp_signifigance_panda,temp_metabolite):
    
    #the desired structure is a pandas dataframe
    #
    #reshape dataframe to be column of values, with "gene" as the metabolite name
    #and from/to tuples as the snp?

    temp_fold_panda=temp_fold_panda.stack().stack().stack()
    temp_fold_panda.index.rename(['organ_from','species_from','disease_from','disease_to','species_to','organ_to'],inplace=True)
    temp_fold_panda=temp_fold_panda.reset_index()
    temp_fold_panda['from']=temp_fold_panda[['organ_from','species_from','disease_from']].apply(tuple,axis='columns')
    temp_fold_panda['to']=temp_fold_panda[['organ_to','species_to','disease_to']].apply(tuple,axis='columns')
    temp_fold_panda=temp_fold_panda.drop(['organ_from', 'species_from', 'disease_from','disease_to','species_to','organ_to'],axis='columns')
    temp_fold_panda.rename({0:'fold'},axis='columns',inplace=True)
    

    temp_signifigance_panda=temp_signifigance_panda.stack().stack().stack()
    temp_signifigance_panda.index.rename(['organ_from','species_from','disease_from','disease_to','species_to','organ_to'],inplace=True)
    temp_signifigance_panda=temp_signifigance_panda.reset_index()
    temp_signifigance_panda['from']=temp_signifigance_panda[['organ_from','species_from','disease_from']].apply(tuple,axis='columns')
    temp_signifigance_panda['to']=temp_signifigance_panda[['organ_to','species_to','disease_to']].apply(tuple,axis='columns')
    temp_signifigance_panda=temp_signifigance_panda.drop(['organ_from', 'species_from', 'disease_from','disease_to','species_to','organ_to'],axis='columns')
    temp_signifigance_panda.rename({0:'signifigance'},axis='columns',inplace=True)



    temp_fold_panda['fold']=temp_fold_panda['fold'].apply(convert_fold_to_log_fold)
    temp_fold_panda['signifigance']=temp_signifigance_panda['signifigance']
    #snap from dash plotly docs. idk what it is. something genomics.
    temp_fold_panda['snap']='from: '+temp_fold_panda['from'].astype(str)+' to: '+temp_fold_panda['to'].astype(str)
    temp_fold_panda.drop(['from','to'],inplace=True,axis='columns')
    temp_fold_panda['metabolite']=temp_metabolite

    return temp_fold_panda




if __name__=="__main__":
    #basic usage instructions
    #we hijacked this code from the volcano plot render code

    #we will go through every single bin,calculate the amount in each zone, add it to a list

    fold_type='fold_change_median_intensity'
    signifigance_type='signifigance_mannwhitney'
    fold_cutoff=1
    signifigance_cutoff=0.01
    
    #this is different from fold cutoff
    #it is here in case we integrate into snakemake
    min_fold_change=0
    #input_panda_address='../results/'+str(min_fold_change)+'/step_6_b_generate_signifigance_test_matrices/binvestigate_with_signifigance_matrices.bin'
    input_panda_address='../../results/'+str(min_fold_change)+'/step_6_b_generate_signifigance_test_matrices/binvestigate_with_signifigance_matrices.bin'

    full_data_panda=pd.read_pickle(input_panda_address)

    signifigance_and_fold_enough=list()
    either_signifigance_or_fold_not_enough=list()
    #fold_list_enough=list()
    #fold_list_not_enough=list()
    metabolite_list=list()

    for index,series in full_data_panda.iterrows():
        print(index)
        fold_panda=full_data_panda.at[index,fold_type]
        signifigance_panda=full_data_panda.at[index,signifigance_type]
        metabolite=full_data_panda.at[index,'name']
        result_panda=coerce_our_structure_to_plotly_volcano(fold_panda,signifigance_panda,metabolite)

        signifigance_and_fold_enough.append(
            len(result_panda.loc[
                (result_panda.signifigance < signifigance_cutoff) &
                (result_panda.fold > fold_cutoff)
            ].index)
        )
        either_signifigance_or_fold_not_enough.append(
            len(result_panda.loc[
                (result_panda.signifigance > signifigance_cutoff) |
                (result_panda.fold < fold_cutoff)
            ].index)
        )
        metabolite_list.append(metabolite)

    my_dict={
        'signifigance_and_fold_enough':signifigance_and_fold_enough,
        'either_signifigance_or_fold_not_enough':either_signifigance_or_fold_not_enough,
        'metabolite':metabolite_list
    }


    overall_population=pd.DataFrame.from_dict(
        my_dict
    )

    print(overall_population)
    print(overall_population.signifigance_and_fold_enough.sum())
    print(overall_population.either_signifigance_or_fold_not_enough.sum())
    print(len(full_data_panda.at[0,'species']))
