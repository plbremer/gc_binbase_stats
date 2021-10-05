import pandas
import networkx as nx
import os
from MainClass import *


if __name__=="__main__":

    count_cutoff=snakemake.params.count_cutoff
    os.system('mkdir -p /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_17_invoke_user_library/')
    os.system('touch /home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/'+str(count_cutoff)+'/step_17_invoke_user_library/dummy.txt')


    compound_nx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_14_reduce_hierarchy_complexity/compounds_networkx.bin'
    species_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_14_reduce_hierarchy_complexity/species_networkx.bin'
    organ_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_14_reduce_hierarchy_complexity/organ_networkx.bin'
    disease_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_14_reduce_hierarchy_complexity/disease_networkx.bin'
    
    compound_nx=nx.readwrite.gpickle.read_gpickle(compound_nx_address)
    species_nx=nx.readwrite.gpickle.read_gpickle(species_networkx_address)
    organ_nx=nx.readwrite.gpickle.read_gpickle(organ_networkx_address)
    disease_nx=nx.readwrite.gpickle.read_gpickle(disease_networkx_address)

        #create an instance of the "organization class"
    my_MainClass=MainClass(species_nx,organ_nx,disease_nx)

    #create a set of compounds that we want to evalulate
    my_MainClass.assign_compound_nodes(
        compound_nx,
        compound_topnode='CHEMONTID:9999999',
        compound_maxlevel=None,
        compound_minlevel=None,
        fold_matrix_base_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_13_swap_fold_matrix_multiindex/each_compounds_fold_matrix/'
    )

    #get the complete species, organ, disease nodeset based on a particular headnode for each hierarchy
    my_MainClass.assign_hierarchical_nodes_from(
        my_MainClass.species_nx,
        my_MainClass.organ_nx,
        my_MainClass.disease_nx,
        species_topnode='1',
        organ_topnode='organ',
        disease_topnode='disease'
    )
    
    #example of a debugger visualization call
    #my_MainClass.NodelistSelector_from.node_selection_visualizer('species')
    #my_MainClass.NodelistSelector_from.node_selection_visualizer('organ')
    #my_MainClass.NodelistSelector_from.node_selection_visualizer('disease')
    
    #get the complete species, organ, disease nodeset based on a particular headnode for each hierarchy. the to instance.
    my_MainClass.assign_hierarchical_nodes_to(
        my_MainClass.species_nx,
        my_MainClass.organ_nx,
        my_MainClass.disease_nx,
        species_topnode='1',
        organ_topnode='organ',
        disease_topnode='disease'     
    )

    #see if the from and to requests are the exact same. if so, we can invoke symmetry to shorten calculations
    my_MainClass.check_from_to_equal()

    #we choose an arbitrary fold matrix as we are only interested in the row/column headings
    one_compound_fold_matrix_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_13_swap_fold_matrix_multiindex/each_compounds_fold_matrix/2.bin'
    fold_matrix=pandas.read_pickle(one_compound_fold_matrix_address)
    my_MainClass.prepare_comparison_request(
        fold_matrix,
        my_MainClass.species_nx,
        my_MainClass.organ_nx,
        my_MainClass.disease_nx,
        my_MainClass.NodelistSelector_from.species_nodelist,
        my_MainClass.NodelistSelector_to.species_nodelist,
        my_MainClass.NodelistSelector_from.organ_nodelist,
        my_MainClass.NodelistSelector_to.organ_nodelist,
        my_MainClass.NodelistSelector_from.disease_nodelist,
        my_MainClass.NodelistSelector_to.disease_nodelist
    )
    my_MainClass.ComparisonRequest.fill_combination_dict_wrapper('from')
    my_MainClass.ComparisonRequest.convert_combination_list_to_dict('from')
    my_MainClass.ComparisonRequest.fill_combination_dict_wrapper('to')
    my_MainClass.ComparisonRequest.convert_combination_list_to_dict('to')


    #pprint(my_MainClass.ComparisonRequest.valid_node_triplets_dict['from'])
    #hold=input('hold')

    #here we enter the "main loop" of the proceedings, whereas we make a comparison selector
    #for every compound.
    my_MainClass.prepare_AllCompoundEvaluator(
        my_MainClass.CompoundNodelistSelector.compound_nodelist,
        True,
        '/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_13_swap_fold_matrix_multiindex/each_compounds_fold_matrix/',
        '/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/user_library_output/',
        my_MainClass.species_nx,
        my_MainClass.organ_nx,
        my_MainClass.disease_nx,
        my_MainClass.ComparisonRequest.valid_node_triplets_dict['from'],
        my_MainClass.ComparisonRequest.valid_node_triplets_dict['to'],
        my_MainClass.from_nodes_to_nodes_equal,
        False
    )

    my_MainClass.AllCompoundEvaluator.evaluate_all_compounds_wrapper()
