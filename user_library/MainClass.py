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
        create an instance of MainClass
        '''
        self.species_nx=temp_species_nx
        self.organ_nx=temp_organ_nx
        self.disease_nx=temp_disease_nx

    def assign_compound_nodes(self,temp_compound_nx,compound_topnode=None,compound_maxlevel=None,compound_minlevel=None,fold_matrix_base_address=None):
        '''
        Assigns a CompoundNodelistSelector.

        See class .py file for more information
        '''
        self.CompoundNodelistSelector=CompoundNodelistSelector(temp_compound_nx,compound_topnode,compound_maxlevel,compound_minlevel,fold_matrix_base_address)

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
        creates an instance of the NodelistSelector. See that class for more details
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
        Due to lack of foresight, some classes require an instance of "from" and an instance of "to", while some handle both
        at the same time
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

    def check_from_to_equal(self):
        '''
        check whether the from and to dicts are exactly equal and set a variable that retains that information
        If they are exactly equal, then we can take a shortcut of starting "to" species at the curent "from" species
        '''

        if (
            (self.NodelistSelector_from.species_nodelist == self.NodelistSelector_to.species_nodelist) and
            (self.NodelistSelector_from.organ_nodelist == self.NodelistSelector_to.organ_nodelist) and
            (self.NodelistSelector_from.disease_nodelist == self.NodelistSelector_to.disease_nodelist)
        ):
            self.from_nodes_to_nodes_equal=True
        else:
            self.from_nodes_to_nodes_equal=False

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
        A ComparisonRequest reduces the combinatorial space from species*organs*diseases to those combinations
        that have at least one entry in the rows/column header
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

    def prepare_AllCompoundEvaluator(
        self,
        temp_compound_nodelist,
        temp_use_multiprocessing,
        temp_location_of_fold_change_matrices,
        temp_output_location,
        temp_species_nx,
        temp_organ_nx,
        temp_disease_nx,
        temp_comparison_request_dict_from,
        temp_comparison_request_dict_to,
        temp_comparison_requests_are_equal,
        temp_use_shortcuts
    ):
        '''
        '''
        self.AllCompoundEvaluator=AllCompoundEvaluator(
            temp_compound_nodelist,
            temp_use_multiprocessing,
            temp_location_of_fold_change_matrices,
            temp_output_location,
            temp_species_nx,
            temp_organ_nx,
            temp_disease_nx,
            temp_comparison_request_dict_from,
            temp_comparison_request_dict_to,
            temp_comparison_requests_are_equal,
            temp_use_shortcuts
        )


if __name__ == "__main__":

    #read in the compound hierarchy
    compound_nx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_7_prepare_compound_hierarchy/classyfire_ont_with_bins_added.bin'
    compound_nx=nx.readwrite.gpickle.read_gpickle(compound_nx_address)
    #the ont reader that we used early in the snakemake is insane and the ancestor/descedant relationship is backwards
    compound_nx=nx.DiGraph.reverse(compound_nx)

    #read in the species, organ, disease hiearchies
    species_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_11_prepare_species_networkx/species_networkx.bin'
    organ_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_12_prepare_organ_and_disease_networkx/organ_networkx.bin'
    disease_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_12_prepare_organ_and_disease_networkx/disease_networkx.bin'
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


    pprint(my_MainClass.ComparisonRequest.valid_node_triplets_dict['from'])
    hold=input('hold')

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
