import sys
import obonet
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import os
import multiprocessing
from functools import partial
import re

def write_each_compound_fold_change_matrix_to_file(temp_nx,temp_address_base, temp_matrix):
    '''
    '''
    #if you get here then you should can the directory that existed previously
    total_address=temp_address_base+temp_matrix+'/'
    os.system('trash '+total_address)
    os.system('mkdir '+total_address)

    #traverse entire compound matrix
    for temp_node in temp_nx.nodes:
        temp_nx.nodes[temp_node][temp_matrix].to_pickle(total_address+str(temp_node)+'.bin')
    
def write_each_bin_to_file(binvestigate_panda,temp_address_base):

    matrices_to_compute=[
        'fold_change_matrix_average',
        'fold_change_matrix_median',
        'signifigance_matrix_mannwhitney',
        'signifigance_matrix_welch'
    ]
    binvestigate_panda_column_names=[
        'fold_change_total_intensity', 
        'fold_change_median_intensity',
        'signifigance_mannwhitney', 
        'signifigance_welch'
    ]

    #print('now outputting unknown bins')
    for index,series in binvestigate_panda.iterrows():
        # if series['inchikey']!='@@@@@@@':
        #     continue
        # else:
        print('printing bin '+str(series['id'])+' iteration number '+str(index))
        for i in range(len(matrices_to_compute)):
            total_address=temp_address_base+matrices_to_compute[i]+'/'
            series[binvestigate_panda_column_names[i]].to_pickle(total_address+str(series['id'])+'.bin')

def bfs_layers(G, sources):
    """Returns an iterator of all the layers in breadth-first search traversal.
    Parameters
    ----------
    G : NetworkX graph
        A graph over which to find the layers using breadth-first search.
    sources : node in `G` or list of nodes in `G`
        Specify starting nodes for single source or multiple sources breadth-first search
    Yields
    ------
    layer: list of nodes
        Yields list of nodes at the same distance from sources
    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> dict(enumerate(nx.bfs_layers(G, [0, 4])))
    {0: [0, 4], 1: [1, 3], 2: [2]}
    >>> H = nx.Graph()
    >>> H.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
    >>> dict(enumerate(nx.bfs_layers(H, [1])))
    {0: [1], 1: [0, 3, 4], 2: [2], 3: [5, 6]}
    >>> dict(enumerate(nx.bfs_layers(H, [1, 6])))
    {0: [1, 6], 1: [0, 3, 4, 2], 2: [5]}
    """
    #this is in here like this because its in a newer version of nx and i was not about to fuck with tht
    if sources in G:
        sources = [sources]
    current_layer = list(sources)
    visited = set(sources)
    for source in current_layer:
        if source not in G:
            raise nx.NetworkXError(f"The node {source} is not in the graph.")
    # this is basically BFS, except that the current layer only stores the nodes at
    # same distance from sources at each iteration
    while current_layer:
        yield current_layer
        next_layer = list()
        for node in current_layer:
            for child in G[node]:
                if child not in visited:
                    visited.add(child)
                    next_layer.append(child)
        current_layer = next_layer


def compute_output_matrix_fold(temp_pandas_list):
    total_panda=pd.concat(temp_pandas_list,axis='index')

    my_groupby_min=total_panda.groupby(
        level=('organ','species','disease'),axis='index'
    ).min()

    my_groupby_max=total_panda.groupby(
        level=('organ','species','disease'),axis='index'
    ).max()

    
    intermediate_min_df=my_groupby_min.where(
        np.sign(my_groupby_min)>0,
        other=0
    )
    intermediate_max_df=my_groupby_max.where(
        np.sign(my_groupby_max)<0,
        other=0
    )
    
    temp_output=intermediate_min_df.where(
        intermediate_min_df !=0,
        other=intermediate_max_df
    )
    
#     temp_output=my_groupby_min.where(
#         np.sign(my_groupby_min)==np.sign(my_groupby_max),other=0
#     )

    temp_output.values[np.tril_indices(len(temp_output.index), -1)]=0

    temp_output=temp_output-temp_output.T-np.diag(np.diag(temp_output))

    np.fill_diagonal(temp_output.values, np.nan)

    return temp_output

def compute_output_matrix_significance(temp_pandas_list):
    total_panda=pd.concat(temp_pandas_list,axis='index')

    temp_output=total_panda.groupby(
        level=('organ','species','disease'),axis='index'
    ).max()

    np.fill_diagonal(temp_output.values, np.nan)

    return temp_output


if __name__ == "__main__":
    
    min_fold_change=sys.argv[1]
    cores_available=int(sys.argv[2])

    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/all_matrices/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/dummy.txt')

    individual_fold_matrix_directory_base='../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/all_matrices/'
    
    matrices_to_compute=[
        'fold_change_matrix_average',
        'fold_change_matrix_median',
        'signifigance_matrix_mannwhitney',
        'signifigance_matrix_welch'
    ]
    for temp_matrix in matrices_to_compute:
        total_address=individual_fold_matrix_directory_base+temp_matrix+'/'
        os.system('trash '+total_address)
        os.system('mkdir '+total_address)


    #make the compounds individual files
    pipeline_input_panda_directory='../results/'+str(min_fold_change)+'/step_6_b_generate_signifigance_test_matrices/'
    #pipeline_output_directory='../results/'+str(min_fold_change)+'/step_0_c_complete_pipeline_input/'    
    
    #binvestigate_panda_address='../results/'+str(min_fold_change)+'/step_6_b_generate_signifigance_test_matrices/binvestigate_with_signifigance_matrices.bin'
    file_list=os.listdir(pipeline_input_panda_directory)
    file_list.remove('dummy.txt')
    for temp_file in file_list:
        temporary_input_panda=pd.read_pickle(pipeline_input_panda_directory+temp_file)
        #we actually do this in the method
        # temporary_input_panda=temporary_input_panda.loc[
        #     temporary_input_panda['inchikey'] == '@@@@@@@',:
        # ]
        #temporary_file_integers=re.findall(r'\d+', temp_file)

        #temp_binvestigate_panda=pandas.read_pickle(binvestigate_panda_address)
        write_each_bin_to_file(temporary_input_panda,individual_fold_matrix_directory_base)



    input_graph_address='../results/'+str(min_fold_change)+'/step_7_prepare_compound_hierarchy/classyfire_ont_with_bins_added.bin'
    #output_graph_address='../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/classyfire_analysis_results.bin'
    #read in network
    compound_network=nx.readwrite.gpickle.read_gpickle(input_graph_address)

    layered_bfs_list=list(bfs_layers(compound_network,'CHEMONTID:0000000'))
    layered_bfs_list.reverse()
    #the algorithm is, go through the bottom most layer, then the 2nd bottom most, etc
    #for each later, if its a compund, skip
    #if its not a compound, then get only the direct descendants "names"
    #open the correspondin files in the directory set that we made above,
    #crunch the "combined" matrix, and output
    #because we concern ourself only with min/max, there is a certain "linear property vibe", where we do not need the full
    #set of compounds, only the direct descendants.
    for layer in layered_bfs_list:
        print(layer)
        for node in layer:
            print(node)
            if compound_network.nodes[node]['type_of_node']=='from_binvestigate':
                continue
            else:
                #print(compound_network)
                temp_successor_list=list(compound_network.successors(node))
                for temp_matrix in matrices_to_compute:

                    temp_pandas_list=list()
                    for temp_successor in temp_successor_list:
                        #continue
                        temp_pandas_list.append(
                            pd.read_pickle(individual_fold_matrix_directory_base+temp_matrix+'/'+str(temp_successor)+'.bin')
                        )

                    if 'fold' in temp_matrix:
                        output_panda=compute_output_matrix_fold(temp_pandas_list)

                    elif 'signifi' in temp_matrix:
                        output_panda=compute_output_matrix_significance(temp_pandas_list)

                    output_panda.to_pickle(
                        individual_fold_matrix_directory_base+temp_matrix+'/'+str(node)+'.bin'
                    )



    # #print(compound_network.nodes)
    # #hold=input('node list')

    # #visualize_added_classes(compound_network)

    
    # nx.draw(compound_network)
    # plt.show()

    # #visualize_added_classes(compound_network)

    # for temp_matrix in matrices_to_compute:
    #     recursively_calculate_fold_matrices(compound_network,'CHEMONTID:9999999',temp_matrix)

    # #write each compound fold matrix panda to file
    # for temp_matrix in matrices_to_compute:
    #     write_each_compound_fold_change_matrix_to_file(compound_network,individual_fold_matrix_directory_base,temp_matrix)


    # #visualize_added_classes(compound_network)
    # '''
    # print(compound_network.nodes[4]['fold_change_matrix'])
    # #print(compound_network.nodes[4]['name'])
    # hold=input('4')
    # print(compound_network.nodes['CHEMONTID:0001073']['fold_change_matrix'])
    # print(compound_network.nodes['CHEMONTID:0001073']['name'])
    # hold=input('0001073')
    # print(compound_network.nodes[1682]['fold_change_matrix'])
    # #print(compound_network.nodes[1682]['name'])
    # hold=input('1682')
    # print(compound_network.nodes['CHEMONTID:0001074']['fold_change_matrix'])
    # print(compound_network.nodes['CHEMONTID:0001074']['name'])
    # hold=input('0001074')
    # print(compound_network.nodes['CHEMONTID:0000435']['fold_change_matrix'])
    # print(compound_network.nodes['CHEMONTID:0000435']['name'])
    # hold=input('0000435')
    # print(compound_network.nodes[2]['fold_change_matrix'])
    # #print(compound_network.nodes[2]['name'])
    # hold=input('2')
    # '''
