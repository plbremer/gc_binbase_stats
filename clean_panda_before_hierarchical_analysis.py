import pandas
import os

def remove_rows_with_no_taxonomy(temp_panda):
    '''
    This function removes rows when there is no species/organ/disease triplet left in those columns

    This can happen when all labels have been dropped 
    '''

    print(temp_panda.index)
    indices_to_drop=[True if len(temp_panda.at[i,'organ'])==0 else False for i in temp_panda.index]
    indices_to_drop=temp_panda.index[indices_to_drop]
    print(indices_to_drop)
    temp_panda.drop(
        labels=indices_to_drop,
        axis='rows',
        inplace=True
    )



def remove_rows_without_curated_inchikey(temp_panda):
    '''
    We remove rows without a curated inchikey
    At some point, we may add ML to them
    '''

    indices_to_drop=[True if temp_panda.at[i,'inchikey_curated']=='pre_curation_file' else False for i in temp_panda.index]
    indices_to_drop=temp_panda.index[indices_to_drop]
    temp_panda.drop(
        labels=indices_to_drop,
        axis='rows',
        inplace=True
    )

def remove_rows_where_curated_inchikey_is_at(temp_panda):
    '''
    This is the case when.... 
    '''
    indices_to_drop=[True if temp_panda.at[i,'inchikey_curated']=='@@@@@@@' else False for i in temp_panda.index]

    indices_to_drop=temp_panda.index[indices_to_drop]

    temp_panda.drop(
        labels=indices_to_drop,
        axis='rows',
        inplace=True
    )

'''
def remove_rows_without_classyfire_assignment(temp_panda):
  
    indices_to_drop=[True if temp_panda.at[i,'direct_parent_5']=='pre_curation_file' else False for i in temp_panda.index]

    indices_to_drop=temp_panda.index[indices_to_drop]

    temp_panda.drop(
        labels=indices_to_drop,
        axis='rows',
        inplace=True
    )    
'''

if __name__ == "__main__":

    #if snakemake in globals():
    count_cutoff=snakemake.params.count_cutoff
    input_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_4_classes_transformed/binvestigate_classes_transformed.bin'
    output_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_5_panda_cleaned/binvestigate_ready_for_analysis.bin'
    os.system('mkdir -p /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_5_panda_cleaned/')
    os.system('touch /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_5_panda_cleaned/dummy.txt')

    input_panda=pandas.read_pickle(input_panda_address)
    #delete rows if the parallel lists organ/species/special property are empty
    remove_rows_with_no_taxonomy(input_panda)

    #we do this for the moment to streamline the small scale analysis
    remove_rows_without_curated_inchikey(input_panda)
    remove_rows_where_curated_inchikey_is_at(input_panda)
    
    #will probably want to convert the standards to taxonomy "unspecified"
    input_panda.to_pickle(output_panda_address)