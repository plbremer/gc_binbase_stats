from nltk import edit_distance
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.datasets import load_iris
from sklearn.cluster import AgglomerativeClustering

def get_levenshtein_distance_matrix(string_list):
    distance_panda=pd.DataFrame(0, index=string_list,columns=string_list,dtype=float)
    print(distance_panda)

    for i in range(0, len(string_list)):
        print(i)
        for j in range(0,i):

            distance_panda.iloc[i,j]=edit_distance(string_list[i],string_list[j])
            #trick to fill upper half at the same time
            distance_panda.iloc[j,i]=distance_panda.iloc[i,j]

    print(distance_panda)

    return distance_panda

def isolate_all_unique_strings_in_column(temp_series):

    unique_string_set=set()

    for temp_string_list in temp_series:
        temp_string_set=set(temp_string_list)

        unique_string_set=unique_string_set.union(temp_string_set)
        #print(len(unique_string_set))
        #hold=input('hold')

    unique_string_list=list(unique_string_set)
    return unique_string_list

def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)

if __name__ == "__main__":
    '''
    starting_panda=pd.read_pickle('/home/rictuar/coding_projects_database/binvestigate_pickle.bin')
    unique_species_list=isolate_all_unique_strings_in_column(starting_panda['species'])
    for item in unique_species_list:
        print(item)
    hold=input('hold')
    species_distance_matrix=get_levenshtein_distance_matrix(unique_species_list)
    #species_distance_matrix=get_levenshtein_distance_matrix(unique_species_list[0:10])
    #render_dendogram
    species_AgglomerativeClustering=AgglomerativeClustering(
        n_clusters=None,affinity='precomputed',linkage='single',distance_threshold=5,compute_distances=True
    )
    species_AgglomerativeClustering.fit(species_distance_matrix)
    plot_dendrogram(species_AgglomerativeClustering,labels=unique_species_list)
    #plot_dendrogram(species_AgglomerativeClustering,labels=unique_species_list[0:10])
    plt.xticks(rotation=270)
    plt.tight_layout()
    plt.show()
    '''


    starting_panda=pd.read_pickle('/home/rictuar/coding_projects_database/binvestigate_pickle.bin')
    unique_organ_list=isolate_all_unique_strings_in_column(starting_panda['organ'])
    for item in unique_organ_list:
        print(item)
    hold=input('hold')
    organ_distance_matrix=get_levenshtein_distance_matrix(unique_organ_list)
    #organ_distance_matrix=get_levenshtein_distance_matrix(unique_organ_list[0:10])
    #render_dendogram
    organ_AgglomerativeClustering=AgglomerativeClustering(
        n_clusters=None,affinity='precomputed',linkage='average',distance_threshold=5,compute_distances=True
    )
    organ_AgglomerativeClustering.fit(organ_distance_matrix)
    plot_dendrogram(organ_AgglomerativeClustering,labels=unique_organ_list)
    #plot_dendrogram(organ_AgglomerativeClustering,labels=unique_organ_list[0:10])
    plt.xticks(rotation=270)
    plt.tight_layout()
    plt.show()




