#glitch if #species < # processors
import pandas
import networkx as nx
import multiprocessing
import random
#import matplotlib.pyplot as plt
#plt.switch_backend('agg')
from pprint import pprint
import itertools

class ComparisonRequest():
    '''
    The purpose of this class is to receive a "complete" set of nodes from something else
    (so, after the species, organ, disease networkx trees have been selected)
    There is an implied combination set for any "three way list of nodes"
    Thus, the goal of this class is to reduce the "complete combination" space to a smaller combination
    Space where each combination has at least 1 valid entry

    that is, it removes things like ('human','leaf','lung cancer')

    The results of this analysis can be complete from any fold matrix, but apply to all compounds
    '''
    def __init__(
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

        self.fold_matrix=temp_fold_matrix
        self.species_nx=temp_species_nx
        self.organ_nx=temp_organ_nx
        self.disease_nx=temp_disease_nx
        self.species_nodelist={
            'from':temp_species_nodelist_from,
            'to':temp_species_nodelist_to
        }
        self.organ_nodelist={
            'from':temp_organ_nodelist_from,
            'to':temp_organ_nodelist_to
        }
        self.disease_nodelist={
            'from':temp_disease_nodelist_from,
            'to':temp_disease_nodelist_to
        }

        self.assign_binvestigate_triplet_list()

        self.valid_node_triplets_list={
            'from':[],
            'to':[]
        }
        self.valid_node_triplets_dict={
            'from':{},
            'to':{}            
        }

    def assign_binvestigate_triplet_list(self):
        '''
        assigns the fold change matrix row/column as an explicit attribute of CommparisonRequest
        not technically necessary, but helpful
        The fold matrices are symmetrical so choosing index or column for would have worked
        '''
        self.binvestigate_triplet_panda=pandas.DataFrame(self.fold_matrix.index.values)
        self.binvestigate_triplet_panda=self.binvestigate_triplet_panda[0].apply(pandas.Series)
        self.binvestigate_triplet_panda.columns=['organ','species','disease']        

    def create_full_node_triplet_list(self,temp_species_list,temp_source):
        '''
        at the moment, never called
        '''
        temp_triplet_node_list=list()
        for temp_species in temp_species_list[temp_source]:
            for temp_organ in self.organ_nodelist[temp_source]:
                for temp_disease in self.disease_nodelist[temp_source]:
                    temp_triplet_node_list.append((temp_species,temp_organ,temp_disease))

        return temp_triplet_node_list

    def fill_combination_dict_wrapper(self,temp_source):
        '''
        Because the total number of species*organ*disease can be very large
        We write a wrapper function so that the actual procedure can be multi-processed
        '''
        
        #prepare multiprocessing
        num_processes = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=4)
        
        #split the species list into equally sized chunks
        #since the results are going into a dict (intrinsically unordered)
        #we shuffle first because results times probably a function of hierarchy level
        chunk_size = len(self.species_nodelist[temp_source])//num_processes
        random.shuffle(self.species_nodelist[temp_source])
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


    def fill_combination_list(self,temp_species_list,temp_source):
        '''
        There is a distinct form of the data that we assume
        We assume that the data is the full outer product of species, organ, disease
        Therefore, test all possible combos
        We keep those triplets that refer to at least one row in the fold matrix

        temp source is the word 'from' or 'to'
        '''

        temp_list_for_analysis=list()

        for i, temp_species in enumerate(temp_species_list):
            print(i)

            temp_species_nodeset=nx.algorithms.dag.descendants(self.species_nx,temp_species)
            temp_species_nodeset.add(temp_species)
            temp_triplet_view_after_species_filter=self.binvestigate_triplet_panda.loc[self.binvestigate_triplet_panda['species'].isin(temp_species_nodeset)]

            for temp_organ in self.organ_nodelist[temp_source]:
                temp_organ_nodeset=nx.algorithms.dag.descendants(self.organ_nx,temp_organ)
                temp_organ_nodeset.add(temp_organ)
                temp_organ_meshlabel_filter_list=[self.organ_nx.nodes[temp_node]['mesh_label'] for temp_node in temp_organ_nodeset]
                temp_triplet_view_after_organ_filter=temp_triplet_view_after_species_filter.loc[temp_triplet_view_after_species_filter['organ'].isin(temp_organ_meshlabel_filter_list)]

                for temp_disease in self.disease_nodelist[temp_source]:
                    temp_disease_nodeset=nx.algorithms.dag.descendants(self.disease_nx,temp_disease)
                    temp_disease_nodeset.add(temp_disease)
                    temp_disease_meshlabel_filter_list=[self.disease_nx.nodes[temp_node]['mesh_label'] for temp_node in temp_disease_nodeset]
                    
                    temp_triplet_view_after_disease_filter=temp_triplet_view_after_organ_filter.loc[temp_triplet_view_after_organ_filter['disease'].isin(temp_disease_meshlabel_filter_list)]

                    if (len(temp_triplet_view_after_disease_filter.index) > 0):
                        temp_list_for_analysis.append((temp_species,temp_organ,temp_disease))

        return temp_list_for_analysis
  
    def convert_combination_list_to_dict(self,temp_source):
        '''
        A dict is more friendly to the traversal procedure (if we find nothing for a certain key, we can just remove/skip that entire
        value set)
        So we cast the list into a dict
        '''
        for element in self.valid_node_triplets_list[temp_source]:

            if element[0] not in self.valid_node_triplets_dict[temp_source]:
                self.valid_node_triplets_dict[temp_source][element[0]]=dict()

            if element[1] not in self.valid_node_triplets_dict[temp_source][element[0]]:
                self.valid_node_triplets_dict[temp_source][element[0]][element[1]]=list()

            self.valid_node_triplets_dict[temp_source][element[0]][element[1]].append(element[2])

        pprint(self.valid_node_triplets_dict[temp_source])

'''
if __name__ == "__main__":

    one_compound_fold_matrix_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_8_perform_compound_hierarchical_analysis/each_compounds_fold_matrix/all_fold_matrices/2.bin'
    species_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_11_prepare_species_networkx/species_networkx.bin'
    organ_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_12_prepare_organ_and_disease_networkx/organ_networkx.bin'
    disease_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_12_prepare_organ_and_disease_networkx/disease_networkx.bin'

    fold_matrix=pandas.read_pickle(one_compound_fold_matrix_address)
    species_nx=nx.readwrite.gpickle.read_gpickle(species_networkx_address)
    organ_nx=nx.readwrite.gpickle.read_gpickle(organ_networkx_address)
    disease_nx=nx.readwrite.gpickle.read_gpickle(disease_networkx_address)

    species_nodelist_from=['2','2093','641','678','668']
    species_nodelist_to=['314146','9443','9526','9544','9606','39107','10090','10114','10116','10117']
    organ_nodelist_from=['A01', 'A08', 'A11', 'A15', 'A15.145', 'A12', 'A12.207', 'A12.207.270', 'A11.436', 'A08.186.211', 'A12.207.152', 'A12.207.152.693', 'A12.207.270.695', 'A15.145.693', 'A05', 'A04', 'A12.207.152.846', 'A05.810.890', 'A01.236', 'A04.411', 'A18', 'A12.207.927', 'A18.024.937', 'A15.145.846', 'A11.284.295.260', 'A04.411.715.100', 'A11.436.081', 'organ']
    organ_nodelist_to=['A01', 'A08', 'A11', 'A15', 'A15.145', 'A12', 'A12.207', 'A12.207.270', 'A11.436', 'A08.186.211', 'A12.207.152', 'A12.207.152.693', 'A12.207.270.695', 'A15.145.693', 'A05', 'A04', 'A12.207.152.846', 'A05.810.890', 'A01.236', 'A04.411', 'A18', 'A12.207.927', 'A18.024.937', 'A15.145.846', 'A11.284.295.260', 'A04.411.715.100', 'A11.436.081', 'organ']
    disease_nodelist_from=['C04.588.180', 'C17.800.090.500', 'C04.588.894.797.520.109.220', 'C17', 'C04.588', 'C08.785.520.100.220', 'C04', 'C08.381.540.140', 'C08', 'No', 'disease']
    disease_nodelist_to=['C04.588.180', 'C17.800.090.500', 'C04.588.894.797.520.109.220', 'C17', 'C04.588', 'C08.785.520.100.220', 'C04', 'C08.381.540.140', 'C08', 'No', 'disease']

    my_ComparisonRequest=ComparisonRequest(
        fold_matrix,
        species_nx,
        organ_nx,
        disease_nx,
        species_nodelist_from,
        species_nodelist_to,
        organ_nodelist_from,
        organ_nodelist_to,
        disease_nodelist_from,
        disease_nodelist_to,        
    )

    my_ComparisonRequest.fill_combination_dict_wrapper('from')
    my_ComparisonRequest.convert_combination_list_to_dict('from')

    my_ComparisonRequest.fill_combination_dict_wrapper('to')
    my_ComparisonRequest.convert_combination_list_to_dict('to')
'''