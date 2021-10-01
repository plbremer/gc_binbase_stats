import multiprocessing
from SingleCompoundEvaluator import *


class AllCompoundEvaluator:
    '''
    basically a wrapper for SingleCompoundEvaluator
    '''

    def __init__(self, temp_compound_nodelist, temp_use_multiprocessing, temp_fold_matrix_base_address, temp_base_output_address, temp_species_nx,temp_organ_nx,temp_disease_nx,temp_node_triplets_from,temp_node_triplets_to,temp_from_nodes_to_nodes_equal,temp_use_shortcuts):
        '''
        '''
        self.compound_nodelist=list(temp_compound_nodelist)
        self.use_multiprocessing=temp_use_multiprocessing
        self.fold_matrix_base_address=temp_fold_matrix_base_address
        self.base_output_address=temp_base_output_address
        self.species_nx=temp_species_nx
        self.organ_nx=temp_organ_nx
        self.disease_nx=temp_disease_nx
        self.node_triplets_from=temp_node_triplets_from
        self.node_triplets_to=temp_node_triplets_to
        self.from_nodes_to_nodes_equal=temp_from_nodes_to_nodes_equal,
        self.use_shortcuts=temp_use_shortcuts

    def evaluate_all_compounds_wrapper(self):
        '''
        If someone wanted to do this on their own computer, then they would probably choose a swatch of compounds
        and evaluate all of them, where each compound is evaulated on an individual processor

        For now, since we might just precompute everything, we keep multiprocessing false
        '''
        print(self.use_multiprocessing)
        if self.use_multiprocessing==False:
            
            for temp_compound in self.compound_nodelist:
                print(temp_compound)
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


        elif self.use_multiprocessing==True:
            #num_processes = multiprocessing.cpu_count()
            num_processes=5
            pool = multiprocessing.Pool(processes=num_processes)
            chunk_size = len(self.compound_nodelist)//num_processes

            compound_nodelist_iterable=list()

            for i in range(0,num_processes):
                if i<(num_processes-1):
                    compound_nodelist_iterable.append(self.compound_nodelist[i*chunk_size:(i+1)*chunk_size])
                elif i==(num_processes-1):
                    compound_nodelist_iterable.append(self.compound_nodelist[i*chunk_size:])

            print(compound_nodelist_iterable)
            hold=input('compound_nodelist_iterable')
            pool.map(self.evaluate_all_compounds_multi,compound_nodelist_iterable)

    '''
        species_nodelist_iterable=list()
        for i in range(0,num_processes):
            if i<(num_processes-1):
                species_nodelist_iterable.append(self.species_nodelist[temp_source][i*chunk_size:(i+1)*chunk_size])
            elif i==(num_processes-1):
                species_nodelist_iterable.append(self.species_nodelist[temp_source][i*chunk_size:])
        transformed_chunks=pool.starmap(self.fill_combination_list,zip(species_nodelist_iterable,itertools.repeat(temp_source)))
        pool.close()
        pool.join()

        #recombine chunks
        for i in range(len(transformed_chunks)):
            self.valid_node_triplets_list[temp_source]+=(transformed_chunks[i])
    '''

    def evaluate_all_compounds_multi(self,temp_compound_nodelist):
        '''
        '''

        for temp_compound in temp_compound_nodelist:
            print(temp_compound)
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
            if self.use_shortcuts==True:
                temp_SingleCompoundEvaluator.evaluate_from()
            elif self.use_shortcuts==False:
                temp_SingleCompoundEvaluator.evaluate_from_no_shortcuts()

            temp_SingleCompoundEvaluator.save_result()

