import numpy as np
import networkx as nx
from SingleResultCalculator import *
import pandas

class SingleCompoundEvaluator:
    '''
    Basically a wrapper for SingleResultCalculator
    '''
    def __init__ (
        self,
        temp_fold_matrix,
        temp_species_nx,
        temp_organ_nx,
        temp_disease_nx,
        temp_from_dict,
        temp_to_dict,
        temp_base_address,
        temp_compound,
        temp_from_nodes_to_nodes_equal
    ):
        '''
        '''
        self.fold_matrix=temp_fold_matrix
        self.species_nx=temp_species_nx
        self.organ_nx=temp_organ_nx
        self.disease_nx=temp_disease_nx
        self.from_dict=temp_from_dict
        self.to_dict=temp_to_dict        
        self.base_address=temp_base_address
        self.compound=temp_compound
        self.from_nodes_to_nodes_equal=temp_from_nodes_to_nodes_equal
        #print(self)
        #print(temp_species_nx)
        #print(self.species_nx)
        #hold=input('hold')
        #for temp_node in self.species_nx.nodes:
        #    print(self.species_nx.nodes[temp_node])

        #print(self.species_nx.nodes)

        self.declare_global_recording_dict()
    
    def declare_global_recording_dict(self):
        self.recording_dict={
        'disease_node_from': list(),
        'disease_node_from_path': list(),
        'disease_node_to': list(),
        'disease_node_to_path': list(),
        'fold_change': list(),
        'included_triplets_from': list(),
        'included_triplets_to': list(),
        'organ_node_from': list(),
        'organ_node_from_path': list(),
        'organ_node_to': list(),
        'organ_node_to_path': list(),
        'species_node_from': list(),
        'species_node_to': list(),  
        }
    
    #def visualize

    def remove_nodes_not_chosen_by_user(self,temp_long_list,temp_list_to_keep):
        '''
        the reason that we do this fancy removal is that we want to preserve the special traversal order
        '''
        temp_shortened_list=list()
        for element in temp_long_list:
            if element in temp_list_to_keep:
                temp_shortened_list.append(element)

        return temp_shortened_list
        
    def evaluate_from(self):
        '''
        '''
        
        #create ordered traversal through species, organ disease (these are always the same so we put outside loop)
        species_traversal_list=list(nx.algorithms.traversal.depth_first_search.dfs_postorder_nodes(self.species_nx,source='1'))
        organ_traversal_list=list(nx.algorithms.traversal.depth_first_search.dfs_postorder_nodes(self.organ_nx,source='organ'))
        disease_traversal_list=list(nx.algorithms.traversal.depth_first_search.dfs_postorder_nodes(self.disease_nx,source='disease'))

        ##print(species_traversal_list)
        #remove species that are not referenced by the user subset selection
        species_traversal_sublist=self.remove_nodes_not_chosen_by_user(species_traversal_list,self.from_dict.keys())
        ##print(species_traversal_sublist)
        #create a list of skippables that will be updated as necessary, since we shoudl not update teh list tha we are traversing over
        species_traversal_skips=list()

        #iterate through specices
        for temp_species in species_traversal_sublist:
            print('-------------------------')
            print('to')
            print('species_traversal_sublist')
            print(species_traversal_sublist)
            print('temp_species')
            print(temp_species)
            print('species_traversal_skips')
            print(species_traversal_skips)
            if temp_species in species_traversal_skips:
                continue
            
            #print(temp_species)
            found_at_least_one_result_for_current_species=False
            #print(organ_traversal_list)
            #create the organ traversal sublist that is referred to by temp_species
            organ_traversal_sublist=self.remove_nodes_not_chosen_by_user(organ_traversal_list,self.from_dict[temp_species].keys())
            #print(organ_traversal_sublist)
            #create a list of skippables that will be updated as necessary, since we shoudl not update teh list tha we are traversing over
            organ_traversal_skips=list()

            for temp_organ in organ_traversal_sublist:
                print(organ_traversal_sublist)
                print(temp_organ)
                if temp_organ in organ_traversal_skips:
                    continue

                found_at_least_one_result_for_current_organ=False
                disease_traversal_sublist=self.remove_nodes_not_chosen_by_user(disease_traversal_list,self.from_dict[temp_species][temp_organ])
                disease_traversal_skips=list()

                for temp_disease in disease_traversal_sublist:
                    if temp_disease in disease_traversal_skips:
                        continue

                    #=False
                    #print(temp_species+' '+temp_organ+' '+temp_disease)
                    #if self.from_nodes_to_nodes_equal==True:
                    found_at_least_one_result_for_current_disease=self.evaluate_to(temp_species,temp_organ,temp_disease)
                    #elif from_nodes_to_nodes_equal==False:
                    #found_at_least_one_result_for_current_disease=self.evaluate_to(temp_species,temp_organ,temp_disease)
                    #found_at_least_one_result_for_current_disease=False

                    if found_at_least_one_result_for_current_disease==True:
                        #add ancestors of temp_disease to disease_traversal_skips
                        found_at_least_one_result_for_current_organ=True
                    elif found_at_least_one_result_for_current_disease==False:
                        disease_traversal_skips+=list(nx.algorithms.dag.ancestors(self.disease_nx,temp_disease))


                if found_at_least_one_result_for_current_organ==True:
                    found_at_least_one_result_for_current_species=True
                    #add ancestors of temp_organ to organ traversal skips
                elif found_at_least_one_result_for_current_organ==False:
                    organ_traversal_skips+=list(nx.algorithms.dag.ancestors(self.organ_nx,temp_organ))

            if found_at_least_one_result_for_current_species==False:
                species_traversal_skips+=list(nx.algorithms.dag.ancestors(self.species_nx,temp_species))
            #hold=input('hold')

    def evaluate_to(self,temp_species_from,temp_organ_from,temp_disease_from):
        '''
        '''
        #create ordered traversal through species, organ disease (these are always the same so we put outside loop)
        species_traversal_list=list(nx.algorithms.traversal.depth_first_search.dfs_postorder_nodes(self.species_nx,source='1'))
        organ_traversal_list=list(nx.algorithms.traversal.depth_first_search.dfs_postorder_nodes(self.organ_nx,source='organ'))
        disease_traversal_list=list(nx.algorithms.traversal.depth_first_search.dfs_postorder_nodes(self.disease_nx,source='disease'))

        #print(species_traversal_list)
        #remove species that are not referenced by the user subset selection
        species_traversal_sublist=self.remove_nodes_not_chosen_by_user(species_traversal_list,self.to_dict.keys())
        print(temp_species_from)
        print(species_traversal_sublist)
        print(species_traversal_sublist.index(temp_species_from))
        if self.from_nodes_to_nodes_equal==True:
            #if the from and to lists are the same, then, from the species nx traversal list, remove all nodes upto and including
            #the current from species
            species_traversal_sublist=species_traversal_sublist[species_traversal_sublist.index(temp_species_from):]
        
        print(species_traversal_sublist)
        hold=input('check proper removal on species traversal sublist')

        
        #print(species_traversal_sublist)
        #create a list of skippables that will be updated as necessary, since we shoudl not update teh list tha we are traversing over
        species_traversal_skips=list()

        found_at_least_one_finding_for_entire_to_nxs=False
        #iterate through specices
        for temp_species in species_traversal_sublist:
            #print('-------------------------')
            #print('to')
            #print('species_traversal_sublist')
            #print(species_traversal_sublist)
            #print('temp_species')
            #print(temp_species)
            #print('species_traversal_skips')
            #print(species_traversal_skips)
            if temp_species in species_traversal_skips:
                continue
            
            #print(temp_species)
            found_at_least_one_result_for_current_species=False
            #print(organ_traversal_list)
            #create the organ traversal sublist that is referred to by temp_species
            organ_traversal_sublist=self.remove_nodes_not_chosen_by_user(organ_traversal_list,self.to_dict[temp_species].keys())
            #print(organ_traversal_sublist)
            #create a list of skippables that will be updated as necessary, since we shoudl not update teh list tha we are traversing over
            organ_traversal_skips=list()

            for temp_organ in organ_traversal_sublist:
                if temp_organ in organ_traversal_skips:
                    continue

                found_at_least_one_result_for_current_organ=False
                disease_traversal_sublist=self.remove_nodes_not_chosen_by_user(disease_traversal_list,self.to_dict[temp_species][temp_organ])
                disease_traversal_skips=list()

                for temp_disease in disease_traversal_sublist:
                    if temp_disease in disease_traversal_skips:
                        continue

                    #print('from '+temp_species_from+' '+temp_organ_from+' '+temp_disease_from)                    
                    #print('to '+temp_species+' '+temp_organ+' '+temp_disease)
                    
                    temp_SingleResultCalculator=SingleResultCalculator(self.fold_matrix,self.species_nx,self.organ_nx,self.disease_nx,True)
                    #SHOULD BE A GLOBAL VARIABLE THAT WE PUT THE RESULT ONTO
                    temp_SingleResultCalculator.calculate_one_result(
                        {
                            'species':temp_species_from,
                            'organ':temp_organ_from,
                            'disease':temp_disease_from
                        },
                        {
                            'species':temp_species,
                            'organ':temp_organ,
                            'disease':temp_disease
                        }
                    )
                    #current_to_from_combination=
                    #pprint(temp_SingleResultCalculator.current_result)
                    #hold=input('hold')
                    
                    ######## NEED TO MAKE 5 A HYPERPARAMETER #########
                    if (
                        temp_SingleResultCalculator.current_result==None or
                        np.isnan(temp_SingleResultCalculator.current_result['fold_change'][0]) or
                        abs(temp_SingleResultCalculator.current_result['fold_change'][0]) < 10
                    ):
                        found_at_least_one_result_for_current_disease=False
                    else:
                        found_at_least_one_result_for_current_disease=True
                        for temp_key in self.recording_dict.keys():
                            self.recording_dict[temp_key].append(temp_SingleResultCalculator.current_result[temp_key][0])
                    

                    if found_at_least_one_result_for_current_disease==True:
                        found_at_least_one_result_for_current_organ=True
                        #differs compared to from. this is the thing that we ultimately return
                        found_at_least_one_finding_for_entire_to_nxs=True
                    elif found_at_least_one_result_for_current_disease==False:
                        #add ancestors of temp_disease to disease_traversal_skips
                        disease_traversal_skips+=list(nx.algorithms.dag.ancestors(self.disease_nx,temp_disease))

                if found_at_least_one_result_for_current_organ==True:
                    found_at_least_one_result_for_current_species=True
                elif found_at_least_one_result_for_current_organ==False:
                    #add ancestors of temp_organ to organ traversal skips
                    organ_traversal_skips+=list(nx.algorithms.dag.ancestors(self.organ_nx,temp_organ))

            if found_at_least_one_result_for_current_species==False:
                species_traversal_skips+=list(nx.algorithms.dag.ancestors(self.species_nx,temp_species))

        #hold=input('finished to')
        return found_at_least_one_finding_for_entire_to_nxs

    def save_result(self):
        '''
        '''
        self.recording_dataframe=pandas.DataFrame.from_dict(self.recording_dict)
        self.recording_dataframe.to_pickle(self.base_address+str(self.compound)+'.bin')


if __name__ == "__main__":

    species_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_11_prepare_species_networkx/species_networkx.bin'
    '''
    organ_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_12_prepare_organ_and_disease_networkx/organ_networkx.bin'
    disease_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_12_prepare_organ_and_disease_networkx/disease_networkx.bin'

    species_nx=nx.readwrite.gpickle.read_gpickle(species_networkx_address)
    organ_nx=nx.readwrite.gpickle.read_gpickle(organ_networkx_address)
    disease_nx=nx.readwrite.gpickle.read_gpickle(disease_networkx_address)

    one_compound_fold_matrix_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_8_perform_compound_hierarchical_analysis/each_compounds_fold_matrix/all_fold_matrices/2.bin'
    fold_matrix=pandas.read_pickle(one_compound_fold_matrix_address)

    my_SingleCompoundEvaluator=SingleCompoundEvaluator(
        species_nx,
        organ_nx,
        disease_nx,
        temp_from_dict,
        temp_to_dict
    )
    '''
