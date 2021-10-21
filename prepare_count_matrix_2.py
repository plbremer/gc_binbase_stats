#from typing_extensions import final
import pandas
import os

'''
at a certain point, it was realized that i would be pulling the data from the "gc binbase database" rather than binvestigate

because of this, it became the case that the sample count would be a function of the species, organ, disease triplet only
and not the number of non-ND samples for a particular compound, as is the case on binvestigate

therefore, we just take the results from the earlier prepare count panda, where every column is now the same, and do a little
work to get results for a table in our database
'''


def create_sample_list_column(temp_triplet_tuple):
    '''
    '''
    print('-------')
    #print(temp_triplet_tuple)
    print(temp_triplet_tuple)
    print(triplet_to_count_panda.index)
    #print(triplet_to_count_panda.index.isin(
        
    #))
    #print(triplet_to_count_panda.index.isin(temp_triplet_tuple))
    print(triplet_to_count_panda.index.isin(temp_triplet_tuple))
    print(triplet_to_count_panda.loc[triplet_to_count_panda.index.isin(temp_triplet_tuple)].values)
    temp_list=triplet_to_count_panda.loc[triplet_to_count_panda.index.isin(temp_triplet_tuple)].values
    final_list=[i[0] for i in temp_list]
    print(final_list)
    return final_list

def get_number_of_triplets(temp_triplet_tuple):
    return len(temp_triplet_tuple)

def get_min_sample_count(temp_sample_count_list):
    return min(temp_sample_count_list)

def get_sum_sample_count(temp_sample_count_list):
    return sum(temp_sample_count_list)

if __name__ == "__main__":

    count_cutoff=snakemake.params.count_cutoff
    os.system('mkdir -p /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_19_prepare_count_matrix_2/')
    os.system('touch /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_19_prepare_count_matrix_2/dummy.txt')



    triplet_to_count_input_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/1/step_15_prepare_count_matrix/full_count_matrix.bin'
    triplet_to_count_panda=pandas.read_pickle(triplet_to_count_input_panda_address)
    unique_triplet_list_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/1/step_17_precompute_comparison_triplets/unique_triplets.bin'
    output_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_19_prepare_count_matrix_2/count_matrix.bin'
    #actually a series

    

    #print(triplet_to_count_panda.index)

    #print(triplet_to_count_panda)


    triplet_to_count_panda=triplet_to_count_panda.iloc[:,0].copy()
    unique_triplet_panda=pandas.read_pickle(unique_triplet_list_panda_address)
    
    
    
    
    print(unique_triplet_panda)

    #create_sample_count_list_column(unique_triplet_panda['from'])
    #print(unique_triplet_panda['from'].apply(create_sample_list_column(),axis='columns'))
    #unique_triplet_panda['sample_count_list']=unique_triplet_panda.apply(lambda x: create_sample_list_column(x['from']),axis=1)

    print(unique_triplet_panda)


    #output_panda=pandas.concat(objs=(unique_triplet_panda['from'],unique_triplet_panda['to']),axis='index').unique()
    #print(output_panda)

    output_panda_dict={
        'unique_triplets':pandas.concat(objs=(unique_triplet_panda['from'],unique_triplet_panda['to']),axis='index').unique()
    }
    output_panda=pandas.DataFrame.from_dict(output_panda_dict)
    print(output_panda)
    output_panda['triplet_count']=output_panda.apply(lambda x: get_number_of_triplets(x['unique_triplets']),axis='columns')

    print(output_panda)

    output_panda['sample_count_list']=output_panda.apply(lambda x: create_sample_list_column(x['unique_triplets']),axis=1)
    print(output_panda)

    output_panda['min_sample_count']=output_panda.apply(lambda x: get_min_sample_count(x['sample_count_list']),axis=1)
    print(output_panda)

    output_panda['sum_sample_count']=output_panda.apply(lambda x: get_sum_sample_count(x['sample_count_list']),axis=1)
    print(output_panda)


    #output_panda.to_pickle()