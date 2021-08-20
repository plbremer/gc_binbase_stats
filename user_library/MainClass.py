#import SingleResultCalculator
from CompoundNodelistSelector import *
from NodelistSelector import *
from ComparisonRequest import *
from SingleCompoundEvaluator import *
from SingleResultCalculator import *
import pandas
from AllCompoundEvaluator import *

class MainClass():

    def __init__(self,temp_species_nx,temp_organ_nx,temp_disease_nx):
        '''
        '''
        self.species_nx=temp_species_nx
        self.organ_nx=temp_organ_nx
        self.disease_nx=temp_disease_nx
        pass

    def assign_compound_nodes(self,temp_compound_nx,compound_topnode=None,compound_maxlevel=None,compound_minlevel=None):
        '''
        '''
        self.CompoundNodelistSelector=CompoundNodelistSelector(temp_compound_nx,compound_topnode,compound_maxlevel,compound_minlevel)

    def assign_hierarchical_nodes_from(
        self,
        temp_species_nx,
        temp_organ_nx,
        temp_disease_nx,   
        species_topnode=None,
        organ_topnode=None,
        disease_topnode=None,
        species_minlevel=None,
        disease_minlevel=None,
        organ_minlevel=None,
        species_maxlevel=None,
        disease_maxlevel=None,
        organ_maxlevel=None
    ):
        '''
        '''
        self.NodelistSelector_from=NodelistSelector(
            temp_species_nx,
            temp_organ_nx,
            temp_disease_nx,   
            species_topnode,
            organ_topnode,
            disease_topnode,
            species_minlevel,
            disease_minlevel,
            organ_minlevel,
            species_maxlevel,
            disease_maxlevel,
            organ_maxlevel
        )

    def assign_hierarchical_nodes_to(
        self,
        temp_species_nx,
        temp_organ_nx,
        temp_disease_nx,   
        species_topnode=None,
        organ_topnode=None,
        disease_topnode=None,
        species_minlevel=None,
        disease_minlevel=None,
        organ_minlevel=None,
        species_maxlevel=None,
        disease_maxlevel=None,
        organ_maxlevel=None
    ):
        '''
        '''
        self.NodelistSelector_to=NodelistSelector(
            temp_species_nx,
            temp_organ_nx,
            temp_disease_nx,   
            species_topnode,
            organ_topnode,
            disease_topnode,
            species_minlevel,
            disease_minlevel,
            organ_minlevel,
            species_maxlevel,
            disease_maxlevel,
            organ_maxlevel
        )

    def prepare_comparison_request(
        self,
        temp_fold_matrix,
        temp_species_nx,
        temp_organ_nx,
        temp_disease_nx,
        temp_species_nodelist_from,
        temp_species_nodelist_to,
        temp_organ_nodelist_from,
        temp_organ_nodelist_to,
        temp_disease_nodelist_from,
        temp_disease_nodelist_to,
    ):
        '''
        '''
        self.ComparisonRequest=ComparisonRequest(
            temp_fold_matrix,
            temp_species_nx,
            temp_organ_nx,
            temp_disease_nx,
            temp_species_nodelist_from,
            temp_species_nodelist_to,
            temp_organ_nodelist_from,
            temp_organ_nodelist_to,
            temp_disease_nodelist_from,
            temp_disease_nodelist_to,
        )
if __name__ == "__main__":

    compound_nx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_7_prepare_compound_hierarchy/classyfire_ont_with_bins_added.bin'
    compound_nx=nx.readwrite.gpickle.read_gpickle(compound_nx_address)
    compound_nx=nx.DiGraph.reverse(compound_nx)

    species_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_11_prepare_species_networkx/species_networkx.bin'
    organ_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_12_prepare_organ_and_disease_networkx/organ_networkx.bin'
    disease_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_12_prepare_organ_and_disease_networkx/disease_networkx.bin'

    species_nx=nx.readwrite.gpickle.read_gpickle(species_networkx_address)
    organ_nx=nx.readwrite.gpickle.read_gpickle(organ_networkx_address)
    disease_nx=nx.readwrite.gpickle.read_gpickle(disease_networkx_address)

    my_MainClass=MainClass(species_nx,organ_nx,disease_nx)
    my_MainClass.assign_compound_nodes(compound_nx,compound_topnode=4545)
    print('---------')
    
    print('---------')
    my_MainClass.assign_hierarchical_nodes_from(
        my_MainClass.species_nx,
        my_MainClass.organ_nx,
        my_MainClass.disease_nx,
        species_topnode='1',
        organ_topnode='organ',
        disease_topnode='disease'     
    )
    my_MainClass.NodelistSelector_from.node_selection_visualizer('species')

    my_MainClass.assign_hierarchical_nodes_to(
        my_MainClass.species_nx,
        my_MainClass.organ_nx,
        my_MainClass.disease_nx,
        species_topnode='1',
        organ_topnode='organ',
        disease_topnode='disease'     
    )
    my_MainClass.NodelistSelector_to.node_selection_visualizer('species')

    #comparison request should probably be rewritten to take a NodelistSelector (but not necessary)
    #here we enter the "main loop" of the proceedings, whereas we make a comparison selector
    #for every compound.
    #                                 '/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_8_perform_compound_hierarchical_analysis/each_compounds_fold_matrix/all_fold_matrices/2.bin
    one_compound_fold_matrix_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_13_swap_fold_matrix_multiindex/each_compounds_fold_matrix/2.bin'
    fold_matrix=pandas.read_pickle(one_compound_fold_matrix_address)
    print(fold_matrix)
    print(my_MainClass.NodelistSelector_from.species_nodelist)
    print(my_MainClass.species_nx)
    hold=input('my_MainClass.NodelistSelector_from.species_nodelist')

    #so i should make the species_nx an attribute of the MainClass object complete with reduction functions
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
    
    
    #the product of these three things is the total number of node that could have been visited
    print(len(my_MainClass.NodelistSelector_from.species_nodelist))
    print(len(my_MainClass.NodelistSelector_from.organ_nodelist))
    print(len(my_MainClass.NodelistSelector_from.disease_nodelist))
    print('----')
    print(len(my_MainClass.NodelistSelector_to.species_nodelist))
    print(len(my_MainClass.NodelistSelector_to.organ_nodelist))
    print(len(my_MainClass.NodelistSelector_to.disease_nodelist))
    print('----')
    #these are teh total number of nodes to visit after filtering out junk like (human, leaf, lung cancer)
    print(len(my_MainClass.ComparisonRequest.valid_node_triplets_list['from']))
    print(len(my_MainClass.ComparisonRequest.valid_node_triplets_list['to']))
    #hold=input('post comparison request')



    #for temp_node in species_nx.nodes:
    #    print(species_nx.nodes[temp_node])

    #print(species_nx.nodes)
    #hold=input('hold')

    '''
    my_SingleCompoundEvaluator=SingleCompoundEvaluator(
        fold_matrix,
        species_nx,
        organ_nx,
        disease_nx,
        my_MainClass.ComparisonRequest.valid_node_triplets_dict['from'],
        my_MainClass.ComparisonRequest.valid_node_triplets_dict['to']
    )

    my_SingleCompoundEvaluator.evaluate_from()

    pprint(my_SingleCompoundEvaluator.recording_dict)

    #with open('/home/rictuar/coding_projects/fiehn_work/gc_bin_base/code/user_library/test_output.txt', 'wt') as out:
    #    pprint(my_SingleCompoundEvaluator.recording_dict, stream=out)
    temp_dataframe=pandas.DataFrame.from_dict(my_SingleCompoundEvaluator.recording_dict)
    temp_dataframe.to_csv('/home/rictuar/coding_projects/fiehn_work/gc_bin_base/code/user_library/test_output.txt',sep='@')
    '''

    my_AllCompoundEvaluator=AllCompoundEvaluator(
        #temp compound nodelist,
        my_MainClass.CompoundNodelistSelector.compound_nodelist,
        #temp use multiprocessing,
        False,
        '/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_13_swap_fold_matrix_multiindex/each_compounds_fold_matrix/',
        #temp base output address
        '/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/user_library_output/',
        my_MainClass.species_nx,
        my_MainClass.organ_nx,
        my_MainClass.disease_nx,
        my_MainClass.ComparisonRequest.valid_node_triplets_dict['from'],
        my_MainClass.ComparisonRequest.valid_node_triplets_dict['to']      
    )

    my_AllCompoundEvaluator.evaluate_all_compounds()

    #want to make "shrinking the nx" an option in the MainClass
    #need to write a function that minimizes a given nx, then unminimize then in the snakemake

    #need to do all 4 things that oliver requested
    #1) synch binvestigate, get new/expanded translation list
    #2) public group names based on counts
    #3) inchikeys based on the mapping that came from the msp
    #4) somehow handle unknowns. possibly fork the snakemake

    #speedup single result calculator
    #1) should come up with a way for single result calculator to not ahve to declare so much stuff
    #2) avoid triple loc
    #3) if doing "complete space" then can invoke the "species of to starts after species of from"
    #4) in cases where there is a "two node" graph, we can make the second node a copy of the first

    #comment everything

    #handle multiple "except for" conditions in the SingleResultCalculator
    #that is, if there is an except for in species as well as in organ, then there are actually
    #three possible interpretations, where each individual can be except for or multiple can be except for

    #hyperparameters that people could add
    #1) cutoff for threshold
    #2) minimum number of samples
    
    #record all regardless of result
    #i dont remember what this means

    #easy to use translator that converts the mesh codes and ncbi codes to english words
    #1) where to put this
    #2) how to confer understanding of path dependence
    
    #some sort of "request converted to data that we actually have" script
    #since we store the minimal splitting tree and people might want more than that

    #come up with actionable interface

    #should make a basic usage version that "does everything"
    #i think that this is becoming less relevant. I think that pre-computing everything is the better
    #option

    #potential bug
    #I wrote it so that SingleCompoundEvaluator fails if mesh labels are given instead of a mesh path by adding [0] instead
    #of the list itself

    #potential upgrade
    #make it so that the nodelists all connect to the original headnode if the version is chosen based on some 
    #level spread

    #need to make it so that hardcoded addresses are no longer the case

    #potential upgrade
    #reverse compound hierarchy during snakemake

    #add multiprocess to all compound evaluator

    #put this shit on github

    #bug
    #doesnnt seem to work when CHEMONTID is the headnode

    #come up with actionable end-user interface

    #put on pypy