import numpy as np
import pandas

import transform_written_organs

#def calculate_single_fold_change_matrix_element():


def calculate_one_count_matrix(temp_bin,temp_MultiIndex):
    #print(temp_bin['intensity'])
    #print(temp_bin['organ'])
    #print(temp_bin['species'])
    #print(temp_MultiIndex)

    temp_DataFrame=pandas.DataFrame(data=np.nan,index=temp_MultiIndex,columns=temp_MultiIndex)
    #print(temp_DataFrame)

    
    #this is possibly the faster, vectorized way to do things
    #however, it will lead to at least a fully calculated matrix which is unnecessary

    #tuple_list=zip(temp_bin['organ'],temp_bin['species'])
    tuple_list=zip(temp_bin['organ'],temp_bin['species'])

    count_dict=dict(zip(tuple_list,temp_bin['count']))

    
    for index,series in temp_DataFrame.iterrows():

        from_count=
        try:
            from_count=count_dict[series.name]
            for temp_column in temp_DataFrame.columns:
                try:
                    if count_dict[temp_column]>from_count:
                        temp_DataFrame.at[series.name,temp_column]=count_dict[temp_column]/from_count
                    else:
                        temp_DataFrame.at[series.name,temp_column]=-from_count/count_dict[temp_column]
                except KeyError:
                    temp_DataFrame.at[series.name,temp_column]=-np.inf


        except KeyError:
            for temp_column in temp_DataFrame.columns:
                try:
                    if (count_dict[temp_column]):
                        temp_DataFrame.at[series.name,temp_column]=np.inf
                except KeyError:
                    continue

    print(temp_DataFrame)
        #hold=input('after one row')




    return temp_DataFrame


    '''
    print(index)
    print(series)
    for temp_column in temp_DataFrame.columns:
        print(series.name)
        print(temp_column)
        hold=input('hold')

        if temp_column
    '''


    
    '''
    for temp_index, temp_sub_dataframe in temp_DataFrame.groupby(level='organ'):
        print('----------------------')
        print(temp_sub_dataframe)

        for temp_single_index, temp_sub_series in temp_sub_dataframe.iterrows():
            print('--------------------')
            print(temp_sub_series)


            
            #from_index=
            #from_intensity=temp_series['intensity']
            #from_intensity=
            
            #for 
            from_intensity=intensity_dict[temp_sub_series.name]

            for temp_column in ser
            #print(intensity_dict)
            #print(temp_sub_series)
            hold=input('innermostloop')

            #from_intensity=
    



    hold=input('end of one fold change matrix calc')
    '''


def calculate_all_count_matrices(temp_panda,temp_organ_species_tuple_list):

    temp_panda['count_matrix']='pre_analysis'

    temp_organ_species_tuple_list.sort(key=lambda temp_tup: temp_tup[0])

    my_MultiIndex=pandas.MultiIndex.from_tuples(tuples=temp_organ_species_tuple_list,sortorder=None,names=['organ','species'])
    print(my_MultiIndex)

    for index,series in temp_panda.iterrows():
        #temp_fold_change_matrix=calculate_one_fold_change_matrix(series)
        print(index)
        print(series['name'])
        temp_panda.at[index,'count_matrix']=calculate_one_count_matrix(series,my_MultiIndex)


if __name__ == "__main__":


    input_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/intermediate_step_transforms/binvestigate_with_fold_matrices.bin'
    output_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/intermediate_step_transforms/binvestigate_with_count_matrices.bin'

    input_panda=pandas.read_pickle(input_panda_address)

    #obtain total organ-species list
    organ_species_tuple_list=list(transform_written_organs.show_all_organ_species_pairs(input_panda))
    print(organ_species_tuple_list)

    #create the total pairwise fold change dataframe for each bin
    calculate_all_count_matrices(input_panda,organ_species_tuple_list)

    #output as pickle
    input_panda.to_pickle(output_panda_address)