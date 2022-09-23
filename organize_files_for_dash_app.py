import sys
import os

if __name__ == "__main__":

    min_fold_change=sys.argv[1]
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_11_organize_files_for_dash_app/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_11_organize_files_for_dash_app/dummy.txt')


    #add non ratio stuff
    non_ratio_dropdown_address='../results/'+str(min_fold_change)+'/step_5_b_make_non_ratio_table/unique_sod_combinations.bin'
    non_ratio_dropdown_address_output='../results/'+str(min_fold_change)+'/step_23_organize_files_for_dash_app/unique_sod_combinations.bin'    
    os.system(f'cp {non_ratio_dropdown_address} {non_ratio_dropdown_address_output}')