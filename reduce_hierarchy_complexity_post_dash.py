import networkx as nx
from pprint import pprint
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import graphviz_layout
import pandas
import os
#import generate_fold_change_matrices
from generate_fold_change_matrices import show_all_organ_species_disease_triplets
from prepare_species_networkx import visualize_nodes_on_a_list

'''
The main purpose of this script is to take the four hierarchies and reduce them to somthing human useable

'''


def reveal_node_attributes(temp_nx):
    for temp_node in temp_nx.nodes:
        pprint(temp_nx.nodes[temp_node])
        print(temp_node)


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


def do_everything(temp_nx_address,temp_node_keep_address,temp_output_address,temp_hierarchy_type):
    
    if temp_hierarchy_type=='compound':
        
        temp_nx=nx.readwrite.gpickle.read_gpickle(temp_nx_address)
        temp_nx=nx.DiGraph.reverse(temp_nx)

        compounds_to_keep_panda=pandas.read_csv(temp_node_keep_address)
        keep_list=compounds_to_keep_panda['nodes_to_keep'].to_list()    
        remove_unwanted_nodes(temp_nx,keep_list,temp_hierarchy_type)
        draw_nx_for_analysis(temp_nx,'compound')
        nx.readwrite.gpickle.write_gpickle(temp_nx,temp_output_address)

    elif temp_hierarchy_type=='species':
        temp_nx=nx.readwrite.gpickle.read_gpickle(temp_nx_address)


        species_to_keep_panda=pandas.read_csv(temp_node_keep_address,)
        keep_list=species_to_keep_panda['nodes_to_keep'].astype(str).to_list()
        remove_unwanted_nodes(temp_nx,keep_list,temp_hierarchy_type)
        draw_nx_for_analysis(temp_nx,temp_hierarchy_type,species_set)
        nx.readwrite.gpickle.write_gpickle(temp_nx,temp_output_address)

    elif temp_hierarchy_type=='organ':
        temp_nx=nx.readwrite.gpickle.read_gpickle(temp_nx_address)

        #draw_nx_for_analysis(temp_nx,temp_hierarchy_type,organ_set)
        organs_to_keep_panda=pandas.read_csv(temp_node_keep_address)
        keep_list=organs_to_keep_panda['nodes_to_keep'].to_list()
        remove_unwanted_nodes(temp_nx,keep_list,temp_hierarchy_type)
        draw_nx_for_analysis(temp_nx,temp_hierarchy_type,organ_set)
        nx.readwrite.gpickle.write_gpickle(temp_nx,temp_output_address)

    elif temp_hierarchy_type=='disease':
        temp_nx=nx.readwrite.gpickle.read_gpickle(temp_nx_address)

        diseases_to_keep_panda=pandas.read_csv(temp_node_keep_address)
        keep_list=diseases_to_keep_panda['nodes_to_keep'].to_list()
        #print(keep_list)
        remove_unwanted_nodes(temp_nx,keep_list,temp_hierarchy_type)
        draw_nx_for_analysis(temp_nx,temp_hierarchy_type,disease_set)
        nx.readwrite.gpickle.write_gpickle(temp_nx,temp_output_address)


def create_text_for_keep_files(temp_nx,temp_hierarchy_type,set_of_binvestigate_nodes=None):
    text_dict={
        'node_id':[],
        'english_name':[],
        'we_map_to':[]
    }
    

    if temp_hierarchy_type=='compound':
        for temp_node in temp_nx.nodes:
            text_dict['node_id'].append(temp_node)
            #english name
            try:
                text_dict['english_name'].append(temp_node+' | '+temp_nx.nodes[temp_node]['name'])
            except TypeError:
                text_dict['english_name'].append(str(temp_node))
            #we map to
            if temp_nx.nodes[temp_node]['type_of_node']=='from_binvestigate':
                text_dict['we_map_to'].append('Yes')
            elif temp_nx.nodes[temp_node]['type_of_node']=='combination':
                text_dict['we_map_to'].append('No')            


    elif temp_hierarchy_type=='species':
        for temp_node in temp_nx.nodes:
            text_dict['node_id'].append(temp_node)
            
            #english name
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
            text_dict['english_name'].append(temp_sci_name+' | '+temp_common_name)
            #we map to
            if temp_node in set_of_binvestigate_nodes:
                text_dict['we_map_to'].append('Yes')
            else:
                text_dict['we_map_to'].append('No')

    elif temp_hierarchy_type=='organ' or temp_hierarchy_type=='disease':

        for temp_node in temp_nx.nodes:
            text_dict['node_id'].append(temp_node)
            #english name
            text_dict['english_name'].append(temp_nx.nodes[temp_node]['mesh_label'])
            #we map to
            if temp_nx.nodes[temp_node]['mesh_label'] in set_of_binvestigate_nodes:
                text_dict['we_map_to'].append('Yes')
            else:
                text_dict['we_map_to'].append('No')

    text_panda=pandas.DataFrame.from_dict(text_dict)
    return text_panda

if __name__=="__main__":
    

    count_cutoff=int(snakemake.params.count_cutoff)
    os.system('mkdir -p /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity_post_dash/')
    os.system('touch /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity_post_dash/dummy.txt')
    

    output_base_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity_post_dash/'


    compound_nx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_8_perform_compound_hierarchical_analysis/classyfire_analysis_results.bin'
    compound_node_keep_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/species_organ_maps/networkx_shrink_compound.txt'
    compound_nx_output_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity_post_dash/compounds_networkx.bin'
    do_everything(compound_nx_address,compound_node_keep_address,compound_nx_output_address,'compound')
    

    #required for species, organ, and disease
    input_binvestigate_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_11_prepare_species_networkx/binvestigate_species_as_taxid.bin'
    binvestigate_panda=pandas.read_pickle(input_binvestigate_panda_address)
    organ_species_disease_triplet_list=show_all_organ_species_disease_triplets(binvestigate_panda)
    #pprint(organ_species_disease_triplet_list)

    #begin species
    species_nx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_11_prepare_species_networkx/species_networkx.bin'
    species_node_keep_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/species_organ_maps/networkx_shrink_species.txt'
    species_nx_output_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity_post_dash/species_networkx.bin'
    do_everything(species_nx_address,species_node_keep_address,species_nx_output_address,'species')

    #get the set of organs in this networkx
    ##input_binvestigate_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_11_prepare_species_networkx/binvestigate_species_as_taxid.bin'
    ##binvestigate_panda=pandas.read_pickle(input_binvestigate_panda_address)
    ##organ_species_disease_triplet_list=show_all_organ_species_disease_triplets(binvestigate_panda)
    ##organ_set={i[0] for i in organ_species_disease_triplet_list}

    organ_nx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_12_prepare_organ_and_disease_networkx/organ_networkx.bin'
    organ_node_keep_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/species_organ_maps/networkx_shrink_organ.txt'
    organ_nx_output_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity_post_dash/organ_networkx.bin'
    do_everything(organ_nx_address,organ_node_keep_address,organ_nx_output_address,'organ')
    

    disease_nx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_12_prepare_organ_and_disease_networkx/disease_networkx.bin'
    disease_node_keep_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/species_organ_maps/networkx_shrink_disease.txt'
    disease_nx_output_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_14_reduce_hierarchy_complexity_post_dash/disease_networkx.bin'
    do_everything(disease_nx_address,disease_node_keep_address,disease_nx_output_address,'disease')    
