import sys
import pandas
import os

#a note - the classyfire tool is weird - for certain compounds, in will repeat the lowest class a few times
#sometimes with blanks between levels. example - http://classyfire.wishartlab.com/entities/WJNGQIYEQLPJMN-IOSLPCCCSA-N
#where there is no subclass, but a direct parent is reported
#for the purposes of our analysis, this is OK. that is because we only take the most specific thing and map to the classyfire taxonomy
#we are not concerned with weird spaces in the tool's reporting system

#the general logic for this script existing in isolation compared to the bins
#is the fact that the count dropping method is slow
#so if we make changes to the classes we want to be able to update quickly

#the general logic for this is like other transforms - check a mapping.txt and replace

#if the bin did not have an inchikey identity, then the classes are all "pre_curation_file"

def print_bin_information_for_classes_curated(temp_panda):
    '''
    this prints the id and inchikey_curated for creation of the curated_class transform mapping.tsv
    '''
    pandas.options.display.max_rows=10000
    #plb update 2-6-2022
    #we now want the pipeline to handle unknown compounds, so we print things where the inchikey curated is "junk"
    #plb update 7-4-22
    ##just for reference, we want the first half of the pipeline to handle unknowns. unknowns will not be "compared" in a volcano plot way tho
    ##no reason to visit this function
    #print(temp_panda.loc[(temp_panda['inchikey_curated']!='@@@@@@@') & (temp_panda['inchikey_curated']!='pre_curation_file') ][['id','inchikey_curated']])
    print(temp_panda[['id','inchikey_curated']])
    pandas.reset_option('display.max_rows')

def update_curated_classes_from_mapping(temp_panda, temp_class_mapping_address):
    '''
    here we add columns for classes results that come from inchikeys

    we do the same matching style based on 'id' that we do for the inchikeys
    '''

    # temp_panda['kingdom']='pre_curation_file'
    # temp_panda['superclass']='pre_curation_file'
    # temp_panda['class']='pre_curation_file'
    # temp_panda['subclass']='pre_curation_file'
    # temp_panda['direct_parent_1']='pre_curation_file'
    # temp_panda['direct_parent_2']='pre_curation_file'
    # temp_panda['direct_parent_3']='pre_curation_file'
    # temp_panda['direct_parent_4']='pre_curation_file'
    # temp_panda['direct_parent_5']='pre_curation_file'

    temp_panda['class_from_curation_not_ML']=True

    class_mapping_panda=pandas.read_csv(temp_class_mapping_address,sep='\t')


    # print(class_mapping_panda.loc[
    #     class_mappping_panda.InChIKey== )
    # print(temp_panda.at[])

    temp_panda=temp_panda.merge(
        right=class_mapping_panda,
        how='left',
        left_on='inchikey',
        right_on='InChIKey'
    )

    temp_panda.drop(
        'Status',
        axis='columns',
        inplace=True
    )
    #for index, series in class_mapping_panda.iterrows():
    #for index, series in temp_panda.iterrows():
    # temp_main_panda_index=temp_panda.index[temp_panda['id']==series['id']]
    # temp_panda.at[temp_main_panda_index,'kingdom']=series['kingdom']
    # temp_panda.at[temp_main_panda_index,'superclass']=series['superclass']
    # temp_panda.at[temp_main_panda_index,'class']=series['class']
    # temp_panda.at[temp_main_panda_index,'subclass']=series['subclass']
    # temp_panda.at[temp_main_panda_index,'direct_parent_1']=series['direct_parent_1']
    # temp_panda.at[temp_main_panda_index,'direct_parent_2']=series['direct_parent_2']
    # temp_panda.at[temp_main_panda_index,'direct_parent_3']=series['direct_parent_3']
    # temp_panda.at[temp_main_panda_index,'direct_parent_4']=series['direct_parent_4']
    # temp_panda.at[temp_main_panda_index,'direct_parent_5']=series['direct_parent_5']

    #temp_panda.at[temp_main_panda_index,'class_from_curation_not_ML']=True
    return temp_panda


if __name__ == "__main__":

    #if snakemake in globals():
    #min_fold_change=snakemake.params.min_fold_change
    min_fold_change=sys.argv[1]
    initial_pickle_address='../results/'+str(min_fold_change)+'/step_3_bins_transformed/binvestigate_bins_transformed.bin'
    class_mapping_address='../resources/species_organ_maps/classes_curated_map.txt'
    output_pickle_address='../results/'+str(min_fold_change)+'/step_4_classes_transformed/binvestigate_classes_transformed.bin'
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_4_classes_transformed/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_4_classes_transformed/dummy.txt')
    #else:
    #    initial_pickle_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/intermediate_step_transforms/binvestigate_bins_transformed.bin'
    #    output_pickle_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/intermediate_step_transforms/binvestigate_classes_transformed.bin'
    #    class_mapping_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/species_organ_maps/classes_curated_map.txt'

    initial_panda=pandas.read_pickle(initial_pickle_address)


    #the classes are printed
    #and put in the proper file if necessary
    #plb 7-4-22 no reason to visit this
    ##print_bin_information_for_classes_curated(initial_panda)
    ##hold=input('copy and inchikey_curated if necessary')

    #fill the class column 
    initial_panda=update_curated_classes_from_mapping(initial_panda, class_mapping_address)

    ###############################################
    ###############################################
    #later, we may add a class from a ML algorithm#
    #in this way, each class could be added to the compound hierarchy#
    ###############################################
    ###############################################


    initial_panda.to_pickle(output_pickle_address)