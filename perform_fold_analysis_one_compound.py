import pandas
import networkx
import itertools

def visualize_traversal_of_tree(temp_nx,temp_node_location_A,temp_node_location_B):
    print('hello')
    total_color_list=list()
    for i,temp_node in enumerate(temp_nx.nodes):
        if temp_nx.nodes[temp_node]['interesting_combination']==True:
            total_color_list.append('#ffa500')
        elif temp_nx.nodes[temp_node]['interesting_combination']==False:
            if temp_nx.nodes[temp_node]['type_of_node']=='combination':
                total_color_list.append('#ff0000')
            elif temp_nx.nodes[temp_node]['type_of_node']=='from_binvestigate':
                total_color_list.append('#32cd32')

    #navy blue for every node
    total_color_list=['#0066cc' for i in range(0,len(temp_nx.nodes))]
    #change node A color to another color
    total_color_list[temp_nx.nodes.index(temp_node_location_A)]='#ff0000'
    #change node B to another color
    total_color_list[temp_nx.nodes.index(temp_node_location_A)]='#32cd32'

    nx.draw(temp_nx,with_labels=True,node_color=total_color_list)
    plt.show()

def traverse_species_trees(temp_grand_species_tree,temp_species_headnode,temp_grand_organ_tree_dict,temp_organ_headnode):
    species_depth_first_node_generator=nx.algorithms.traversal.depth_first_search.dfs_preorder_nodes(temp_grand_species_tree,temp_headnode)
    print('hello')

    species_depth_first_node_list=list(species_depth_first_node_generator)
    
    #for node_location_A in species_depth_first_node_list:
    for i in range(0,len(species_depth_first_node_list)):

        #check and act if we are in a "one parent/child branch"



        for j in range(i,len(species_depth_first_node_list)):
            if i == j:
                continue

            #check and act if we are in a "one parent/child branch"

            visualize_traversal_of_tree(temp_grand_species_tree,species_depth_first_node_list[i],species_depth_first_node_list[j])

            traverse_organ_trees(temp_grand_organ_tree,temp_organ_headnode,species_depth_first_node_list[i],species_depth_first_node_list[j])
    
def traverse_organ_trees(temp_grand_organ_tree_dict,temp_organ_headnode,temp_species_node_A,temp_species_node_B)

    organ_depth_first_node_generator_dict={
        temp_key:nx.algorithms.traversal.depth_first_search.dfs_preorder_nodes(temp_grand_organ_tree_dict[temp_key],temp_headnode)
        for temp_key in temp_grand_organ_tree_dict.get_keys
    }

    




if __name__ == "__main__":
    
    #read in fold matrix
    #fold_matrix_address=
    #probably have to flip hierarchical multiindex

    #read in grand species networkx
    grand_species_networkx_address=''

    #read in grand organ matrix non cancer


    #read in grand organ matrix cancer



    #calculate lower diagonal




