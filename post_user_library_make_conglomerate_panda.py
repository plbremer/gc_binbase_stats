import pandas
import os
from pprint import pprint




if __name__ == "__main__":

    count_cutoff=snakemake.params.count_cutoff
    os.system('mkdir -p /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_18_post_user_library_make_conglomerate_panda/')
    os.system('touch /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_18_post_user_library_make_conglomerate_panda/dummy.txt')

    file_base_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_17_invoke_user_library/output/'
    output_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_18_post_user_library_make_conglomerate_panda/conglomerate_result_panda.bin'

    directory_list=os.listdir(file_base_address)
    #directory_list.remove('dummy.txt')
    #directory_list.remove('abbreviated')
    #directory_list.remove('total_subdata_panda_symmetrical.bin')
    #directory_list.remove('total_subdata_panda_no_shortcuts.bin')
    #directory_list.remove('29.bin')
    pprint(directory_list)

    #hold=input('sdfgh')
    total_panda=pandas.read_pickle(file_base_address+directory_list[0])

    for i,temp_file in enumerate(directory_list):
        print(i)
        print(temp_file)
        if i==0:
            continue

        else:
            temp_panda=pandas.read_pickle(file_base_address+temp_file)
            total_panda=pandas.concat([total_panda,temp_panda],sort=False)


    total_panda.reset_index(drop=True,inplace=True)
    total_panda.to_pickle(output_address)



