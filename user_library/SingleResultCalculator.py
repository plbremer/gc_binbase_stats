'''
i believe that i need to update this so that it handles "sub position" nodes
ie human vs mammals
'''

import numpy as np
import pandas
import networkx as nx
from pprint import pprint
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import re

class SingleResultCalculator():
    '''
    '''

    def __init__(self,temp_fold_matrix,temp_species_nx,temp_organ_nx,temp_disease_nx,temp_verbose):
        '''
        '''
        self.fold_matrix=temp_fold_matrix
        self.species_nx=temp_species_nx
        self.organ_nx=temp_organ_nx
        self.disease_nx=temp_disease_nx
        self.assign_binvestigate_triplet_list()
        self.verbose=temp_verbose
    
    def assign_binvestigate_triplet_list(self):
        '''
        assigns the fold change matrix row/column as an explicit attribute of SingleResultCalculator
        not technically necessary, but helpful
        The fold matrices are symmetrical so choosing index or column for would have worked
        '''
        ##print(self.fold_matrix)
        ##hold=input('hold')
        self.binvestigate_triplet_panda=pandas.DataFrame(self.fold_matrix.index.values)
        self.binvestigate_triplet_panda=self.binvestigate_triplet_panda[0].apply(pandas.Series)
        self.binvestigate_triplet_panda.columns=['organ','species','disease']

    def calculate_one_result(self,temp_node_triplet_from,temp_node_triplet_to):
        '''
        Goes through all of the steps associated with calculating a single result that comes from two
        triplets.
        For organ/disease, the triplet words can be mesh paths (e.g. A11.234.352) or english words (e.g. "Cell")
        '''
        ##print(temp_node_triplet_from)
        ##print(temp_node_triplet_to)
        ##print('--------------')
        
        #convert the english triplet to lists of subgraphs. possible to have more than one subgraph per mesh_label for organ and disease
        self.prepare_subgraphs(temp_node_triplet_from,temp_node_triplet_to)
        ##pprint(self.binvestigate_subgraphs)
        ##hold=input('----------')
        #convert the full node sets to words that are on the fold matrix
        self.identify_binvestigate_triplets()
        ##pprint(self.binvestigate_entries_per_subgraph)
        ##hold=input('---------')
        
        ##print('---------')
        
        
        self.create_combinations()
        ##pprint(self.combination_list)
        ##pprint(self.combination_list_headnode)
        ##hold=input('combination_list')


        self.reduce_combinations_per_sub_super_sets()
        ##pprint(self.combination_list)
        ##hold=input('post reduction')


        #do the calculation 
        self.create_result_dict(temp_node_triplet_from,temp_node_triplet_to)

    def prepare_subgraphs(self,temp_node_triplet_from,temp_node_triplet_to):
        '''
        The purpose of this function is to receive two  triplet (species, organ, disease) of labels as a human would write them (english words)
        Or two triplets wih the mesh paths instead of mesh labels

        And then convert each entry in each triplet to a list of subgraphs that are each a set of nodes
        The reason for the complication associated with english mesh labels is that a mesh label can have multple locations in the mesh hierarchy
        And therefore for any given organ or disease, we must create a list of subgraphs
        '''
        binvestigate_subgraphs={
            'species_from':[],
            'species_to':[],
            'organ_from':[],
            'organ_to':[],
            'disease_from':[],
            'disease_to':[]
        }

        binvestigate_subgraph_headnodes={
            'species_from':[],
            'species_to':[],
            'organ_from':[],
            'organ_to':[],
            'disease_from':[],
            'disease_to':[]
        }

        binvestigate_subgraphs['species_from'].append(nx.algorithms.dag.descendants(self.species_nx,temp_node_triplet_from['species']))
        #descendants returns a set and we want to add to the set, which is the first item in the list
        binvestigate_subgraphs['species_from'][0].add(temp_node_triplet_from['species'])
        binvestigate_subgraph_headnodes['species_from'].append(temp_node_triplet_from['species'])
        binvestigate_subgraphs['species_to'].append(nx.algorithms.dag.descendants(self.species_nx,temp_node_triplet_to['species']))
        binvestigate_subgraphs['species_to'][0].add(temp_node_triplet_to['species'])
        binvestigate_subgraph_headnodes['species_to'].append(temp_node_triplet_to['species'])

        #if we receive an organ and/or disease name that is already  in "mesh hierarchy format"
        #then we do not need to call the convert_mesh_lable_to_mesh_node_list
        #otherwise
        #we gather a list of nodes for each mesh label and then populate the appropriate value in binvestigate_subgraphs
        #if theres a pattern LETTER NUMBER NUMBER and splitting it via . gives an empty list (if we are not dealing with a mesh label)
        if re.search("^[a-zA-Z]\d{2}$",temp_node_triplet_from['organ'].split('.')[0]) is None:
            temp_organ_from_nodes_list=self.convert_mesh_label_to_mesh_node_list(temp_node_triplet_from['organ'],'organ')
        else:
            temp_organ_from_nodes_list=[temp_node_triplet_from['organ']]
            #print(temp_node_triplet_from['organ'].split('.')[0])
        if re.search("^[a-zA-Z]\d{2}$",temp_node_triplet_to['organ'].split('.')[0]) is None:
            temp_organ_to_nodes_list=self.convert_mesh_label_to_mesh_node_list(temp_node_triplet_to['organ'],'organ')
        else:
            temp_organ_to_nodes_list=[temp_node_triplet_to['organ']]
        if re.search("^[a-zA-Z]\d{2}$",temp_node_triplet_from['disease'].split('.')[0]) is None:
            ##print('met condition from')
            temp_disease_from_nodes_list=self.convert_mesh_label_to_mesh_node_list(temp_node_triplet_from['disease'],'disease')
        else:
            temp_disease_from_nodes_list=[temp_node_triplet_from['disease']]
        if re.search("^[a-zA-Z]\d{2}$",temp_node_triplet_to['disease'].split('.')[0]) is None:
            ##print('met condition to')
            temp_disease_to_nodes_list=self.convert_mesh_label_to_mesh_node_list(temp_node_triplet_to['disease'],'disease')
        else:
            temp_disease_to_nodes_list=[temp_node_triplet_to['disease']]

        ##print(temp_disease_from_nodes_list)
        ##print(temp_disease_to_nodes_list)
        ##hold=input('temp nodelists disease from then to')
        ##print(temp_organ_from_nodes_list)
        ##print(temp_organ_to_nodes_list)
        ##hold=input('temp nodelists organ from then to')

        for i, temp_node in enumerate(temp_organ_from_nodes_list):
            binvestigate_subgraphs['organ_from'].append(nx.algorithms.dag.descendants(self.organ_nx,temp_node))
            binvestigate_subgraphs['organ_from'][i].add(temp_node)
            binvestigate_subgraph_headnodes['organ_from'].append(temp_node)
        for i, temp_node in enumerate(temp_organ_to_nodes_list):
            binvestigate_subgraphs['organ_to'].append(nx.algorithms.dag.descendants(self.organ_nx,temp_node))
            binvestigate_subgraphs['organ_to'][i].add(temp_node)
            binvestigate_subgraph_headnodes['organ_to'].append(temp_node)
        for i, temp_node in enumerate(temp_disease_from_nodes_list):
            binvestigate_subgraphs['disease_from'].append(nx.algorithms.dag.descendants(self.disease_nx,temp_node))
            binvestigate_subgraphs['disease_from'][i].add(temp_node)
            binvestigate_subgraph_headnodes['disease_from'].append(temp_node)
        for i, temp_node in enumerate(temp_disease_to_nodes_list):
            binvestigate_subgraphs['disease_to'].append(nx.algorithms.dag.descendants(self.disease_nx,temp_node))
            binvestigate_subgraphs['disease_to'][i].add(temp_node)        
            binvestigate_subgraph_headnodes['disease_to'].append(temp_node)
        
        self.binvestigate_subgraphs=binvestigate_subgraphs
        self.binvestigate_subgraph_headnodes=binvestigate_subgraph_headnodes

    def convert_mesh_label_to_mesh_node_list(self,temp_label,hierarchy_type):
        '''
        for an english word in the mesh hiearchy (as well as a given type of hierarchy - disease or organ)
        find the list of nodes that have that corresponding mesh label
        e.g. Plasma to 'A12.207.152.693' 'A12.207.270.695' 'A15.145.693'
        '''
        #print(temp_label)
        #print(hierarchy_type)
        #nx.draw(self.organ_nx)
        #plt.show()
        if hierarchy_type=='organ':
            #node_list=self.organ_nx.nodes['mesh_label']
            ##print([temp_node for temp_node in self.organ_nx.nodes if self.organ_nx.nodes[temp_node]['mesh_label']==temp_label])
            if temp_label=='Organ':
                return['organ']
            else:
                return [temp_node for temp_node in self.organ_nx.nodes if self.organ_nx.nodes[temp_node]['mesh_label']==temp_label]
        elif hierarchy_type=='disease':
            if temp_label=='Disease':
                return['disease']
            else:
                return [temp_node for temp_node in self.disease_nx.nodes if self.disease_nx.nodes[temp_node]['mesh_label']==temp_label]

    def identify_binvestigate_triplets(self):
        '''
        This takes each of the nodes in each of teh subgraphs for each of the hierarchies
        And finds all of the "nodes (species) or "node labels" (organ, disease) that have entries in the fold matrix
        '''
        self.binvestigate_entries_per_subgraph={
            'species_from':[],
            'species_to':[],
            'organ_from':[],
            'organ_to':[],
            'disease_from':[],
            'disease_to':[]
        }

        for key in self.binvestigate_subgraphs.keys():
            #find if we are workign with species, organ, or disease
            temp_hierarchy_type=key.split('_')[0]
            ##print(temp_hierarchy_type)

            for i, subgraph in enumerate(self.binvestigate_subgraphs[key]):
                ##print(i)
                ##print(self.binvestigate_subgraphs[key][i])
                if temp_hierarchy_type=='species':
                    self.binvestigate_entries_per_subgraph[key].append(self.binvestigate_subgraphs[key][0])
                elif temp_hierarchy_type=='organ':
                    self.binvestigate_entries_per_subgraph[key].append({self.organ_nx.nodes[temp_node]['mesh_label'] for temp_node in self.organ_nx.nodes if temp_node in self.binvestigate_subgraphs[key][i]})
                elif temp_hierarchy_type=='disease':
                    self.binvestigate_entries_per_subgraph[key].append({self.disease_nx.nodes[temp_node]['mesh_label'] for temp_node in self.disease_nx.nodes if temp_node in self.binvestigate_subgraphs[key][i]})

    def create_combinations(self):
        '''
        
        '''
        '''
        self.binvestigate_entries_per_subgraph={
            'species_from':[],
            'species_to':[],
            'organ_from':[],
            'organ_to':[],
            'disease_from':[],
            'disease_to':[]
        }
        '''
        self.combination_list_headnode=list()

        ##print('here')
        self.combination_list=list()
        ##print(self.binvestigate_entries_per_subgraph['organ_from'])
        ##print(len(self.binvestigate_entries_per_subgraph['organ_from']))
        ##print(range(len(self.binvestigate_entries_per_subgraph['organ_from'])))
        for a in range(len(self.binvestigate_entries_per_subgraph['organ_from'])):
            ##print('heres')
            for b in range(len(self.binvestigate_entries_per_subgraph['disease_from'])):
                for c in range(len(self.binvestigate_entries_per_subgraph['organ_to'])):
                    for d in range(len(self.binvestigate_entries_per_subgraph['disease_to'])):
                        self.combination_list.append(
                            {
                                'from':{
                                    'species':self.binvestigate_entries_per_subgraph['species_from'][0],
                                    'organ':self.binvestigate_entries_per_subgraph['organ_from'][a],
                                    'disease':self.binvestigate_entries_per_subgraph['disease_from'][b]
                                },
                                'to':{
                                    'species':self.binvestigate_entries_per_subgraph['species_to'][0],
                                    'organ':self.binvestigate_entries_per_subgraph['organ_to'][c],
                                    'disease':self.binvestigate_entries_per_subgraph['disease_to'][d]
                                }
                            }
                        )
                        self.combination_list_headnode.append(
                            {
                                'from':{
                                    'species':self.binvestigate_subgraph_headnodes['species_from'][0],
                                    'organ':self.binvestigate_subgraph_headnodes['organ_from'][a],
                                    'disease':self.binvestigate_subgraph_headnodes['disease_from'][b]
                                },
                                'to':{
                                    'species':self.binvestigate_subgraph_headnodes['species_to'][0],
                                    'organ':self.binvestigate_subgraph_headnodes['organ_to'][c],
                                    'disease':self.binvestigate_subgraph_headnodes['disease_to'][d]
                                }
                            }
                        )
        #print(self.combination_list_headnode)

    def reduce_combinations_per_sub_super_sets(self):
        '''
        There is a special type of relationship between nodes in the same tree, when one node is in the ancestors/descendants
        of the other node. in this case, the type of calculation that should be done is an "except for" calculation

        That is, if humans versus mammals, one would calculate "all mammals except for humans vs humans"

        of course, it is possible to have contradicting super/sub requests
        mammals, lungs vs humans, all

        where one triplet has one hiearchys supernode and the other triplet has the other hierarchys supernode

        therefore, we need to, for each combination, reduce each tree

        We also want to allow "the same" nodes to be compared (human lungs vs mammal lungs)

        We identify what to do by looking at the combination_list_headnodes and we operate on the combination_list
        '''
        ##print(self.combination_list)
        ##print(self.combination_list_headnode)
        ##hold=input('inside reduce_combinations_pers_sub_super_set')

        for i,temp_calculation_pair in enumerate(self.combination_list_headnode):
            #do the calc once for species, once for organs, once for disease
            if temp_calculation_pair['to']['species'] in nx.algorithms.dag.descendants(self.species_nx,temp_calculation_pair['from']['species']):
                self.combination_list[i]['from']['species']=self.combination_list[i]['from']['species'].difference(self.combination_list[i]['to']['species'])
            elif temp_calculation_pair['from']['species'] in nx.algorithms.dag.descendants(self.species_nx,temp_calculation_pair['to']['species']):
                self.combination_list[i]['to']['species']=self.combination_list[i]['to']['species'].difference(self.combination_list[i]['from']['species'])

            if temp_calculation_pair['to']['organ'] in nx.algorithms.dag.descendants(self.organ_nx,temp_calculation_pair['from']['organ']):
                ##print(self.combination_list[i]['to']['organ'])
                self.combination_list[i]['from']['organ']=self.combination_list[i]['from']['organ'].difference(self.combination_list[i]['to']['organ'])
                ##print(self.combination_list[i]['to']['organ'])
                ##hold=input('should not be here')
            elif temp_calculation_pair['from']['organ'] in nx.algorithms.dag.descendants(self.organ_nx,temp_calculation_pair['to']['organ']):
                ##print(self.combination_list[i]['to']['organ'])
                self.combination_list[i]['to']['organ']=self.combination_list[i]['to']['organ'].difference(self.combination_list[i]['from']['organ'])
                ##print(self.combination_list[i]['to']['organ'])
                ##hold=input('check subtraction')


            if temp_calculation_pair['to']['disease'] in nx.algorithms.dag.descendants(self.disease_nx,temp_calculation_pair['from']['disease']):
                self.combination_list[i]['from']['disease']=self.combination_list[i]['from']['disease'].difference(self.combination_list[i]['to']['disease'])
            elif temp_calculation_pair['from']['disease'] in nx.algorithms.dag.descendants(self.disease_nx,temp_calculation_pair['to']['disease']):
                self.combination_list[i]['to']['disease']=self.combination_list[i]['to']['disease'].difference(self.combination_list[i]['from']['disease'])

    def create_result_dict(self,temp_node_triplet_from,temp_node_triplet_to):
        '''
        receives a set of combinations and iterates through each

        for each iteration, makes a subsetted dataframe, determines what the "result" value is (which represents some combination)]
        then records that value
        '''
        #make a dict
        feature_dict={
            'species_node_from':[],
            'organ_node_from':[],
            'disease_node_from':[],
            'species_node_to':[],
            'organ_node_to':[],
            'disease_node_to':[],
            'included_triplets_from':[],
            'included_triplets_to':[],
            'fold_change':[],
            'organ_node_from_path':[],
            'disease_node_from_path':[],
            'organ_node_to_path':[],
            'disease_node_to_path':[]         
        }

        for i,temp_calculation_pair in enumerate(self.combination_list):
            
            ##print(temp_calculation_pair)
            ##hold=input('temp_calculation_pair')
            ##print(self.fold_matrix)
            temp_fold_matrix_subset_view=self.fold_matrix.loc[
                self.fold_matrix.index.isin(temp_calculation_pair['from']['species'],level='species'),
                self.fold_matrix.columns.isin(temp_calculation_pair['to']['species'],level='species')
            ]
            ##print(temp_fold_matrix_subset_view)
            ##print('----------')
            temp_fold_matrix_subset_view=temp_fold_matrix_subset_view.loc[
                temp_fold_matrix_subset_view.index.isin(temp_calculation_pair['from']['organ'],level='organ'),
                temp_fold_matrix_subset_view.columns.isin(temp_calculation_pair['to']['organ'],level='organ')
            ]
            ##print(temp_fold_matrix_subset_view)
            ##print('----------')
            temp_fold_matrix_subset_view=temp_fold_matrix_subset_view.loc[
                temp_fold_matrix_subset_view.index.isin(temp_calculation_pair['from']['disease'],level='disease'),
                temp_fold_matrix_subset_view.columns.isin(temp_calculation_pair['to']['disease'],level='disease')
            ]            

            ##print(temp_fold_matrix_subset_view)
            
            ##print(len(temp_fold_matrix_subset_view.columns.to_list()))
            ##print(len(temp_fold_matrix_subset_view.index.to_list()))
            
            ##hold=input('post all subsetting')

            #it is possible to have combinations where the original triplet is valid, but after invoking the 
            #except-for subtraction, there ends up being no values
            
            
            if (len(temp_fold_matrix_subset_view.columns.to_list()) == 0) or (len(temp_fold_matrix_subset_view.index.to_list()) == 0):
                self.current_result=None
            else:
                '''
                #conditions=[
                #    np.isnan(temp_fold_matrix_subset_view.values).any(),
                #    all(temp_fold_matrix_subset_view==np.inf),
                #    all(temp_fold_matrix_subset_view==-np.inf),
                #    any(temp_fold_matrix_subset_view<0) and any(temp_fold_matrix_subset_view>0),
                #    any(temp_fold_matrix_subset_view==0),
                #    all(temp_fold_matrix_subset_view>=0.01),
                #    all(temp_fold_matrix_subset_view<=-0.01)
                #]
                #conditions=[
                #    np.isnan(temp_fold_matrix_subset_view.values).any(),
                #    (temp_fold_matrix_subset_view.values==np.inf).all(),
                #    (temp_fold_matrix_subset_view.values==-np.inf).all(),
                #    (temp_fold_matrix_subset_view.values<0).any() and (temp_fold_matrix_subset_view.values>0).any(),
                #    (temp_fold_matrix_subset_view.values==0).any(),
                #    (temp_fold_matrix_subset_view.values>=0.01).all(),
                    (temp_fold_matrix_subset_view.values<=-0.01).all()
                ]

                choices=[
                    np.nan,
                    np.inf,
                    -np.inf,
                    np.nan,
                    np.nan,
                    min(temp_fold_matrix_subset_view),
                    max(temp_fold_matrix_subset_view)
                ]
                print(temp_fold_matrix_subset_view.values)
                print(temp_fold_matrix_subset_view.to_numpy())
                
                print(np.select(conditions,choices))
                hold=input('np select')
                #print(self.binvestigate_subgraph_headnodes)
                '''
                #
                #print(one_df_transform(temp_fold_matrix_subset_view.values))
                #hold=input('np select')
                feature_dict['fold_change'].append( float(self.one_df_transform(temp_fold_matrix_subset_view.values)) )
                feature_dict['species_node_from'].append(temp_node_triplet_from['species'])
                feature_dict['organ_node_from'].append(temp_node_triplet_from['organ'])
                feature_dict['disease_node_from'].append(temp_node_triplet_from['disease'])
                feature_dict['species_node_to'].append(temp_node_triplet_to['species'])
                feature_dict['organ_node_to'].append(temp_node_triplet_to['organ'])
                feature_dict['disease_node_to'].append(temp_node_triplet_to['disease'])
                feature_dict['included_triplets_from'].append( temp_fold_matrix_subset_view.index.values.tolist() )
                feature_dict['included_triplets_to'].append( temp_fold_matrix_subset_view.columns.values.tolist() )
                #in case we end up with a null dataframe
    #            try:
                #feature_dict['fold_change'].append(np.select(conditions,choices))
    #            except ValueError:


                feature_dict['organ_node_from_path'].append(self.combination_list_headnode[i]['from']['organ'])
                feature_dict['disease_node_from_path'].append(self.combination_list_headnode[i]['from']['disease'])
                feature_dict['organ_node_to_path'].append(self.combination_list_headnode[i]['to']['organ'])
                feature_dict['disease_node_to_path'].append(self.combination_list_headnode[i]['to']['disease'])
                #['organ_from'][i]),
                #feature_dict['disease_node_from_path'].append(self.binvestigate_subgraph_headnodes['disease_from'][i]),
                #feature_dict['organ_node_to_path'].append(self.binvestigate_subgraph_headnodes['organ_to'][i]),
                #feature_dict['disease_node_to_path'].append(self.binvestigate_subgraph_headnodes['disease_to'][i])
            
            
                self.current_result=feature_dict
        #pprint(feature_dict)
        #hold=input('hold')
        #return feature_dict

#def one_column_custom_aggregation(temp_column):
#    return temp_column.groupby(level=('organ','species','disease')).agg(func=one_cell_transform)

    def one_df_transform(self, temp_df):
        '''
        given an numpy array, chooses what the aggregate value is
        '''
        conditions=[
            np.isnan(temp_df).any(),
            (temp_df==np.inf).all(),
            (temp_df==-np.inf).all(),
            (temp_df<0).any() and (temp_df>0).any(),
            (temp_df==0).any(),
            (temp_df>0).all(),
            (temp_df<0).all()
        ]
        
        choices=[
            np.nan,
            np.inf,
            -np.inf,
            0,
            0,
            temp_df.min(),
            temp_df.max()
        ]
        return np.select(conditions,choices)


if __name__ == "__main__":

    one_compound_fold_matrix_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_8_perform_compound_hierarchical_analysis/each_compounds_fold_matrix/all_fold_matrices/2.bin'
    species_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_11_prepare_species_networkx/species_networkx.bin'
    organ_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_12_prepare_organ_and_disease_networkx/organ_networkx.bin'
    disease_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_12_prepare_organ_and_disease_networkx/disease_networkx.bin'

    fold_matrix=pandas.read_pickle(one_compound_fold_matrix_address)
    species_nx=nx.readwrite.gpickle.read_gpickle(species_networkx_address)
    organ_nx=nx.readwrite.gpickle.read_gpickle(organ_networkx_address)
    disease_nx=nx.readwrite.gpickle.read_gpickle(disease_networkx_address)

    #nx.draw(species_nx)
    #plt.show()

    my_SingleResultCalculator=SingleResultCalculator(fold_matrix,species_nx,organ_nx,disease_nx,True)

    
    #test_from_triplet={
    #    'species':'9606',
    #    'organ':'Plasma',
    #    'disease':'No'
    #}
    #test_to_triplet={
    #    'species':'9606',
    #    'organ':'Lung',
    #    'disease':'No'
    #}
    
    #test_from_triplet={
    #    'species':'2',
    #    'organ':'A11',
    #    'disease':'No'
    #}
    #test_to_triplet={
    #    'species':'9606',
    #    'organ':'A11.436.081',
    #    'disease':'No'
    #}

    
    #test_from_triplet={
    #    'species':'9606',
    #    'organ':'Alveolar Epithelial Cells',
    #    'disease':'disease'
    #}
    #test_to_triplet={
    #    'species':'9606',
    #    'organ':'Epithelial Cells',
    #    'disease':'disease'
    #}
    
    test_from_triplet={
        'species':'9909',
        'organ':'A15.145.693',
        'disease':'No'
    }
    test_to_triplet={
        'species':'9685',
        'organ':'A15.145.693',
        'disease':'Disease'
    }    
    '''
    test_from_triplet={
        'species':'9909',
        'organ':'A15.145.693',
        'disease':'No'
    }
    test_to_triplet={
        'species':'9685',
        'organ':'A15.145.693',
        'disease':'No'
    } 
    '''
    test=(my_SingleResultCalculator.calculate_one_result(test_from_triplet,test_to_triplet))
    pprint(my_SingleResultCalculator.current_result)
    