import sys
import pandas as pd
'''
at the moment not used.
integrated into build_hierarchy_filter_tables
'''



if __name__ == "__main__":

    #headnodes pairs to triplet list pair
    min_fold_change=sys.argv[1]
    hpttlp_input_address='../../results/'+str(min_fold_change)+'/step_17_precompute_comparison_triplets/headnodes_to_triplet_list.bin'
    species_map_to_address='../../results/'+str(min_fold_change)+'/step_20_build_hierarchy_filter_tables/table_species_dash.bin'
    organ_map_to_address='../../results/'+str(min_fold_change)+'/step_20_build_hierarchy_filter_tables/table_organ_dash.bin'
    disease_map_to_address='../../results/'+str(min_fold_change)+'/step_20_build_hierarchy_filter_tables/table_disease_dash.bin'

    species_panda=pandas.read_pickle(species_map_to_address)
    organ_panda=pandas.read_pickle(organ_map_to_address)
    disease_panda=pandas.read_pickle(disease_map_to_address)
    hpttlp_panda=pandas.read_pickle(hpttlp_input_address)

    species_nodes=species_panda.loc[species_panda['we_map_to']=='Yes']['node_id'].to_list()
    organ_nodes=organ_panda.loc[organ_panda['we_map_to']=='Yes']['node_id'].to_list()
    disease_nodes=disease_panda.loc[disease_panda['we_map_to']=='Yes']['node_id'].to_list()

    hpttlp_panda['basic_vs_basic']=True
    print(species_nodes)
    print(organ_nodes)
    print(disease_nodes)

    hpttlp_panda=pd.read_pickle(hpttlp_input_address)

    hpttlp_panda['basic_vs_basic']=True

    # print(hpttlp_panda.loc[
    #     (
    #         (~(hpttlp_panda['species_headnode_from'].isin(species_nodes)))
    #     )
    # ])

    hpttlp_panda.loc[
        (
            (~hpttlp_panda['species_headnode_from'].isin(species_nodes)) |
            (~hpttlp_panda['organ_headnode_from'].isin(organ_nodes)) |
            (~hpttlp_panda['disease_headnode_from'].isin(disease_nodes)) |
            (~hpttlp_panda['species_headnode_to'].isin(species_nodes)) |
            (~hpttlp_panda['organ_headnode_to'].isin(organ_nodes)) |
            (~hpttlp_panda['disease_headnode_to'].isin(disease_nodes))
        ),'basic_vs_basic'
    ]=False

    print(hpttlp_panda)