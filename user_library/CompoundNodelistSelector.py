import networkx as nx
import matplotlib.pyplot as plt
#plt.switch_backend('agg')
from pprint import pprint
#import pydot
#from networkx.drawing.nx_pydot import graphviz_layout

class CompoundNodelistSelector:

    def __init__(self,temp_compound_nx,compound_topnode=None,compound_maxlevel=None,compound_minlevel=None):
        '''
        '''
        self.compound_nx=temp_compound_nx

        if compound_topnode is not None:
            #the ont reader or the ont itself is insane and the ancestor/descedant relationship is backwards
            #self.compound_nodelist=nx.algorithms.dag.ancestors(self.compound_nx,compound_topnode)
            self.compound_nodelist=nx.algorithms.dag.descendants(self.compound_nx,compound_topnode)
            self.compound_nodelist.add(compound_topnode)
            ##print(self.compound_nodelist)
            ##color_list=list()
            ##for temp_node in self.compound_nx.nodes:
            ##    if temp_node in self.compound_nodelist:
            ##        color_list.append('#00ff00')
            ##    else:
            ##        color_list.append('#ff0000')
            ##nx.draw(self.compound_nx,color)
            ##hold=input('compound_nodelist')

        if (compound_minlevel is not None) and (compound_maxlevel is not None):
            self.set_nodelist_by_level('compound',compound_minlevel,compound_maxlevel)


    def set_nodelist_by_level(self,temp_type,temp_min,temp_max):
        '''
        this code is borrowed from NodelistSelector  therefore it goes about things in a a seemingly roundabout fashion
        '''
        setattr(self,temp_type+'_nodelist',list())
        print(self.compound_nodelist)
        hold=input('self.compound_nodelist')

        if temp_type=='compound':
            temp_headnode='CHEMONTID:9999999'
        else:
            temp_headnode=temp_type

        shortest_path_node_dict=nx.algorithms.shortest_paths.generic.shortest_path(getattr(self,temp_type+'_nx'),source=temp_headnode)
        pprint(shortest_path_node_dict)
        shortest_path_length_dict={temp_key:len(shortest_path_node_dict[temp_key]) for temp_key in shortest_path_node_dict.keys()}
        pprint(shortest_path_length_dict)

        for temp_key in shortest_path_length_dict.keys():
            print(temp_key)
            if (shortest_path_length_dict[temp_key]>temp_min) and (shortest_path_length_dict[temp_key]<temp_max):
                print('met conditions')
                getattr(self,temp_type+'_nodelist').append(temp_key)
                print(getattr(self,temp_type+'_nodelist'))
            #hold=input('hold')

    def node_selection_visualizer(self,temp_type):
        '''
        '''
        print(self.compound_nx)
        print(self.compound_nodelist)
        color_list=list()
        for temp_node in getattr(self,temp_type+'_nx'):
            if temp_node in getattr(self,temp_type+'_nodelist'):
                color_list.append('#00dd00')
            elif temp_node =='CHEMONTID:9999999':
                color_list.append('#ff0000')
            else:
                color_list.append('#0000dd')
        
        #H = nx.convert_node_labels_to_integers(self.compound_nx, label_attribute='node_label')
        #H_layout = nx.nx_pydot.pydot_layout(self.compound_nx, prog='dot')
        #G_layout = {H.nodes[n]['node_label']: p for n, p in H_layout.items()}
        #nx.draw(getattr(self,temp_type+'_nx'), G_layout,with_labels=True,node_color=color_list)
        #pos = nx.drawing.nx_pydot.graphviz_layout(self.compound_nx, prog="twopi")
        #pos = nx.nx_agraph.pygraphviz_layout(getattr(self,temp_type+'_nx'), prog='dot')
        #pos = nx.nx_agraph.pygraphviz_layout(self.compound_nx, prog='dot')
        #nx.draw(getattr(self,temp_type+'_nx'), pos,with_labels=True,node_color=color_list)
        nx.draw(self.compound_nx,with_labels=True,node_color=color_list)
        #nx.draw(self.compound_nx,node_color=color_list)
        plt.show()

'''
if __name__ == "__main__":


    compound_nx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_7_prepare_compound_hierarchy/classyfire_ont_with_bins_added.bin'

    compound_nx=nx.readwrite.gpickle.read_gpickle(compound_nx_address)
    compound_nx=nx.DiGraph.reverse(compound_nx)
    print([n for n,d in compound_nx.in_degree() if d==0] )

    for temp_node in compound_nx.nodes:
        print(temp_node)
        try: 
            compound_nx.nodes[temp_node]['classyfire_name']=compound_nx.nodes[temp_node]['name']
            compound_nx.nodes[temp_node].pop('name',None)
        except KeyError:
            print('hi')

    print(compound_nx.nodes['CHEMONTID:9999999'])
    hold=input('hold')
    #my_CompoundNodelistSelector=CompoundNodelistSelector(compound_nx,compound_topnode='CHEMONTID:0001534')
    my_CompoundNodelistSelector=CompoundNodelistSelector(compound_nx,compound_maxlevel=5,compound_minlevel=3)

    #my_CompoundNodelistSelector.node_selection_visualizer('compound')
'''