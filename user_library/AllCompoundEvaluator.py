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
        If someone wanted to do this on their own computer, then they would probably choose a swatch of compounds
        and evaluate all of them, where each compound is evaulated on an individual processor

        For now, since we might just precompute everything, we keep multiprocessing false
        '''
        print(self.use_multiprocessing)
        if self.use_multiprocessing==False:
            
            for temp_compound in self.compound_nodelist:

                temp_fold_matrix=pandas.read_pickle(self.fold_matrix_base_address+str(temp_compound)+'.bin')
                temp_SingleCompoundEvaluator=SingleCompoundEvaluator(
                    temp_fold_matrix,
                    self.species_nx,
                    self.organ_nx,
                    self.disease_nx,
                    self.node_triplets_from,
                    self.node_triplets_to,
                    self.base_output_address,
                    temp_compound,
                    self.from_nodes_to_nodes_equal
                )

                temp_SingleCompoundEvaluator.evaluate_from()

                temp_SingleCompoundEvaluator.save_result()