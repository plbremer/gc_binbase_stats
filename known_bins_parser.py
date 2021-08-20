from pprint import pprint
import pandas as pd

def parse_gcbinbase_msp(temp_address,temp_labels_of_interest):

    value_dict={temp_label:[] for temp_label in temp_labels_of_interest}

    temp_file=open(temp_address,'r')

    #most_recently_found_attribute

    current_block={temp_label:'none_found' for temp_label in temp_labels_of_interest}

    for line in temp_file:
        if line=='\n':
            for temp_label in current_block.keys():
                value_dict[temp_label].append(current_block[temp_label])
            current_block={temp_label:'none_found' for temp_label in temp_labels_of_interest}

        elif line.split(':')[0] in temp_labels_of_interest:

            current_block[line.split(':')[0]]=(line.split(':')[1].strip())


    return value_dict

def append_aggregate_counts(temp_msp_panda,temp_binvestigate_panda):
    '''
    '''

    temp_count_column_dict={'id':[],'total_count':[],'name':[],'_id':[],'group':[]}

    for index,series in temp_msp_panda.iterrows():
        #print(series['BinId'])
        #print(temp_binvestigate_panda.loc[temp_binvestigate_panda['id']==float(series['BinId'])])
        
        #print('----------------')
        #print(series)
        #print('---------------')
        #hold=input('above is index of binvestigate')
        #print(series['BinId'])
        #print(temp_binvestigate_panda.loc[temp_binvestigate_panda['id']==float(series['BinId'])]['count'])
        #print(temp_binvestigate_panda.loc[temp_binvestigate_panda['id']==float(series['BinId'])]['count'][index])
        #print('----------')
        #print(series['BinId'])
        #print(temp_list)
        try:
            temp_index=temp_binvestigate_panda.loc[temp_binvestigate_panda['id']==float(series['BinId'])].index.to_list()[0]
            temp_count_column_dict['total_count'].append(sum(temp_binvestigate_panda.loc[temp_binvestigate_panda['id']==float(series['BinId'])]['count'][temp_index]))
            temp_count_column_dict['id'].append(temp_binvestigate_panda.loc[temp_binvestigate_panda['id']==float(series['BinId'])]['id'][temp_index])
            temp_count_column_dict['name'].append(temp_binvestigate_panda.loc[temp_binvestigate_panda['id']==float(series['BinId'])]['name'][temp_index])
            temp_count_column_dict['group'].append(temp_binvestigate_panda.loc[temp_binvestigate_panda['id']==float(series['BinId'])]['group'][temp_index])
            temp_count_column_dict['_id'].append(temp_binvestigate_panda.loc[temp_binvestigate_panda['id']==float(series['BinId'])]['_id'][temp_index])
        except IndexError:
            temp_count_column_dict['total_count'].append('none_found')
            temp_count_column_dict['id'].append('none_found')
            temp_count_column_dict['name'].append('none_found')
            temp_count_column_dict['group'].append('none_found')
            temp_count_column_dict['_id'].append('none_found')    

        #pprint(temp_count_column_dict)

        #hold=input('hold')


    binvestigate_subset_panda=pd.DataFrame.from_dict(temp_count_column_dict)

    output_panda=temp_msp_panda.join(binvestigate_subset_panda,how='inner')

    print(output_panda)

    return output_panda








if __name__ == "__main__":
    msp_address="/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/gc_binbase_bin_msp/known_bins.txt"
    output_address="/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/gc_binbase_bin_msp/known_bins_parsed_aggregates_added.csv"
    labels_of_interest=['BinId','InChI Key','Name','Group']

    value_dict=parse_gcbinbase_msp(msp_address,labels_of_interest)
    value_df=pd.DataFrame.from_dict(value_dict)

    binvestigate_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/binvestigate_pull/binvestigate_pickle.bin'
    binvestigate_panda=pd.read_pickle(binvestigate_panda_address)


    output_panda=append_aggregate_counts(value_df,binvestigate_panda)

    #value_df.to_csv(output_address,sep=',')

    output_panda.to_csv(output_address,sep='¬')
