import matplotlib.pyplot as plt
import networkx as nx
import pandas
import numpy as np
import os
from networkx.drawing.nx_pydot import graphviz_layout
import sys

def check_fold_matrix_maintains_combinations(temp_panda,temp_fold_number,temp_count_meeting_fold_number):
    '''
    '''
    
    #print(temp_panda)
    #hold=input('arrived in one fold matrix')
    #meets_number_mask=temp_panda.loc[temp_panda.abs()>temp_fold_number]
    #dataframe_as_one_column=temp_panda.stack()
    mask=temp_panda.abs().ge(temp_fold_number)
    #mask=temp_panda.apply(lambda x: x)
    #print(dataframe_as_one_column)
    #print(temp_panda.values)
    #print(mask)
    #hold=input('mask')
    #hold=input('check one column')
    #meets_number_mask=temp_panda.mask(cond=(temp_panda.abs()>temp_fold_number),
    #print(meets_number_mask)
    #print(mask.value_counts())
    #hold=input('mask value counts')
    #print(mask['blood_plasma','rattus'].value_counts())
    #hold=input()
    #print(mask.stack())
    #hold=input('stack value counts')
    #print(mask[[i for i in mask.columns]].stack())
    #print(mask.stack().stack())
    #hold=input('double stack value counts mask')

    #print(mask.stack().stack().value_counts()[False])
    print('before try')
    try:
        #count_above_fold_thresh=(mask.stack().stack().value_counts()[True])
        count_above_fold_thresh=mask.apply(pandas.Series.value_counts).sum(axis='columns')[True]
        #value_counts=mask.apply(pandas.Series.value_counts)
        #count_above_fold_thresh=[True  for temp in all_predecessors_concatenated_DataFrame.apply(pandas.Series.value_counts).index.to_list()]
        print('after try')
        if count_above_fold_thresh>=temp_count_meeting_fold_number:
            return True
        else:
            return False
    except KeyError:
        return False
        # print('no true')
    #print()
    #hold=input('final count of  true')

def assign_combination_success_status(temp_nx,temp_predecessor_count,temp_fold_number,temp_count_meeting_fold_number):
    '''
    ok so the goal is to determine how effectively "fold patterns" are progressing up the compound hierarchy

    so we generate a traveral of the entire node set from networkx api. actually we dont even need to do this
    just iterate through each node.

    we then check each node to see if it meets the three criteria

    if it does, we assign the node a property "meets_criteria=True" and if not =False

    later, we could assign some sort of fractional number so that the rendered color could be a fraction of the way across
    a colorbar, thereby allowing us to observe the dying out of the  patterns
    '''


    for temp_node in temp_nx.nodes:
        print(temp_node)
        #check predacessors
        if len(list(temp_nx.predecessors(temp_node)))<temp_predecessor_count:
            temp_nx.nodes[temp_node]['interesting_combination']=False
            continue

        
        if check_fold_matrix_maintains_combinations(
            temp_nx.nodes[temp_node]['fold_change_matrix'],
            temp_fold_number,
            temp_count_meeting_fold_number
            )==False:
            temp_nx.nodes[temp_node]['interesting_combination']=False
            continue

        temp_nx.nodes[temp_node]['interesting_combination']=True





def visualize_added_classes(temp_nx):
    
    #add_one_node_to_classyfire_network(parsed_obo,binvestigate_panda.loc[0],class_to_node_dict)
    #color_list_original=['#1f78b4' for i in range(0,temp_original_classyfire_nodecount)]
    #color_list_new=['#32cd32' for i in range(0,len(temp_nx.nodes)-temp_original_classyfire_nodecount)]
    #total_color_list=color_list_original+color_list_new
    total_color_list=list()
    for i,temp_node in enumerate(temp_nx.nodes):
        if temp_nx.nodes[temp_node]['interesting_combination']==True:
            total_color_list.append('#ffa500')
        elif temp_nx.nodes[temp_node]['interesting_combination']==False:
            if temp_nx.nodes[temp_node]['type_of_node']=='combination':
                total_color_list.append('#ff0000')
            elif temp_nx.nodes[temp_node]['type_of_node']=='from_binvestigate':
                total_color_list.append('#32cd32')

    pos = nx.nx_agraph.pygraphviz_layout(temp_nx, prog='dot')
    #pos = graphviz_layout(temp_nx, prog="dot")
    nx.draw(temp_nx, pos,with_labels=True)
    plt.show()
    #nx.draw(temp_nx,with_labels=True,node_color=total_color_list)
    #plt.show() 

if __name__ == "__main__":
    
    min_fold_change=int(sys.argv[1] )
    predecessor_count =int(sys.argv[2])
    fold_number=int(sys.argv[3])
    count_meeting_fold_number=int(sys.argv[4])

    # predecessor_count=snakemake.params.predecessor_count
    # fold_number=snakemake.params.fold_number
    # count_meeting_fold_number=snakemake.params.count_meeting_fold_number
    # count_cutoff=snakemake.params.count_cutoff
    input_graph_address='../results/'+str(min_fold_change)+'/step_8_perform_compound_hierarchical_analysis/classyfire_analysis_results.bin'
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_9_compound_analysis_stats/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_9_compound_analysis_stats/dummy.txt')
 
    #predecessor_count=2
    #fold_number=2
    #count_meeting_fold_number=2
    #input_graph_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/intermediate_step_transforms/classyfire_analysis_results.bin'
    
    
    #output_graph_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/intermediate_step_transforms/classyfire_analysis_results.bin'

    #read in network
    compound_network=nx.readwrite.gpickle.read_gpickle(input_graph_address)
    #print(compound_network.nodes)
    #hold=input('node list')

    #show fraction (number?) of nodes in each generation that have at least one non-null spot in fold matrix
    #or we could color them?

    #same as above but with nodes that have >5 contributors?
    #or we coudl color them?

    #same as above but have greater than x non null, over y fold absolute value, with z contributors


    assign_combination_success_status(
        compound_network,
        predecessor_count,
        fold_number,
        count_meeting_fold_number
    )

    visualize_added_classes(compound_network)
