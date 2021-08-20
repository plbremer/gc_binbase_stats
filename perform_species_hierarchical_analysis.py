import networkx as nx
import matplotlib.pyplot as plt

if __name__=="__main__":


    species_taxid_mapping_panda_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/species_organ_maps/species_tax_id.bin'

    binvestigate_taxonomy_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/intermediate_step_transforms/binvestigate_species_networkx.bin'

    binvestigate_taxonomy_networkx=nx.readwrite.gpickle.read_gpickle(binvestigate_taxonomy_address)

    species_taxid_panda=pandas.read_pickle(species_taxid_mapping_panda_address)
    binvestigate_taxid_list=species_taxid_panda['tax_id'].astype('str').to_list()


    #print(binvestigate_taxonomy_networkx.nodes)
    #print(binvestigate_taxonomy_networkx.nodes['12908'])

    for temp_node in binvestigate_taxonomy_networkx.nodes:
        #print(temp_node+' '+binvestigate_species_networkx.nodes[temp_node]['scientific_name']+' '+binvestigate_species_networkx.nodes[temp_node]['rank'])
        print(binvestigate_taxonomy_networkx.nodes[temp_node])

    for temp_node in binvestigate_taxonomy_networkx.nodes:


    nx.draw(binvestigate_taxonomy_networkx,with_labels=True)
    plt.show()