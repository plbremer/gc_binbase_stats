import numpy as np
import pandas
import networkx as nx
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

def visualize_point(temp_nx,temp_label):
    print('hello')
    color_list=['#0000ff' for temp_node in temp_nx.nodes]
    color_list[list(temp_nx.nodes).index(temp_label)]='#00ff00'
    pos = nx.nx_agraph.pygraphviz_layout(temp_nx, prog='dot')
    nx.draw(temp_nx, pos,with_labels=True,node_color=color_list)
    plt.show()
    #plt.show(block=False) 
    #plt.pause(1)
    #plt.close()

def visualize_subgraph_via_individuals(temp_nx,temp_node_from,temp_node_to):
    #temp_organ_descendants=nx.algorithms.dag.descendants(temp_organ_view_from,temp_organ_location_from)
    if temp_node_to==None:
        #this is a set
        temp_visualization_descendants=nx.algorithms.dag.descendants(temp_nx,temp_node_from)
        temp_visualization_descendants.add(temp_node_from)
    elif temp_node_to!=None:
        temp_visualization_descendants_from=nx.algorithms.dag.descendants(temp_nx,temp_node_from)
        temp_visualization_descendants_from.add(temp_node_from)
        temp_visualization_descendants_to=nx.algorithms.dag.descendants(temp_nx,temp_node_to)
        temp_visualization_descendants_to.add(temp_node_to)
        temp_visualization_descendants=temp_visualization_descendants_from.difference(temp_visualization_descendants_to)
    #print('hello')
    #color_list=['#0000ff' for temp_node in temp_nx.nodes]
    #color_list[list(temp_nx.nodes).index(temp_label)]='#00ff00'
    color_list=list()
    for temp_node in temp_nx.nodes:
        if temp_node in temp_visualization_descendants:
            color_list.append('#00dd00')
        else:
            color_list.append('#0000dd')
    pos = nx.nx_agraph.pygraphviz_layout(temp_nx, prog='dot')
    nx.draw(temp_nx, pos,with_labels=True,node_color=color_list)
    plt.show()

def visualize_subgraph_via_nodelist(temp_nx,temp_subgraph):
    color_list=list()
    for temp_node in temp_nx.nodes:
        if temp_node in temp_subgraph.nodes:
            color_list.append('#00dd00')
        else:
            color_list.append('#0000dd')
    pos = nx.nx_agraph.pygraphviz_layout(temp_nx, prog='dot')
    nx.draw(temp_nx, pos,with_labels=True,node_color=color_list)
    plt.show()

def create_disease_relevant_list(temp_disease_location_from,temp_disease_location_to,temp_all_species_list_from,temp_all_species_list_to,temp_all_organ_list_from,temp_all_organ_list_to,temp_disease_view_from,temp_disease_view_to):
    print('INSIDE OF create_disease_relevant_list')

    #            location_disease_from,location_disease_to,
    #            temp_all_species_list_from,temp_all_species_list_to,
    #            temp_all_organ_list_from,temp_all_organ_list_to,
    #            disease_subgraph_view_from,disease_subgraph_view_to


    if temp_disease_location_to==None:
        print('this is a from call')
        temp_disease_descendants=nx.algorithms.dag.descendants(temp_disease_view_from,temp_disease_location_from)
        #descendants never include self (super annoyingly)
        #add manually

        temp_disease_descendants.add(temp_disease_view_from.nodes[temp_disease_location_from]['mesh_label'])
        print(temp_disease_descendants)
        #print(temp_species_location_from)
        hold=input('temp_disease_descendants from')
        #we make the list in the if statement because 
        #relevant_disease_list=total_triplet_panda.loc[
        #    total_triplet_panda['species'].astype(str).isin(temp_all_species_list_from) & total_triplet_panda['organ'].isin(temp_organ_descendants)
        #]['disease'].to_list()
    
    elif temp_disease_location_to!=None:
        print('this is a to call')
        #check if we have only one disease, in which case we can just add "self" in a way
        if temp_disease_location_from==temp_disease_location_to:
            print('temp_disease_location_from==temp_disease_location_to')
            temp_disease_descendants=set()
            temp_disease_descendants.add(temp_disease_location_from)
            print(temp_disease_descendants)
            hold=input('temp_organ_descendants to')
        else:
            #the basic idea is that the list of diseases is to-from
            print('we are going from ' +temp_disease_location_from+' to '+temp_disease_location_to)
            temp_disease_descendants_to=nx.algorithms.dag.descendants(temp_disease_view_to,temp_disease_location_to)
            
            #print()
            temp_disease_descendants_to.add(temp_disease_location_to)
            print(temp_disease_descendants_to)
            temp_disease_descendants_from=nx.algorithms.dag.descendants(temp_disease_view_from,temp_disease_location_from)
            temp_disease_descendants_from.add(temp_disease_location_from)
            print(temp_disease_descendants_from)
            temp_disease_descendants=temp_disease_descendants_to.difference(temp_disease_descendants_from)
            print(temp_disease_descendants)
            #print(temp_species_location_from+' '+temp_species_descendants_to)
            hold=input('temp_disease_descendants to after subtracting from')  
            #relevant_disease_list=total_triplet_panda.loc[
            #    #to takes care of the subtraction of species as it is defined as the difference when it is created
            #    total_triplet_panda['species'].astype(str).isin(temp_all_species_list_to) & total_triplet_panda['organ'].isin(temp_organ_descendants)
            #]['disease'].to_list()      
    
    return temp_disease_descendants  

def create_view_of_disease_nx(temp_organ_location_from,temp_organ_location_to,temp_all_species_list_from,temp_all_species_list_to,temp_organ_view_from,temp_organ_view_to):
    print('INSIDE OF create_view_of_disease_nx')

    if temp_organ_location_to==None:
        temp_organ_descendants=nx.algorithms.dag.descendants(temp_organ_view_from,temp_organ_location_from)
        #descendants never include self (super annoyingly)
        #add manually
        #SUSPICIOUS LINE
        temp_organ_descendants.add(temp_organ_view_from.nodes[temp_organ_location_from]['mesh_label'])
        print(temp_organ_descendants)
        #print(temp_species_location_from)
        hold=input('temp_organ_descendants from')
        #we make the list in the if statement because 
        relevant_disease_list=total_triplet_panda.loc[
            total_triplet_panda['species'].astype(str).isin(temp_all_species_list_from) & total_triplet_panda['organ'].isin(temp_organ_descendants)
        ]['disease'].to_list()
    
    elif temp_organ_location_to!=None:
        if temp_organ_location_from==temp_organ_location_to:
            temp_organ_descendants=set()
            temp_organ_descendants.add(temp_organ_view_from.nodes[temp_organ_location_from]['mesh_label'])
            print(temp_organ_descendants)
            print(total_triplet_panda['species'].astype(str).isin(temp_all_species_list_to).value_counts())
            print(total_triplet_panda['organ'].isin(temp_organ_descendants).value_counts())
            hold=input('temp_organ_descendants to')
            relevant_disease_list=total_triplet_panda.loc[
                #to takes care of the subtraction of species as it is defined as the difference when it is created

                total_triplet_panda['species'].astype(str).isin(temp_all_species_list_to) & total_triplet_panda['organ'].isin(temp_organ_descendants)
            ]['disease'].to_list() 
        else:
            print(temp_organ_location_from+' '+temp_organ_location_to)
            temp_organ_descendants_to=nx.algorithms.dag.descendants(temp_organ_view_to,temp_organ_location_to)
            
            #print()
            temp_organ_descendants_to.add(temp_organ_location_to)
            print(temp_organ_descendants_to)
            temp_organ_descendants_from=nx.algorithms.dag.descendants(temp_organ_view_from,temp_organ_location_from)
            temp_organ_descendants_from.add(temp_organ_location_from)
            print(temp_organ_descendants_from)
            temp_organ_descendants=temp_organ_descendants_to.difference(temp_organ_descendants_from)
            print(temp_organ_descendants)
            #print(temp_species_location_from+' '+temp_species_descendants_to)
            hold=input('temp_organ_descendants to')  
            relevant_disease_list=total_triplet_panda.loc[
                #to takes care of the subtraction of species as it is defined as the difference when it is created
                total_triplet_panda['species'].astype(str).isin(temp_all_species_list_to) & total_triplet_panda['organ'].isin(temp_organ_descendants)
            ]['disease'].to_list()      
    
    
    

    #print(total_triplet_panda.loc[total_triplet_panda['species']])
    
    
    #print(temp_all_species_list_from)
    #print(temp_organ_descendants)
    #print(total_triplet_panda['species'].astype(str).isin(temp_all_species_list_from).value_counts())
    #print(total_triplet_panda['organ'].isin(temp_organ_descendants).value_counts())
    
    print(relevant_disease_list)
    hold=input('relevant disease list')
    
    disease_node_subset_list=[temp_node for temp_node in disease_nx.nodes if (disease_nx.nodes[temp_node]['mesh_label'] in relevant_disease_list)]
    
    print(disease_node_subset_list)
    hold=input('organ_node_subset_list')
    ## the node names represent the node paths)
    #create a view of the graph based on the node set
    ##for each node, add the set of ancestors to a collective set as well as the element itself
    total_disease_subgraph_node_set=set()
    for temp_node in disease_node_subset_list:
        #total_subgraph_node_set.add(
        #    nx.algorithms.shortest_paths.generic.shortest_path(
        #        organ_nx, source='organ',target=temp_node
        #    )
        #)
        temp_path=set(nx.algorithms.shortest_paths.generic.shortest_path(
                disease_nx, source='disease',target=temp_node
            ))
        print(temp_path)
        total_disease_subgraph_node_set.update(temp_path)
        hold=input('single node path for disease')
    #create the subgraph view based on relevant nodes
    disease_subgraph_view=disease_nx.subgraph(total_disease_subgraph_node_set)


    #temp species descendants is the list of species that are relevant based on the from/to position in the
    #species graph
    #if we have a from call, then the descedants is "from" and is every species in the subgraph
    #if we have a to call, then th descendants if to minus from
    return disease_subgraph_view,temp_organ_descendants
    ##finally return the set    

def create_view_of_organ_nx(temp_species_location_from,temp_species_location_to):
    #take species location
    #get entire descendant set from species_nx
    #nx.draw(species_nx)
    #plt.show()
    if temp_species_location_to==None:
        temp_species_descendants=nx.algorithms.dag.descendants(species_nx,temp_species_location_from)
        #descendants never include self (super annoyingly)
        #add manually
        temp_species_descendants.add(temp_species_location_from)
        print(temp_species_descendants)
        print(temp_species_location_from)
        hold=input('temp_species_descendants from')
    elif temp_species_location_to!=None:
        #if we have the same species from and to then we 
        if temp_species_location_from==temp_species_location_to:
            temp_species_descendants=set()
            temp_species_descendants.add(temp_species_location_from)
            print(temp_species_descendants)
            hold=input('temp_species_descendants to')
        else:
            print(temp_species_location_from+' '+temp_species_location_to)
            temp_species_descendants_to=nx.algorithms.dag.descendants(species_nx,temp_species_location_to)
            
            #print()
            temp_species_descendants_to.add(temp_species_location_to)
            print(temp_species_descendants_to)
            temp_species_descendants_from=nx.algorithms.dag.descendants(species_nx,temp_species_location_from)
            temp_species_descendants_from.add(temp_species_location_from)
            print(temp_species_descendants_from)
            temp_species_descendants=temp_species_descendants_to.difference(temp_species_descendants_from)
            print(temp_species_descendants)
            #print(temp_species_location_from+' '+temp_species_descendants_to)
            hold=input('temp_species_descendants to')        
    
    
    
    
    
    #filter entire triplet set based on species, producing a subset of organs that are relevant
    #done as a view of a panda
    #print(total_triplet_panda.loc[total_triplet_panda['species'].astype(str).isin(temp_species_descendants)]['organ'].to_list())
    #hold=input('hold')
    #print(total_triplet_panda.loc[total_triplet_panda['species'].astype(str).isin(temp_species_descendants)]['organ'].values)
    relevant_organs_list=total_triplet_panda.loc[total_triplet_panda['species'].astype(str).isin(temp_species_descendants)]['organ'].to_list()
    #print(total_triplet_panda.loc[total_triplet_panda['species']])
    print(relevant_organs_list)
    hold=input('relevant organs list')
    #from that set of organs, create a set of nodes (an organ can have multiple node names because
    organ_node_subset_list=[temp_node for temp_node in organ_nx.nodes if (organ_nx.nodes[temp_node]['mesh_label'] in relevant_organs_list)]
    print(organ_node_subset_list)
    hold=input('organ_node_subset_list')
    ## the node names represent the node paths)
    #create a view of the graph based on the node set
    ##for each node, add the set of ancestors to a collective set as well as the element itself
    total_subgraph_node_set=set()
    for temp_node in organ_node_subset_list:
        #total_subgraph_node_set.add(
        #    nx.algorithms.shortest_paths.generic.shortest_path(
        #        organ_nx, source='organ',target=temp_node
        #    )
        #)
        temp_path=set(nx.algorithms.shortest_paths.generic.shortest_path(
                organ_nx, source='organ',target=temp_node
            ))
        print(temp_path)
        total_subgraph_node_set.update(temp_path)
        hold=input('single node path')
    #create the subgraph view based on relevant nodes
    organ_subgraph_view=organ_nx.subgraph(total_subgraph_node_set)


    #temp species descendants is the list of species that are relevant based on the from/to position in the
    #species graph
    #if we have a from call, then the descedants is "from" and is every species in the subgraph
    #if we have a to call, then th descendants if to minus from
    return organ_subgraph_view,temp_species_descendants
    ##finally return the set

def do_disease_analysis(disease_nx_view_from,disease_nx_view_to,temp_all_species_list_from,temp_all_species_list_to,temp_all_organ_list_from,temp_all_organ_list_to):
    disease_dfpo_traversal_list_from=list(nx.algorithms.traversal.depth_first_search.dfs_postorder_nodes(disease_nx_view_from,source='disease'))
    print(disease_dfpo_traversal_list_from)
    hold=input('disease_dfpo_traversal_list_from')
    disease_dfpo_traversal_list_to=list(nx.algorithms.traversal.depth_first_search.dfs_postorder_nodes(disease_nx_view_to,source='disease'))
    print(disease_dfpo_traversal_list_to)
    hold=input('disease_dfpo_traversal_list_to')

    list_of_skippable_ancestors_disease_from=list()
    
    
    for location_disease_from in disease_dfpo_traversal_list_from:
        #if it was determined that the descendants of this node had no results, then this node cant have results
        if location_disease_from in list_of_skippable_ancestors_disease_from:
            print('we see that location_species_from '+location_species_from)
            print('is in list_of_skippable_ancestors_species_from')
            print(list_of_skippable_ancesfromrs_species_from)
            hold=input('so we are continuing')
            continue

        found_a_result_disease_from=False

        print('VISUALIZE DISEASE FROM')
        visualize_point(disease_nx_view_from,location_disease_from)
    
        #we only want to make the disease subview once, so we do it within the organ from for lop
        
        
        all_disease_list_from=create_disease_relevant_list(
            location_disease_from,None,
            temp_all_species_list_from,None,
            temp_all_organ_list_from,None,
            disease_nx_view_from,None
        )
        

        #the only time that we could benefit from the symmetry is when speciesfrom==speciesto
        #thsi is a special case that happens only "down the diagonal"
        #and honestly i dont care to program that microscopic efficieny in
        #however, the disease view MUST think about where .......................
        list_of_skippable_ancestors_disease_to=list()
    
        for location_disease_to in disease_dfpo_traversal_list_to:
            #if it was determined that the descendants of this node had no results, then this node cant have results
            if location_disease_to in list_of_skippable_ancestors_disease_to:
                print('we see that location_disease_to '+location_disease_to)
                print('is in list_of_skippable_ancestors_disease_to')
                print(list_of_skippable_ancestors_disease_to)
                hold=input('so we are continuing')
                continue
    
            visualize_point(disease_nx_view_to,location_disease_to)
            #we want tnice symmetry, so we put the organ subgraph view to within the spcies method
            all_disease_list_to=create_disease_relevant_list(
                location_disease_from,location_disease_to,
                temp_all_species_list_from,temp_all_species_list_to,
                temp_all_organ_list_from,temp_all_organ_list_to,
                disease_nx_view_from,disease_nx_view_to
            )
            
            #if we did not find a result for all the possible organs, then we know that there is no 
            #result for the ancestors of this species as we head toward
            #the organ analysis requires the total set of "species entries" so that we can produce a view
            #of the organ matrix and do a lot less looping
            

            print(temp_all_species_list_from)
            print(temp_all_species_list_to)
            print(temp_all_organ_list_from)
            print(temp_all_organ_list_to)
            print(all_disease_list_from)
            print(all_disease_list_to)

            hold=input('about to do one slice comparison')
            

            nan_result=perform_single_assesment(
                temp_all_species_list_from,
                temp_all_species_list_to,
                temp_all_organ_list_from,
                temp_all_organ_list_to,
                all_disease_list_from,
                all_disease_list_to                
            )
            ####
            #make sure that result is np.nan doesnt fail because of stupid np.nan equality rules
            ####
            if nan_result:
                print('found a nan result, adding')
                print(nx.algorithms.dag.ancestors(disease_nx_view_to,location_disease_to))
                print('to')
                print(list_of_skippable_ancestors_disease_to)
                list_of_skippable_ancestors_disease_to+=list(nx.algorithms.dag.ancestors(disease_nx_view_to,location_disease_to))
                print(list_of_skippable_ancestors_disease_to)
                hold=input('added')
            elif nan_result==False:
                found_a_result_disease_from=True
                hold=input('result of one perform_single_assesment was that nan_result==False')
            

            hold=input('holding at the end of disease to')
        #
        if found_a_result_disease_from==False:
            list_of_skippable_ancestors_disease_from+=list(nx.algorithms.dag.ancestors(disease_nx_view_from,location_disease_from))

        print('we found that the overall result of found_a_result_disease_from is '+str(found_a_result_disease_from))
        hold=input('holding at the end of disease from')
        return found_a_result_disease_from

def do_organ_analysis(organ_nx_view_from,organ_nx_view_to,temp_all_species_list_from,temp_all_species_list_to):

    organ_dfpo_traversal_list_from=list(nx.algorithms.traversal.depth_first_search.dfs_postorder_nodes(organ_nx_view_from,source='organ'))
    print(organ_dfpo_traversal_list_from)
    hold=input('organ_dfpo_traversal_list_from')
    organ_dfpo_traversal_list_to=list(nx.algorithms.traversal.depth_first_search.dfs_postorder_nodes(organ_nx_view_to,source='organ'))
    print(organ_dfpo_traversal_list_to)
    hold=input('organ_dfpo_traversal_list_to')

    list_of_skippable_ancestors_organ_from=list()
    

    for location_organ_from in organ_dfpo_traversal_list_from:
        #if it was determined that the descendants of this node had no results, then this node cant have results
        if location_organ_from in list_of_skippable_ancestors_organ_from:
            print('we see that location_organ_from '+location_organ_from)
            print('is in list_of_skippable_ancestors_organ_from')
            print(list_of_skippable_ancestors_organ_from)
            hold=input('so we are continuing')
            continue

        visualize_point(organ_nx_view_from,location_organ_from)
        
        found_a_result_organ_from=False

    
        #we only want to make the disease subview once, so we do it within the organ from for lop
        
        disease_subgraph_view_from,all_organ_list_from=create_view_of_disease_nx(
            location_organ_from,None,
            temp_all_species_list_from,None,
            organ_nx_view_from,None
        )
        
        #the only time that we could benefit from the symmetry is when speciesfrom==speciesto
        #thsi is a special case that happens only "down the diagonal"
        #and honestly i dont care to program that microscopic efficieny in
        #however, the disease view MUST think about where .......................
        list_of_skippable_ancestors_organ_to=list()
        for location_organ_to in organ_dfpo_traversal_list_to:
            #if it was determined that the descendants of this node had no results, then this node cant have results
            if location_organ_to in list_of_skippable_ancestors_organ_to:
                print('we see that location_organ_to '+location_organ_to)
                print('is in list_of_skippable_ancestors_organ_to')
                print(list_of_skippable_ancestors_organ_to)
                hold=input('so we are continuing')
                continue
    
            visualize_point(organ_nx_view_to,location_organ_to)
            #we want tnice symmetry, so we put the organ subgraph view to within the spcies method
            
            disease_subgraph_view_to,all_organ_list_to=create_view_of_disease_nx(
                location_organ_from,location_organ_to,temp_all_species_list_from,temp_all_species_list_to,organ_nx_view_from,organ_nx_view_to
            )
            
            #if we did not find a result for all the possible organs, then we know that there is no 
            #result for the ancestors of this species as we head toward
            #the organ analysis requires the total set of "species entries" so that we can produce a view
            #of the organ matrix and do a lot less looping
            
            found_a_result_organ_to=do_disease_analysis(
                disease_subgraph_view_from,disease_subgraph_view_to,
                temp_all_species_list_from,temp_all_species_list_to,
                all_organ_list_from,all_organ_list_to
            )
            
            #
            



            if not found_a_result_organ_to:
                list_of_skippable_ancestors_organ_to+=list(nx.algorithms.dag.ancestors(organ_nx_view_to,location_organ_to))
            elif found_a_result_organ_to:
                found_a_result_organ_from=True
            

            hold=input('holding at the end of organ to')
        if found_a_result_organ_from==False:
            list_of_skippable_ancestors_organ_from+=list(nx.algorithms.dag.ancestors(organ_nx_view_from,location_organ_from))

        hold=input('holding at the end of organ from')
        #found_a_result_organ_from tell species if we found a result at all 
        return found_a_result_organ_from

def do_species_analysis():

    #for species, we traverse the entire list for from AND to, because both are guaranteed to have entries
    #at every species node
    #however, we do custom traversals for organs and diseases because we usually usually have different positions
    #on the speices trees and therefore different organ tree views (subgraphs)
    species_dfpo_traversal_list=list(nx.algorithms.traversal.depth_first_search.dfs_postorder_nodes(species_nx,source='1'))
    print('species_dfpo_traversal_list')
    print(species_dfpo_traversal_list)
    #print(len(species_dfpo_traversal_list))

    list_of_skippable_ancestors_species_from=list()
    
    #traverse the entire species from list
    for location_species_from in species_dfpo_traversal_list:
        #if it was determined that the descendants of this node had no results, then this node cant have results
        if location_species_from in list_of_skippable_ancestors_species_from:
            print('we see that location_species_from '+location_species_from)
            print('is in list_of_skippable_ancestors_species_from')
            print(list_of_skippable_ancestors_species_from)
            hold=input('so we are continuing')
            continue

        #
        #visualize_point(species_nx,location_species_from)
        #what i really want to do is visualize the subgraph superimposed on the entire species nx
        visualize_subgraph_via_individuals(species_nx,location_species_from,None)

        found_a_result_species_from=False

        
        #we only want to make the organ subview once, so we do it within the species from for lop
        organ_subgraph_view_from,all_species_list_from=create_view_of_organ_nx(location_species_from,None)
        visualize_subgraph_via_nodelist(organ_nx,organ_subgraph_view_from)
        print(all_species_list_from)
        hold=input('all species found in the organ subgraph from')
        
        #we get a new skip list ever from iteration
        list_of_skippable_ancestors_species_to=list()
        #start at same as current node as we can do things like "human lungs" vs "human liver"
        for location_species_to in species_dfpo_traversal_list[species_dfpo_traversal_list.index(location_species_from):]:
            #if it was determined that the descendants of this node had no results, then this node cant have results
            if location_species_to in list_of_skippable_ancestors_species_to:
                print('we see that location_species_to '+location_species_to)
                print('is in list_of_skippable_ancestors_species_to')
                print(list_of_skippable_ancestors_species_to)
                hold=input('so we are continuing')
                continue
                

            
            visualize_point(species_nx,location_species_to)

            #we want tnice symmetry, so we put the organ subgraph view to within the spcies method
            organ_subgraph_view_to,all_species_list_to=create_view_of_organ_nx(location_species_from,location_species_to)
            
            #if we did not find a result for all the possible organs, then we know that there is no 
            #result for the ancestors of this species as we head toward
            #the organ analysis requires the total set of "species entries" so that we can produce a view
            #of the organ matrix and do a lot less looping
            found_a_result_species_to=do_organ_analysis(organ_subgraph_view_from,organ_subgraph_view_to,all_species_list_from,all_species_list_to)
            

            
            

            if not found_a_result_species_to:
                list_of_skippable_ancestors_species_to+=list(nx.algorithms.dag.ancestors(species_nx,location_species_to))
            elif found_a_result_species_to:
                found_a_result_species_from=True
            

            hold=input('holding at the end of species to')

        #if, after going through every species_to, finding a result is still false, then we can add the 
        #ancestors to the list that species_from can skip
        if not found_a_result_species_from:
            list_of_skippable_ancestors_species_from+=list(nx.algorithms.dag.ancestors(species_nx,location_species_from))

        hold=input('holding at the end of species from')

def perform_single_assesment(temp_species_from,temp_species_to,temp_organ_from,temp_organ_to,temp_disease_from,temp_disease_to):
    #        nan_result=found_a_result_organ_to=perform_single_assesment(
    #            temp_all_species_list_from,
    #            temp_all_species_list_to,
    #            all_organ_list_from,
    #            all_organ_list_to,
    #            all_disease_list_from,
    #            all_disease_list_to                

    #species_filter_view=fold_matrix.loc[]

    fold_matrix_species_view=fold_matrix.loc[
        fold_matrix.index.isin(temp_species_from,level='species'),
        fold_matrix.columns.isin(temp_species_to,level='species')
    ]
    print(fold_matrix_species_view)
    hold=input('view of species')

    fold_matrix_organ_view=fold_matrix_species_view.loc[
        fold_matrix_species_view.index.isin(temp_organ_from,level='organ'),
        fold_matrix_species_view.columns.isin(temp_organ_to,level='organ')        
    ]
    print(fold_matrix_organ_view)
    hold=input('view of species then organ')
    fold_matrix_disease_view=fold_matrix_organ_view.loc[
        fold_matrix_organ_view.index.isin(temp_disease_from,level='disease'),
        fold_matrix_organ_view.columns.isin(temp_disease_to,level='disease')    
    ].values

    print(fold_matrix_disease_view)
    hold=input('iew of species then organ then disease turned values')

    conditions=[
        any(np.isnan(fold_matrix_disease_view)),
        all(fold_matrix_disease_view==np.inf),
        all(fold_matrix_disease_view==-np.inf),
        any(fold_matrix_disease_view<0) and any(fold_matrix_disease_view>0),
        any(fold_matrix_disease_view==0),
        all(fold_matrix_disease_view>=1),
        all(fold_matrix_disease_view<=-1)
    ]

    choices=[
        np.nan,
        np.inf,
        -np.inf,
        np.nan,
        np.nan,
        min(fold_matrix_disease_view),
        max(fold_matrix_disease_view)
    ]
    result=np.select(conditions,choices)
    print(result)
    hold=input('one calculated result')

    ####
    #here is where we will add to our results dictionary
    ###
    if np.isnan(result):
        return True
    else:
        return False
    #return np.select(conditions,choices)

if __name__ == "__main__":

    one_compound_fold_matrix_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_8_perform_compound_hierarchical_analysis/each_compounds_fold_matrix/all_fold_matrices/2.bin'

    species_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_11_prepare_species_networkx/species_networkx.bin'
    organ_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_12_prepare_organ_and_disease_networkx/organ_networkx.bin'
    disease_networkx_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/10/step_12_prepare_organ_and_disease_networkx/disease_networkx.bin'

    fold_matrix=pandas.read_pickle(one_compound_fold_matrix_address)
    species_nx=nx.readwrite.gpickle.read_gpickle(species_networkx_address)
    organ_nx=nx.readwrite.gpickle.read_gpickle(organ_networkx_address)
    disease_nx=nx.readwrite.gpickle.read_gpickle(disease_networkx_address)

    total_triplet_panda=pandas.DataFrame(fold_matrix.index.values)
    total_triplet_panda=total_triplet_panda[0].apply(pandas.Series)
    total_triplet_panda.columns=['organ','species','disease']
    print(total_triplet_panda)
    print(fold_matrix)
    hold=input('hold')

    #nx.draw(species_nx)
    #plt.show()

    do_species_analysis()
