import multiprocessing
from SingleCompoundEvaluator import *


class AllCompoundEvaluator:
    '''
    basically a wrapper for SingleCompoundEvaluator
    '''

    def __init__(self, temp_compound_nodelist, temp_use_multiprocessing, temp_fold_matrix_base_address, temp_base_output_address, temp_species_nx,temp_organ_nx,temp_disease_nx,temp_node_triplets_from,temp_node_triplets_to,temp_from_nodes_to_nodes_equal):
        '''
        '''
        self.compound_nodelist=temp_compound_nodelist
        self.use_multiprocessing=temp_use_multiprocessing
        self.fold_matrix_base_address=temp_fold_matrix_base_address
        self.base_output_address=temp_base_output_address
        self.species_nx=temp_species_nx
        self.organ_nx=temp_organ_nx
        self.disease_nx=temp_disease_nx
        self.node_triplets_from=temp_node_triplets_from
        self.node_triplets_to=temp_node_triplets_to
        self.from_nodes_to_nodes_equal=temp_from_nodes_to_nodes_equal

    def evaluate_all_compounds(self):
        '''
        '''
        print(self.use_multiprocessing)
        if self.use_multiprocessing==False:
            
            for temp_compound in self.compound_nodelist:

                temp_fold_matrix=pandas.read_pickle(self.fold_matrix_base_address+str(temp_compound)+'.bin')
                print(temp_compound)
                ##print(self.fold_matrix_base_address+str(temp_compound)+'.bin')
                #hold=input('hold')
                temp_SingleCompoundEvaluator=SingleCompoundEvaluator(
                    #fold_matrix,
                    temp_fold_matrix,
                    #species_nx,
                    self.species_nx,
                    #organ_nx,
                    self.organ_nx,
                    #disease_nx,
                    self.disease_nx,
                    #my_MainClass.ComparisonRequest.valid_node_triplets_dict['from'],
                    self.node_triplets_from,
                    #my_MainClass.ComparisonRequest.valid_node_triplets_dict['to'],
                    self.node_triplets_to,
                    #self.base_output_address,
                    self.base_output_address,
                    #temp_compound
                    temp_compound,
                    self.from_nodes_to_nodes_equal
                )

                temp_SingleCompoundEvaluator.evaluate_from()

                #temp_SingleCompoundEvaluator.save_result(self.base_output_address,temp_compound)
                temp_SingleCompoundEvaluator.save_result()

