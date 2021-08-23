import networkx as nx
from pprint import pprint
import matplotlib.pyplot as plt
plt.switch_backend('agg')

class NodelistSelector():
    '''
    The purpose of this class to is choose a broad swath of nodes from the species, organ, disease trees based on 
    a given headnode for each or a set of levels for each (or some other method that has not yet been written)

    The "full list of nodes" is then given to Comparison request which filters out nonesense combinations that could never be legit
    for example (Human, leaf, lung cancer)
    '''
    def __init__(
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

        self.species_nx=temp_species_nx
        self.organ_nx=temp_organ_nx
        self.disease_nx=temp_disease_nx

        if species_topnode is not None:
            self.species_nodelist=nx.algorithms.dag.descendants(self.species_nx,species_topnode)
            self.species_nodelist.add(species_topnode)
            self.species_nodelist=list(self.species_nodelist)

        if organ_topnode is not None:
            self.organ_nodelist=nx.algorithms.dag.descendants(self.organ_nx,organ_topnode)
            self.organ_nodelist.add(organ_topnode)
            self.organ_nodelist=list(self.organ_nodelist)

        if disease_topnode is not None:
            self.disease_nodelist=nx.algorithms.dag.descendants(self.disease_nx,disease_topnode)
            self.disease_nodelist.add(disease_topnode)
            self.disease_nodelist=list(self.disease_nodelist)

        if (species_minlevel is not None) and (species_maxlevel is not None):
            self.set_nodelist_by_level('species',species_minlevel,species_maxlevel)
        if (organ_minlevel is not None) and (organ_maxlevel is not None):
            self.set_nodelist_by_level('organ',organ_minlevel,organ_maxlevel)
        if (disease_minlevel is not None) and (disease_maxlevel is not None):
            self.set_nodelist_by_level('disease',disease_minlevel,disease_maxlevel)            

    def set_nodelist_by_level(self,temp_type,temp_min,temp_max):
        '''
        An alternative method to check nodes. Note, may not work
        '''

        setattr(self,temp_type+'_nodelist',list())
        if temp_type=='species':
            temp_headnode='1'
        else:
            temp_headnode=temp_type

        shortest_path_node_dict=nx.algorithms.shortest_paths.generic.shortest_path(getattr(self,temp_type+'_nx'),source=temp_headnode)
        pprint(shortest_path_node_dict)
        shortest_path_length_dict={temp_key:len(shortest_path_node_dict[temp_key]) for temp_key in shortest_path_node_dict.keys()}
        pprint(shortest_path_length_dict)

        for temp_key in shortest_path_length_dict.keys():
            if (shortest_path_length_dict[temp_key]>temp_min) and (shortest_path_length_dict[temp_key]<temp_max):
                getattr(self,temp_type+'_nodelist').append(temp_key)

    def node_selection_visualizer(self,temp_type):
        '''
        A debugging tool.
        '''
        color_list=list()
        for temp_node in getattr(self,temp_type+'_nx'):
            if temp_node in getattr(self,temp_type+'_nodelist'):
                color_list.append('#00dd00')
            else:
                color_list.append('#0000dd')
        pos = nx.nx_agraph.pygraphviz_layout(getattr(self,temp_type+'_nx'), prog='dot')
        nx.draw(getattr(self,temp_type+'_nx'), pos,with_labels=True,node_color=color_list)
        plt.show()


'''
if __name__ == "__main__":

    species_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_11_prepare_species_networkx/species_networkx.bin'
    organ_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_12_prepare_organ_and_disease_networkx/organ_networkx.bin'
    disease_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_12_prepare_organ_and_disease_networkx/disease_networkx.bin'

    species_nx=nx.readwrite.gpickle.read_gpickle(species_networkx_address)
    organ_nx=nx.readwrite.gpickle.read_gpickle(organ_networkx_address)
    disease_nx=nx.readwrite.gpickle.read_gpickle(disease_networkx_address)



    my_NodelistSelector=NodelistSelector(
        species_nx,
        organ_nx,
        disease_nx,
        species_minlevel=3,
        species_maxlevel=10,
        #organ_topnode='organ',
        organ_minlevel=2,
        organ_maxlevel=4,
        disease_topnode='disease'     
    )


    print(my_NodelistSelector.species_nodelist)

    my_NodelistSelector.node_selection_visualizer('species')
    my_NodelistSelector.node_selection_visualizer('organ')
'''