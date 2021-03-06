import pandas as pd
import sys
import os

if __name__ == "__main__":

    
    min_fold_change=sys.argv[1]
    input_panda_address='../results/'+str(min_fold_change)+'/step_5_panda_cleaned/binvestigate_ready_for_analysis.bin'
    output_panda_address='../results/'+str(min_fold_change)+'/step_5_b_make_non_ratio_table/non_ratio_table.bin'
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_5_b_make_non_ratio_table/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_5_b_make_non_ratio_table/dummy.txt')

    output_dict={
        'bin':[],
        'compound':[],
        'species':[],
        'organ':[],
        'disease':[],
        'intensity_average':[],
        'intensity_median':[],
        'percent_present':[]
    }

    temp=pd.read_pickle(input_panda_address)

    for index,series in temp.iterrows():
        output_dict['bin']+=[series['id'] for i in range(len(series['species']))]
        output_dict['compound']+=[series['name'] for i in range(len(series['species']))]
        output_dict['species']+=series['species']
        output_dict['organ']+=series['organ']
        output_dict['disease']+=series['special_property_list']
        output_dict['intensity_average']+=series['total_intensity']
        output_dict['intensity_median']+=series['median_intensity']
        output_dict['percent_present']+=series['percent_present']


    temp_2=pd.DataFrame.from_dict(output_dict)
    temp_2.to_pickle(output_panda_address)

    temp_2['combined_sod']=temp_2.species+' - '+temp_2.organ+' - '+temp_2.disease
    temp_2.combined_sod.value_counts().to_pickle(
        '../results/'+str(min_fold_change)+'/step_5_b_make_non_ratio_table/unique_sod_combinations.bin'
    )


