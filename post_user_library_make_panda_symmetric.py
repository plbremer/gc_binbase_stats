import pandas
import itertools


def create_symmetric_panda(temp_panda):
    columns_with_from=[temp_column for temp_column in temp_panda.columns if 'from' in temp_column ]
    print(columns_with_from)
    columns_with_to=[temp_column for temp_column in temp_panda.columns if 'to' in temp_column ]
    print(columns_with_to)
    columns_other=[temp_column for temp_column in temp_panda.columns if (('to' not in temp_column) and ('from' not in temp_column)) ]
    print(columns_other)

    new_panda=temp_panda.copy()

    #rename_dict=
    total_zip=list(zip(columns_with_from,columns_with_to))+list(zip(columns_with_to,columns_with_from))

    column_name_swap_dict={temp[0]:temp[1] for temp in total_zip}

    new_panda.rename(column_name_swap_dict,axis='columns',inplace=True)
    new_panda['fold_change']=new_panda['fold_change'].mul(other=-1)

    new_panda_column_order=list(temp_panda.columns)
    new_panda=new_panda.reindex(columns=new_panda_column_order)

    print(temp_panda)
    print(new_panda)

    hold=input('hold')
    total_result=pandas.concat([temp_panda,new_panda],sort=False)
    print(total_result)

    return total_result




if __name__=="__main__":

    no_shortcut_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/user_library_output/total_subdata_panda.bin'
    input_panda=pandas.read_pickle(no_shortcut_panda_address)
    #print(input_panda)
    #hold=input('hold')
    total_panda=create_symmetric_panda(input_panda)
    output_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/user_library_output/total_subdata_panda_symmetrical.bin'

    total_panda.to_pickle(output_panda_address)