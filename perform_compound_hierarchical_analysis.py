import sys
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
def recursively_calculate_fold_matrices(temp_nx,bottom_node,temp_matrix):
    '''
    '''
    current_predecessor_iterator=temp_nx.predecessors(bottom_node)
    current_predecessor_list=list(current_predecessor_iterator)

    predecessors_with_fold_matrices=list()
    predecessors_without_fold_matrices=list()
    for predecessor in current_predecessor_list:
        print(predecessor)
        #print('0-00')
        try:
            #print(temp_nx.nodes[predecessor])
            #print('-----------------------------------------------------------------------------')
            #print(temp_nx.nodes[predecessor][temp_matrix])
            if temp_nx.nodes[predecessor][temp_matrix] is not None:
                predecessors_with_fold_matrices.append(predecessor)
        except KeyError:
            #print('inside key error')
            predecessors_without_fold_matrices.append(predecessor)

    if len(predecessors_without_fold_matrices) == 0:
        #print('lenght of zero')
        calculate_combined_fold_change_matrix_vectorized(temp_nx,current_predecessor_list,bottom_node,temp_matrix)
        return
    else:
        #recursively calculate fold change matrices for subgraph for each predecessor in without
        for temp_predecessor in predecessors_without_fold_matrices:
            recursively_calculate_fold_matrices(temp_nx,temp_predecessor,temp_matrix)
        #calculate combined fold change matrix with all predacessors (which, after  the above, will be both lists)
        #print('arrived with a non zero pred list')
        calculate_combined_fold_change_matrix_vectorized(temp_nx,current_predecessor_list,bottom_node,temp_matrix)
        return

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

def one_cell_transform_fold(temp_cell):
    conditions=[
        #np.isnan(temp_cell.values).any(),
        #all(temp_cell==np.inf),
        #all(temp_cell==-np.inf),
        any(temp_cell<0) and any(temp_cell>0),
        #any(temp_cell==0),
        all(temp_cell>0),
        all(temp_cell<0)
    ]

    choices=[
        #np.nan,
        #np.inf,
        #-np.inf,
        0,
        #0,
        min(temp_cell),
        max(temp_cell)
    ]

    return np.select(conditions,choices)

def one_cell_transform_sig(temp_cell):
    conditions=[
        #np.isnan(temp_cell.values).any(),
        #all(temp_cell==np.inf),
        #all(temp_cell==-np.inf),
        #any(temp_cell<0) and any(temp_cell>0),
        #any(temp_cell==0),
        all(temp_cell>0)
        #all(temp_cell<0)
    ]

    choices=[
        #np.nan,
        #np.inf,
        #-np.inf,
        #0,
        #0,
        #min(temp_cell),
        max(temp_cell)
    ]

    return np.select(conditions,choices)

def one_column_custom_aggregation_fold(temp_column):
    return temp_column.groupby(level=('organ','species','disease')).agg(func=one_cell_transform_fold)

def one_column_custom_aggregation_sig(temp_column):
    return temp_column.groupby(level=('organ','species','disease')).agg(func=one_cell_transform_sig)   

#perform fold change matrix analysis
def calculate_combined_fold_change_matrix_vectorized(temp_nx,temp_predecessor_list,temp_bottom_node,temp_matrix):
    #hyperparameters that we currently have as (implicitly by the way this is coded)
    ##average or lowest -> lowest
    ##how many exceptions -> no exceptions
    # print('hi')
    # print(temp_predecessor_list)
    # print(temp_bottom_node)
    # print(temp_matrix)
    # for i in temp_predecessor_list:
    #     print(temp_nx.nodes[i])
    #print(temp_nx.nodes[tuple(temp_predecessor_list)])
    temp_MultiIndex=temp_nx.nodes[temp_predecessor_list[0]][temp_matrix].columns
    
    temp_DataFrame=pandas.DataFrame(data=np.nan,index=temp_MultiIndex,columns=temp_MultiIndex)
    # print(temp_bottom_node)

    #if there is only one predecessor, then we dont need to calculate anything, just copy and return
    if len(temp_predecessor_list)==1:
        temp_nx.nodes[temp_bottom_node][temp_matrix]=temp_nx.nodes[temp_predecessor_list[0]][temp_matrix]
        temp_nx.nodes[temp_bottom_node]['type_of_node']='combination'
        return

    predecessor_fold_matrices=[temp_nx.nodes[temp_predecessor][temp_matrix] for temp_predecessor in temp_predecessor_list]

    all_predecessors_concatenated_DataFrame=pandas.concat(
        objs=predecessor_fold_matrices,
        keys=range(0,len(temp_predecessor_list))
        )

    #if the enitre predecessor list is nan or 0 then there is no meaningful information
    #makethe next one entirely np.nan and return
    
    if all([True if temp in [np.nan, 0] else False for temp in all_predecessors_concatenated_DataFrame.apply(pandas.Series.value_counts).index.to_list()]):
        #hold=input('here')
        print('found a dead node')
        temp_nx.nodes[temp_bottom_node][temp_matrix]=temp_DataFrame
        temp_nx.nodes[temp_bottom_node]['type_of_node']='combination'
        return


    if 'fold' in temp_matrix:
        num_processes=cores_available
        #num_processes = multiprocessing.cpu_count()
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
        transformed_chunks=pool.map(partial(pandas.DataFrame.agg,func=one_column_custom_aggregation_fold),panda_chunks)
        #recombine_chunks
        for i in range(len(transformed_chunks)):
            if i<(num_processes-1):
                temp_DataFrame.iloc[:,i*chunk_size:(i+1)*chunk_size]=transformed_chunks[i]
            elif i==(num_processes-1):
                temp_DataFrame.iloc[:,i*chunk_size:]=transformed_chunks[i]
        
        temp_nx.nodes[temp_bottom_node][temp_matrix]=temp_DataFrame
        temp_nx.nodes[temp_bottom_node]['type_of_node']='combination'

    elif 'signifigance' in temp_matrix:
        num_processes=cores_available
        #num_processes = multiprocessing.cpu_count()
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
        transformed_chunks=pool.map(partial(pandas.DataFrame.agg,func=one_column_custom_aggregation_sig),panda_chunks)
        #recombine_chunks
        for i in range(len(transformed_chunks)):
            if i<(num_processes-1):
                temp_DataFrame.iloc[:,i*chunk_size:(i+1)*chunk_size]=transformed_chunks[i]
            elif i==(num_processes-1):
                temp_DataFrame.iloc[:,i*chunk_size:]=transformed_chunks[i]
        
        temp_nx.nodes[temp_bottom_node][temp_matrix]=temp_DataFrame
        temp_nx.nodes[temp_bottom_node]['type_of_node']='combination'


def write_each_unknown_to_file(binvestigate_panda,temp_address_base):

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

    print('now outputting unknown bins')
    for index,series in binvestigate_panda.iterrows():
        if series['inchikey']!='@@@@@@@':
            continue
        else:
            print('printing unknown '+str(series['id'])+' iteration number '+str(index))
            for i in range(len(matrices_to_compute)):
                total_address=temp_address_base+matrices_to_compute[i]+'/'
                series[binvestigate_panda_column_names[i]].to_pickle(total_address+str(series['id'])+'.bin')



def do_everything(temp_nx,temp_node_keep_address,temp_hierarchy_type):
    
    if temp_hierarchy_type=='compound':
        
        temp_nx=nx.DiGraph.reverse(temp_nx)
        #draw_nx_for_analysis(temp_nx,'compound')
        compounds_to_keep_panda=pandas.read_csv(temp_node_keep_address)
        keep_list=compounds_to_keep_panda['nodes_to_keep'].to_list()    
        remove_unwanted_nodes(temp_nx,keep_list,temp_hierarchy_type)
        #draw_nx_for_analysis(temp_nx,'compound')

    return temp_nx

def remove_unwanted_nodes(temp_nx,temp_nodes_to_keep,temp_hierarchy_type):
    '''
    for species and compounds, we automatically keep a node if it is a leaf
    for organs and diseases, we require that a node be explicitly listed to be kept
    '''
    
    nodes_to_drop=list()
    if temp_hierarchy_type=='compound' or temp_hierarchy_type=='species':
        for temp_node in temp_nx.nodes:
            if (temp_node not in temp_nodes_to_keep) and (len(list(temp_nx.successors(temp_node)))>0):
                nodes_to_drop.append(temp_node)
    elif temp_hierarchy_type=='organ' or temp_hierarchy_type=='disease':
        for temp_node in temp_nx.nodes:
            if (temp_node not in temp_nodes_to_keep):
                nodes_to_drop.append(temp_node)


    for temp_node in nodes_to_drop:

        list_of_predecessors=list(temp_nx.predecessors(temp_node))
        list_of_successors=list(temp_nx.successors(temp_node))
        for temp_predecessor in list_of_predecessors:
            print(temp_predecessor)
            for temp_successor in list_of_successors:
                print(temp_successor)
                temp_nx.add_edge(temp_predecessor,temp_successor)
        temp_nx.remove_node(temp_node)

    return temp_nx

def draw_nx_for_analysis(temp_nx,temp_hierarchy_type,set_of_binvestigate_nodes=None):
    '''

    '''
    #for compound matrix, it is obvious that bins => source of data
    #for species matrix, we put that information into an attribute called "type of node" where the values
    #   are "from binvestigate" or "combination"
   

    total_color_list=list()
    
    if temp_hierarchy_type=='compound':
        label_dict=get_labels_for_drawing(temp_nx,'compound')
        for i,temp_node in enumerate(temp_nx.nodes):
            if temp_nx.nodes[temp_node]['type_of_node']=='combination':
                total_color_list.append('#ff0000')
            elif temp_nx.nodes[temp_node]['type_of_node']=='from_binvestigate':
                total_color_list.append('#32cd32')
    
    elif temp_hierarchy_type=='species':
        label_dict=get_labels_for_drawing(temp_nx,'species')
        for i,temp_node in enumerate(temp_nx.nodes):
            if temp_node in set_of_binvestigate_nodes:
                total_color_list.append('#32cd32')
            else:
                total_color_list.append('#ff0000')
    
    elif temp_hierarchy_type=='organ':
        label_dict=get_labels_for_drawing(temp_nx,'organ')
        for i,temp_node in enumerate(temp_nx.nodes):
            if temp_nx.nodes[temp_node]['mesh_label'] in set_of_binvestigate_nodes:
                total_color_list.append('#32cd32')
            else:
                total_color_list.append('#ff0000')

    elif temp_hierarchy_type=='disease':
        label_dict=get_labels_for_drawing(temp_nx,'disease')
        for i,temp_node in enumerate(temp_nx.nodes):
            if temp_nx.nodes[temp_node]['mesh_label'] in set_of_binvestigate_nodes:
                total_color_list.append('#32cd32')
            else:
                total_color_list.append('#ff0000')




    pos = nx.nx_agraph.pygraphviz_layout(temp_nx, prog='dot')
    nx.draw(temp_nx, pos,labels=label_dict,node_color=total_color_list)
    plt.show()


def get_labels_for_drawing(temp_nx,temp_hierarchy_type):

    label_dict=dict()
    if temp_hierarchy_type=='compound':
        for temp_node in temp_nx.nodes:
            try:
                label_dict[temp_node]=(temp_node+'\n'+temp_nx.nodes[temp_node]['name'])
            except TypeError:
                label_dict[temp_node]=(str(temp_node))

    elif temp_hierarchy_type=='species':
        for temp_node in temp_nx.nodes:
            pprint(temp_nx.nodes[temp_node])
            try:
                temp_sci_name=temp_nx.nodes[temp_node]['scientific_name']
            except KeyError:
                temp_sci_name='no scientific name found'

            try:
                if type(temp_nx.nodes[temp_node]['common_name']) == list:
                    temp_common_name=temp_nx.nodes[temp_node]['common_name'][0]
                else:
                    temp_common_name=temp_nx.nodes[temp_node]['common_name']
            except KeyError:
                temp_common_name='no common name found' 

            label_dict[temp_node]=(temp_node+'\n'+temp_sci_name+'\n'+temp_common_name)

    elif temp_hierarchy_type=='organ' or temp_hierarchy_type=='disease':
        for temp_node in temp_nx.nodes:
            print(temp_node)
            label_dict[temp_node]=temp_node+'\n'+temp_nx.nodes[temp_node]['mesh_label']

    return label_dict


if __name__ == "__main__":
    
    
    matrices_to_compute=[
        'fold_change_matrix_average',
        'fold_change_matrix_median',
        'signifigance_matrix_mannwhitney',
        'signifigance_matrix_welch'
    ]
    min_fold_change=sys.argv[1]
    cores_available=int(sys.argv[2])
    input_graph_address='../results/'+str(min_fold_change)+'/step_7_prepare_compound_hierarchy/classyfire_ont_with_bins_added.bin'
    output_graph_address='../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/classyfire_analysis_results.bin'
    individual_fold_matrix_directory_base='../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/all_matrices/'
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/all_matrices/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/dummy.txt')

    #read in network
    compound_network=nx.readwrite.gpickle.read_gpickle(input_graph_address)
    #print(compound_network.nodes)
    #hold=input('node list')

    #visualize_added_classes(compound_network)

    remove_branches_without_fold_matrices(compound_network)


    #visualize_added_classes(compound_network)

    for temp_matrix in matrices_to_compute:
        recursively_calculate_fold_matrices(compound_network,'CHEMONTID:9999999',temp_matrix)

    #write each compound fold matrix panda to file
    for temp_matrix in matrices_to_compute:
        write_each_compound_fold_change_matrix_to_file(compound_network,individual_fold_matrix_directory_base,temp_matrix)


    #visualize_added_classes(compound_network)
    '''
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
    '''


    #update 220926 plb
    #originally from "reduce hierarchy complexity post dash"
    #compound_nx_address='../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/classyfire_analysis_results.bin'
    compound_node_keep_address='../resources/species_organ_maps/networkx_shrink_compound.txt'
    #compound_nx_output_address='../results/'+str(min_fold_change)+'/step_14_reduce_hierarchy_complexity_post_dash/compounds_networkx.bin'
    compound_network=do_everything(compound_network,compound_node_keep_address,'compound')


    nx.readwrite.gpickle.write_gpickle(compound_network,output_graph_address,protocol=0)

    #update 220926 plb
    #we also want the unknowns for the final database, but not in the compound analysis
    #so we just copy them over from the binvestigate pickle
    binvestigate_panda_address='../results/'+str(min_fold_change)+'/step_6_b_generate_signifigance_test_matrices/binvestigate_with_signifigance_matrices.bin'
    binvestigate_panda=pandas.read_pickle(binvestigate_panda_address)
    write_each_unknown_to_file(binvestigate_panda,individual_fold_matrix_directory_base)