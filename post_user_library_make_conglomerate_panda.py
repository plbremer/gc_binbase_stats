import pandas
import os
from pprint import pprint




if __name__ == "__main__":

    file_base_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/user_library_output/'
    output_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/user_library_output/total_subdata_panda_no_shortcuts.bin'
    directory_list=os.listdir(file_base_address)

    directory_list.remove('total_subdata_panda.bin')
    directory_list.remove('abbreviated')
    directory_list.remove('total_subdata_panda_symmetrical.bin')
    pprint(directory_list)


    total_panda=pandas.read_pickle(file_base_address+directory_list[0])

    for i,temp_file in enumerate(directory_list):
        print(i)
        print(temp_file)
        if i==0:
            continue

        else:
            temp_panda=pandas.read_pickle(file_base_address+temp_file)
            total_panda=pandas.concat([total_panda,temp_panda],sort=False)


    total_panda.to_pickle(output_address)



