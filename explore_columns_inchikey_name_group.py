import pandas as pd

if __name__ == "__main__":


    starting_panda=pd.read_pickle('/home/rictuar/coding_projects_database/binvestigate_pickle.bin')

    #for index,temp_row in pd.iterrows(starting_panda):

    #    if temp_row['inchikey'] 

    bottom_right=starting_panda.loc[ starting_panda['name'].str.isnumeric() ]
    #top_left=top_left.loc[ not (pd.isnull(starting_panda['inchikey'])) ]
    #top_left=top_left.loc[ top_left['inchikey'].isnull ]
    bottom_right=bottom_right.loc[ ~(pd.isnull(bottom_right['inchikey'])) ]
    #& ( )
    print(bottom_right)

    pd.set_option("display.max_rows", None)
    top_left=starting_panda.loc[ ~(starting_panda['name'].str.isnumeric()) ]
    top_left=top_left.loc[ (pd.isnull(top_left['inchikey'])) ]

    print(top_left)

    #has_name=starting_panda.loc[~(starting_panda['name'].str.isnumeric())]
    #print(has_name)
    pd.set_option("display.max_rows", 500)
    #pd.options.display.max_rows=500
    print(starting_panda.loc[0:400, ["id","name","group","_id"]])