import obonet
import matplotlib.pyplot as plt
import networkx as nx
import pandas
import numpy as np
import os
import multiprocessing
from functools import partial

#cut network to those nodes related to a fold branch
def remove_branches_without_fold_matrices(temp_nx):
    '''
    we want to remove unrelated branches so that we can do the recursive analysis

    there are two conditions for the keeping of a node, either

    the node itself has a numerical name (meaning that it came from a bin)
    or the ancestors of the bin have a number (meaning that it will be a node merge point later)
    '''

    nodes_to_remove=list()

    for i, temp_node in enumerate(temp_nx.nodes):

        if type(temp_node) != str:
            continue

        temp_ancestor_list=nx.algorithms.dag.ancestors(temp_nx,temp_node)
        has_numerical_value_in_ancestors=False

        for temp_ancestor in temp_ancestor_list:
            if type(temp_ancestor) != str:
                has_numerical_value_in_ancestors=True
                break
        
        if has_numerical_value_in_ancestors==False:
            nodes_to_remove.append(temp_node)

    temp_nx.remove_nodes_from(nodes_to_remove)

#recursively control the assignment of fold change matrices
def recursively_calculate_fold_matrices(temp_nx,bottom_node):
    '''
    '''
    current_predecessor_iterator=temp_nx.predecessors(bottom_node)
    current_predecessor_list=list(current_predecessor_iterator)

    '''
    predecessors_all_have_fold_matrices=True
    for predecessor in current_predecessor_iterator:
        try:
            temp_nx.nodes[predecessor]['fold_change_matrix']
        except KeyError:
            predecessors_all_have_fold_matrices=False
    '''
    #print(list(current_predecessor_iterator))
    #hold=input('pre separate predecessors')
    predecessors_with_fold_matrices=list()
    predecessors_without_fold_matrices=list()
    for predecessor in current_predecessor_list:
        print(predecessor)
        try:
            if temp_nx.nodes[predecessor]['fold_change_matrix'] is not None:
                predecessors_with_fold_matrices.append(predecessor)
        except KeyError:
            predecessors_without_fold_matrices.append(predecessor)
    #print(predecessors_with_fold_matrices)
    #print(predecessors_without_fold_matrices)
    #hold=input('post separate predacessors')

    #if predecessors_all_have_fold_matrices:
    if len(predecessors_without_fold_matrices) == 0:
        #print('we found a base case')
        #print(predecessors_with_fold_matrices)
        #print(predecessors_without_fold_matrices)
        #print(current_predecessor_list)
        #hold=input('we found a base case')
        calculate_combined_fold_change_matrix_vectorized(temp_nx,current_predecessor_list,bottom_node)
        return
    else:
        #recursively calculate fold change matrices for subgraph for each predecessor in without
        #print('we found a recursive case')
        #print(predecessors_with_fold_matrices)
        #print(predecessors_without_fold_matrices)
        #print(current_predecessor_list)
        #hold=input('we found a recursive case')
        for temp_predecessor in predecessors_without_fold_matrices:
            recursively_calculate_fold_matrices(temp_nx,temp_predecessor)
        #calculate combined fold change matrix with all predacessors (which, after  the above, will be both lists)
        calculate_combined_fold_change_matrix_vectorized(temp_nx,current_predecessor_list,bottom_node)
        return
        
        #for temp predecessor in list of predecessors
        #calculate combined matrix (recursively calulate combined fold matrix (temp predacessor))

#perform fold change matrix analysis
def calculate_combined_fold_change_matrix(temp_nx,temp_predecessor_list,temp_bottom_node):
    #hyperparameters that we currently have as (implicitly by the way this is coded)
    ##average or lowest -> lowest
    ##how many exceptions -> no exceptions

    temp_MultiIndex=temp_nx.nodes[temp_predecessor_list[0]]['fold_change_matrix'].columns
    temp_DataFrame=pandas.DataFrame(data=np.nan,index=temp_MultiIndex,columns=temp_MultiIndex)
    print(temp_DataFrame)
    #hold=input('check test just after creation')

    predecessor_fold_matrices=[temp_nx.nodes[temp_predecessor]['fold_change_matrix'] for temp_predecessor in temp_predecessor_list]

    all_predecessors_concatenated_DataFrame=pandas.concat(
        objs=predecessor_fold_matrices,
        keys=range(0,len(temp_predecessor_list))
        )

    #print(temp_DataFrame)
    print(all_predecessors_concatenated_DataFrame)
    hold=input('check form of dataframe')

    for index, series in temp_DataFrame.iterrows():
        print(index)
        for temp_column in temp_DataFrame.columns:
            #print(series)
            #print(index)
            #print(temp_column)
            
            one_cell_slice=all_predecessors_concatenated_DataFrame.xs(
                key=(index[0],index[1],index[2]),
                level=(1,2,3)
            )[temp_column]
            print(one_cell_slice.values)
            #print(one_cell_slice.isnull())
            #print(one_cell_slice.isnull().values)
            #print(one_cell_slice.isnull().values.any())
            #hold=input('logc check')

            
             
            if one_cell_slice.isnull().values.any():
                temp_DataFrame.at[series.name,temp_column]=np.nan
                #temp_DataFrame.at[series.name,temp_column]='hello'
            elif all(one_cell_slice==np.inf):
                temp_DataFrame.at[series.name,temp_column]=np.inf
            elif all(one_cell_slice==-np.inf):
                temp_DataFrame.at[series.name,temp_column]=-np.inf
            elif any(one_cell_slice<0) and any(one_cell_slice>0):
                temp_DataFrame.at[series.name,temp_column]=0
            elif any(one_cell_slice==0):
                temp_DataFrame.at[series.name,temp_column]=0
            elif all(one_cell_slice>0):
                temp_DataFrame.at[series.name,temp_column]=min(one_cell_slice)
            elif all(one_cell_slice<0):
                temp_DataFrame.at[series.name,temp_column]=max(one_cell_slice)
            else:
                hold=input('something is wrong - fold matrix malformed')

            #print(temp_DataFrame.at[series.name,temp_column])
            #hold=input('working on multislice')

    #        slice_across_all_predacessors_one_cell=
    
    #print(all_predecessors_concatenated_DataFrame)
    #print(temp_DataFrame)
    #print(temp_nx.nodes[temp_bottom_node]['name'])
    #hold=input('check combination dataframe')    
    
    temp_nx.nodes[temp_bottom_node]['fold_change_matrix']=temp_DataFrame
    temp_nx.nodes[temp_bottom_node]['type_of_node']='combination'
    

    #indices of the min value of all

def visualize_added_classes(temp_nx):
    '''
    '''
    #add_one_node_to_classyfire_network(parsed_obo,binvestigate_panda.loc[0],class_to_node_dict)
    #color_list_original=['#1f78b4' for i in range(0,temp_original_classyfire_nodecount)]
    #color_list_new=['#32cd32' for i in range(0,len(temp_nx.nodes)-temp_original_classyfire_nodecount)]
    #total_color_list=color_list_original+color_list_new
    total_color_list=list()
    for temp_node in temp_nx.nodes:
        try:
            if temp_node==1682:
                hold=input('foudn 1682')
                total_color_list.append('#0000ff')
            elif temp_nx.nodes[temp_node]['type_of_node']=='from_binvestigate':
                total_color_list.append('#32cd32')
            elif temp_nx.nodes[temp_node]['type_of_node']=='combination':
                total_color_list.append('#ff0000')
        except KeyError:
            total_color_list.append('#1f78b4')

    nx.draw(temp_nx,with_labels=True,node_color=total_color_list,node_size=150)
    plt.show() 

def write_each_compound_fold_change_matrix_to_file(temp_nx,temp_address_base):
    '''
    '''
    #if you get here then you should can the directory that existed previously
    total_address=temp_address_base+'all_fold_matrices/'
    os.system('trash '+total_address)
    os.system('mkdir '+total_address)

    #traverse entire compound matrix
    for temp_node in temp_nx.nodes:
        temp_nx.nodes[temp_node]['fold_change_matrix'].to_pickle(total_address+str(temp_node)+'.bin')








def one_cell_transform(temp_cell):

    #print(temp_cell)
    #print(temp_cell.values)
    #print(np.isnan(temp_cell.values).any())
    conditions=[
        np.isnan(temp_cell.values).any(),
        all(temp_cell==np.inf),
        all(temp_cell==-np.inf),
        any(temp_cell<0) and any(temp_cell>0),
        any(temp_cell==0),
        all(temp_cell>0),
        all(temp_cell<0)
    ]

    choices=[
        np.nan,
        np.inf,
        -np.inf,
        0,
        0,
        min(temp_cell),
        max(temp_cell)
    ]
    #print(np.select(conditions,choices))
    #hold=input('one')

    return np.select(conditions,choices)




def one_column_custom_aggregation(temp_column):
    #print('hi')
    #print('bye')
    #hold=input('temp colum')
    #print(temp_column.groupby(level=('organ','species','disease')).agg(func=one_cell_transform))
    #hold=input('temp column grouped')
    #print(temp_column.name)

    return temp_column.groupby(level=('organ','species','disease')).agg(func=one_cell_transform)
    '''
    conditions=[
        temp_column.groupby(level=('organ','species','disease')).values.isnull().any(),
        all(temp_column.groupby(level=('organ','species','disease'))==np.inf),
        all(temp_column.groupby(level=('organ','species','disease'))==-np.inf),
        any(temp_column.groupby(level=('organ','species','disease'))<0) and any(temp_column.groupby(level=('organ','species','disease'))>0),
        any(temp_column.groupby(level=('organ','species','disease'))==0),
        all(temp_column.groupby(level=('organ','species','disease'))>0),
        all(temp_column.groupby(level=('organ','species','disease'))<0)
    ]

    choices=[
        np.nan,
        np.inf,
        -np.inf,
        0,
        0,
        min(temp_column.groupby(level=('organ','species','disease'))),
        max(temp_column.groupby(level=('organ','species','disease')))
    ]
    '''
    

#perform fold change matrix analysis
def calculate_combined_fold_change_matrix_vectorized(temp_nx,temp_predecessor_list,temp_bottom_node):
    #hyperparameters that we currently have as (implicitly by the way this is coded)
    ##average or lowest -> lowest
    ##how many exceptions -> no exceptions

    temp_MultiIndex=temp_nx.nodes[temp_predecessor_list[0]]['fold_change_matrix'].columns
    temp_DataFrame=pandas.DataFrame(data=np.nan,index=temp_MultiIndex,columns=temp_MultiIndex)
    print(temp_bottom_node)
    #print(temp_predecessor_list)
    #print(temp_DataFrame)
    #hold=input('check test just after creation')

    #if there is only one predecessor, then we dont need to calculate anything, just copy and return
    if len(temp_predecessor_list)==1:
        temp_nx.nodes[temp_bottom_node]['fold_change_matrix']=temp_nx.nodes[temp_predecessor_list[0]]['fold_change_matrix']
        temp_nx.nodes[temp_bottom_node]['type_of_node']='combination'
        return



    predecessor_fold_matrices=[temp_nx.nodes[temp_predecessor]['fold_change_matrix'] for temp_predecessor in temp_predecessor_list]


    all_predecessors_concatenated_DataFrame=pandas.concat(
        objs=predecessor_fold_matrices,
        keys=range(0,len(temp_predecessor_list))
        )

    #if the enitre predecessor list is nan or 0 then there is no meaningful information
    #makethe next one entirely np.nan and return
    #print(all_predecessors_concatenated_DataFrame.apply(pandas.Series.value_counts).index.to_list())
    #print([True if temp in [np.nan, 0] else False for temp in all_predecessors_concatenated_DataFrame.apply(pandas.Series.value_counts).index.to_list()])
    #hold=input('hodl')
    
    if all([True if temp in [np.nan, 0] else False for temp in all_predecessors_concatenated_DataFrame.apply(pandas.Series.value_counts).index.to_list()]):
        #hold=input('here')
        print('found a dead node')
        temp_nx.nodes[temp_bottom_node]['fold_change_matrix']=temp_DataFrame
        temp_nx.nodes[temp_bottom_node]['type_of_node']='combination'
        return


    #print(all_predecessors_concatenated_DataFrame)
    #hold=input('better not be length one')
    #print(temp_DataFrame)
    #print(all_predecessors_concatenated_DataFrame)
    #hold=input('check form of dataframe')

    '''
    conditions=[
        all_predecessors_concatenated_DataFrame.xs(key=(index[0],index[1],index[2]),level=(1,2,3)).isnull().values.any(),
        all(all_predecessors_concatenated_DataFrame.xs(key=(index[0],index[1],index[2]),level=(1,2,3)))==np.inf,
        all(all_predecessors_concatenated_DataFrame.xs(key=(index[0],index[1],index[2]),level=(1,2,3)))==-np.inf,
        any((all_predecessors_concatenated_DataFrame.xs(key=(index[0],index[1],index[2]),level=(1,2,3)))<0) and any((all_predecessors_concatenated_DataFrame.xs(key=(index[0],index[1],index[2]),level=(1,2,3)))>0),
        any(all_predecessors_concatenated_DataFrame.xs(key=(index[0],index[1],index[2]),level=(1,2,3))==0),
        all(all_predecessors_concatenated_DataFrame.xs(key=(index[0],index[1],index[2]),level=(1,2,3))>0),
        all(all_predecessors_concatenated_DataFrame.xs(key=(index[0],index[1],index[2]),level=(1,2,3))<0)
    ]

    choices=[
        np.nan,
        np.inf,
        -np.inf,
        0,
        0,
        min(all_predecessors_concatenated_DataFrame.xs(key=(index[0],index[1],index[2]),level=(1,2,3))),
        max(all_predecessors_concatenated_DataFrame.xs(key=(index[0],index[1],index[2]),level=(1,2,3)))
    ]
    '''
    
    
    num_processes = multiprocessing.cpu_count()
    chunk_size = len(all_predecessors_concatenated_DataFrame.columns)//num_processes
    panda_chunks=list()
    for i in range(0,num_processes):
    #chunks = [post_species_transform_panda.iloc[post_species_transform_panda[i:i + chunk_size]] for i in range(0, post_species_transform_panda.shape[0], chunk_size)]
        if i<(num_processes-1):
            panda_chunks.append(all_predecessors_concatenated_DataFrame.iloc[:,i*chunk_size:(i+1)*chunk_size])
        elif i==(num_processes-1):
            panda_chunks.append(all_predecessors_concatenated_DataFrame.iloc[:,i*chunk_size:])
    #print(panda_chunks)
    #hold=input('check chunks')
    pool = multiprocessing.Pool(processes=num_processes)
    transformed_chunks=pool.map(partial(pandas.DataFrame.agg,func=one_column_custom_aggregation),panda_chunks)
    #recombine_chunks
    for i in range(len(transformed_chunks)):
        if i<(num_processes-1):
            temp_DataFrame.iloc[:,i*chunk_size:(i+1)*chunk_size]=transformed_chunks[i]
        elif i==(num_processes-1):
            temp_DataFrame.iloc[:,i*chunk_size:]=transformed_chunks[i]
    #temp_DataFrame=pandas.concat(transformed_chunks)
    
    
    
    
    
    
    
    
    
    #temp_DataFrame=all_predecessors_concatenated_DataFrame.agg(func=one_column_custom_aggregation)

    #print(temp_DataFrame)
    #hold=input('did agg')
    #temp_DataFrame=np.select(conditions,choices)
    
    temp_nx.nodes[temp_bottom_node]['fold_change_matrix']=temp_DataFrame
    temp_nx.nodes[temp_bottom_node]['type_of_node']='combination'
    

    #indices of the min value of all



if __name__ == "__main__":
    count_cutoff=snakemake.params.count_cutoff
    input_graph_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_7_prepare_compound_hierarchy/classyfire_ont_with_bins_added.bin'
    output_graph_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_8_perform_compound_hierarchical_analysis/classyfire_analysis_results.bin'
    individual_fold_matrix_directory_base='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_8_perform_compound_hierarchical_analysis/each_compounds_fold_matrix/'
    os.system('mkdir -p /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_8_perform_compound_hierarchical_analysis/each_compounds_fold_matrix/')
    os.system('touch /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_8_perform_compound_hierarchical_analysis/dummy.txt')

    #read in network
    compound_network=nx.readwrite.gpickle.read_gpickle(input_graph_address)
    print(compound_network.nodes)
    hold=input('node list')

    #visualize_added_classes(compound_network)

    remove_branches_without_fold_matrices(compound_network)

    #visualize_added_classes(compound_network)


    recursively_calculate_fold_matrices(compound_network,'CHEMONTID:9999999')
    visualize_added_classes(compound_network)

    print(compound_network.nodes[4]['fold_change_matrix'])
    #print(compound_network.nodes[4]['name'])
    hold=input('4')
    print(compound_network.nodes['CHEMONTID:0001073']['fold_change_matrix'])
    print(compound_network.nodes['CHEMONTID:0001073']['name'])
    hold=input('0001073')
    print(compound_network.nodes[1682]['fold_change_matrix'])
    #print(compound_network.nodes[1682]['name'])
    hold=input('1682')
    print(compound_network.nodes['CHEMONTID:0001074']['fold_change_matrix'])
    print(compound_network.nodes['CHEMONTID:0001074']['name'])
    hold=input('0001074')
    print(compound_network.nodes['CHEMONTID:0000435']['fold_change_matrix'])
    print(compound_network.nodes['CHEMONTID:0000435']['name'])
    hold=input('0000435')
    print(compound_network.nodes[2]['fold_change_matrix'])
    #print(compound_network.nodes[2]['name'])
    hold=input('2')


    nx.readwrite.gpickle.write_gpickle(compound_network,output_graph_address)

    #write each compound fold matrix panda to file
    write_each_compound_fold_change_matrix_to_file(compound_network,individual_fold_matrix_directory_base)
