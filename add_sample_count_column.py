



import pandas
from pprint import pprint
import os

def convert_mapping_panda_to_columns(temp_panda):
    temp_panda=temp_panda.stack()
    
    #print(temp_panda)
    #print(temp_panda.columns)

    return temp_panda
    
#def sew_compound_into_triplets_from()

if __name__ == "__main__":

    count_cutoff=snakemake.params.count_cutoff
    os.system('mkdir -p /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_20_add_sample_count_column/')
    os.system('touch /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_20_add_sample_count_column/dummy.txt')


    input_result_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_19_add_triplet_count_column/conglomerate_result_panda_triplets.bin'
    input_mapping_sum_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_15_prepare_count_matrix/sum_count_matrix.bin'
    input_mapping_min_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_15_prepare_count_matrix/min_count_matrix.bin'
    output_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_20_add_sample_count_column/conglomerate_result_panda_count.bin'

    
    result_panda=pandas.read_pickle(input_result_panda_address)

    mapping_panda_min=pandas.read_pickle(input_mapping_min_panda_address)
    #print(mapping_panda_min)



    #work preparing the mapping panda
    mapping_series_min=convert_mapping_panda_to_columns(mapping_panda_min)
    #print(mapping_series_min)
    
    mapping_dict_min=dict(zip(mapping_series_min.index,mapping_series_min.values))
    #pprint(mapping_dict_min)
    
    #work preparing the results panda
    #makea  new column that is 
    #"included triplets from/to" with "compound" sewn into every tuple
    result_panda['min_count_from']=result_panda.apply(
        lambda temp_series:[element+(temp_series['compound'],) for element in temp_series['included_triplets_from'] ],
        axis='columns')
    
    print(result_panda)
    
    #map replace every tuple with the mapping dict value
    result_panda['min_count_from']=result_panda['min_count_from'].apply( lambda temp_list: [mapping_dict_min[element] for element in temp_list] )
    print(result_panda)
    
    
    result_panda['min_count_to']=result_panda.apply(
        lambda temp_series:[element+(temp_series['compound'],) for element in temp_series['included_triplets_to'] ],
        axis='columns')

    print(result_panda)
    #map replace every tuple with the mapping dict value
    result_panda['min_count_to']=result_panda['min_count_to'].apply( lambda temp_list: [mapping_dict_min[element] for element in temp_list] )
    print(result_panda)
    
    













    
    mapping_panda_sum=pandas.read_pickle(input_mapping_sum_panda_address)
    #print(mapping_panda_sum)



    #work preparing the mapping panda
    mapping_series_sum=convert_mapping_panda_to_columns(mapping_panda_sum)
    #print(mapping_series_sum)
    
    mapping_dict_sum=dict(zip(mapping_series_sum.index,mapping_series_sum.values))
    #pprint(mapping_dict_sum)
    
    #work preparing the results panda
    #makea  new column that is 
    #"included triplets from/to" with "compound" sewn into every tuple
    result_panda['sum_count_from']=result_panda.apply(
        lambda temp_series:[element+(temp_series['compound'],) for element in temp_series['included_triplets_from'] ],
        axis='columns')

    print(result_panda)
    
    #map replace every tuple with the mapping dict value
    result_panda['sum_count_from']=result_panda['sum_count_from'].apply( lambda temp_list: [mapping_dict_sum[element] for element in temp_list] )
    print(result_panda)
    
    print(result_panda.columns)


    result_panda['sum_count_to']=result_panda.apply(
        lambda temp_series:[element+(temp_series['compound'],) for element in temp_series['included_triplets_to'] ],
        axis='columns')

    print(result_panda)
    #map replace every tuple with the mapping dict value
    result_panda['sum_count_to']=result_panda['sum_count_to'].apply( lambda temp_list: [mapping_dict_sum[element] for element in temp_list] )
    print(result_panda)
    #result_panda['equals']=result_panda['sum_count_from'].equals(result_panda['min_count_from'])
    #print(result_panda['equals'].value_counts())

    result_panda.to_pickle(output_address)
    