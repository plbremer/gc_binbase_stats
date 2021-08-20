import networkx as nx
from collections import defaultdict
from pprint import pprint
import matplotlib.pyplot as plt

#__author__ = "Uli Koehler"
#__copyright__ = "Copyright 2015, Uli Kö221hler"
#__license__ = "CC0 1.0 Universal"
#__version__ = "1.0"

def readMeSH(fin):
    """
    Given a file-like object, generates MeSH objects, i.e.
    dictionaries with a list of values for each qualifier.
    Example: {"MH": ["Acetylcysteine"]}
    """
    currentEntry = None
    for line in fin:
        line = line.strip()
        if not line:
            continue
        # Handle new record. MeSH explicitly marks this
        if line == "*NEWRECORD":
            # Yiel old entry, initialize new one
            if currentEntry:
                yield currentEntry
            currentEntry = defaultdict(list)
            continue
        # Line example: "MH = Acetylcysteine"
        key, _, value = line.partition(" = ")
        # Append to value list
        currentEntry[key].append(value)
    # If there is a non-empty entry left, yield it
    if currentEntry:
        yield currentEntry

def add_nodepath_and_label_to_endnode_to_networkx(temp_nx,temp_mesh_entry):

    nodepath_string_path_list=temp_mesh_entry['MN']
    end_node_label=temp_mesh_entry['MH'][0]

    for temp_string_path in nodepath_string_path_list:
        node_path_elements=temp_string_path.split('.')
        #print(node_path_elements)
        node_paths=list()
        #for temp_element in node_path_elements:
        # #   node_paths.append
        #    for 
        #for i in range(0,len(node_path_elements)):
            #temp_path=''
            #for j in range(0,i):
            #    temp_path+=node_path_elements[j]+'.'
        #    node_paths.append('.'.join(node_paths[0:i]))
        #if len(node_path_elements)>1:
        for i in range(0,len(node_path_elements)):
            node_paths.append('.'.join(node_path_elements[0:i+1]))
        #elif len(node_path_elements)==1:
        #    node_paths.append(node_path_elements[0])
        #print(node_paths)
        #hold=input('hold')
        #print(end_node_label)
        #print(node_path)
        if 'A' in node_paths[0]:
            nx.add_path(temp_nx,node_paths)

            
            #temp_nx.nodes[temp_nx.nodes[node_path[-1]]]['mesh_label']=end_node_label[0]
            temp_nx.nodes[node_paths[-1]]['mesh_label']=end_node_label
            if(len(node_paths)==1):
                print(node_path_elements)
                print(node_paths)
                print(temp_nx.nodes[node_paths[-1]])
                print(end_node_label)
            #nx.draw(temp_nx,with_labels=True)
            #plt.show()
                hold=input('hold')




if __name__ == "__main__":
    
    #create organ networkx
    organ_networkx=nx.DiGraph()
    
    # Example of how to use readMeSH()
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    with open(args.file, "r") as infile:
        # readMeSH() yields MeSH objects, i.e. dictionaries
        for entry in readMeSH(infile):
            #pprint(entry)
            add_nodepath_and_label_to_endnode_to_networkx(organ_networkx,entry)
            #hold=input('hold')
        #nx.draw(organ_networkx,with_labels=True)
        #plt.show()

        
        #node_labels = {
        #    n: data.get('mesh_label', '') for n, data in organ_networkx.nodes(data=True)
        #}
        #nx.draw(organ_networkx,labels=node_labels)
        #plt.show()
        for i in ['A01','A02','A03']:
            #node_labels = {
            #    n: data.get('mesh_label', '') for n, data in organ_networkx.subgraph(nx.descendants(organ_networkx,i)).nodes(data=True)
            #}
            #nx.draw(organ_networkx.subgraph(nx.descendants(organ_networkx,i)),labels=node_labels)
            nx.draw(organ_networkx.subgraph(nx.descendants(organ_networkx,i)),with_labels=True)
            plt.show()