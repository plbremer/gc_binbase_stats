import pandas as pd
import os
import numpy as np

def combine_pandas_from_pickles(temp_path_list, extension=None):

    grand_panda=pd.DataFrame()

    for temp_path in temp_path_list:

        if ('.null' in temp_path):
            continue
        
        if (os.path.isdir(temp_path)):
            continue

        temp_panda=pd.read_pickle(temp_path)
        print(temp_panda)

        grand_panda=grand_panda.append(temp_panda)

        print(grand_panda)

        #hold=input('hold')

    grand_panda['id']=pd.to_numeric(grand_panda['id'])
    grand_panda.sort_values(by='id',axis='index',ignore_index=True,inplace=True)
    print(grand_panda)
    

    
    return grand_panda

def swap_all_null_with_nan(temp_dataframe):

    for temp_column in temp_dataframe.columns:

        #print(temp_dataframe.loc[ temp_dataframe[temp_column]=='null',temp_column])
        temp_dataframe.loc[ temp_dataframe[temp_column]=='null',temp_column] = np.nan
        
        #hold=input('hold')

    return temp_dataframe

if __name__ == "__main__":

    initial_directory='/home/rictuar/coding_projects_database/'
    file_list=os.listdir(initial_directory)

    print(file_list)

    path_list=[initial_directory+i for i in file_list]

    combined_panda=combine_pandas_from_pickles(path_list,'.bin')

    combined_panda=swap_all_null_with_nan(combined_panda)

    print(combined_panda)
    #combined_panda.to_csv(initial_directory+'binvestigate_csv.csv',sep='¬')
    combined_panda.to_pickle(initial_directory+'binvestigate_pickle.bin')