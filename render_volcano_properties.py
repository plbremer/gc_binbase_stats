from unittest import result
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as ticker




def convert_fold_to_log_fold(temp_fold):
    '''
    custom conversion to the typical log fold change from ours
    '''
    
    if temp_fold>0:
        return np.log2(temp_fold)
    elif temp_fold<0:
        return np.log2(abs(1/temp_fold))

def coerce_our_structure_to_plotly_volcano(temp_fold_panda,temp_signifigance_panda,temp_metabolite):
    #the desired structure is a pandas dataframe
    #
    #reshape dataframe to be column of values, with "gene" as the metabolite name
    #and from/to tuples as the snp?
    #this removes the diagonal, somehwere

    #i know this because for the 36*36 species, it returns 1260, which is 36*36-36 (the square matrix minus the diagonal)
    temp_fold_panda=temp_fold_panda.stack().stack().stack()
    temp_fold_panda.index.rename(['organ_from','species_from','disease_from','disease_to','species_to','organ_to'],inplace=True)
    temp_fold_panda=temp_fold_panda.reset_index()
    temp_fold_panda['from']=temp_fold_panda[['organ_from','species_from','disease_from']].apply(tuple,axis='columns')
    temp_fold_panda['to']=temp_fold_panda[['organ_to','species_to','disease_to']].apply(tuple,axis='columns')
    temp_fold_panda=temp_fold_panda.drop(['organ_from', 'species_from', 'disease_from','disease_to','species_to','organ_to'],axis='columns')
    temp_fold_panda.rename({0:'fold'},axis='columns',inplace=True)
    temp_signifigance_panda=temp_signifigance_panda.stack().stack().stack()
    temp_signifigance_panda.index.rename(['organ_from','species_from','disease_from','disease_to','species_to','organ_to'],inplace=True)
    temp_signifigance_panda=temp_signifigance_panda.reset_index()
    temp_signifigance_panda['from']=temp_signifigance_panda[['organ_from','species_from','disease_from']].apply(tuple,axis='columns')
    temp_signifigance_panda['to']=temp_signifigance_panda[['organ_to','species_to','disease_to']].apply(tuple,axis='columns')
    temp_signifigance_panda=temp_signifigance_panda.drop(['organ_from', 'species_from', 'disease_from','disease_to','species_to','organ_to'],axis='columns')
    temp_signifigance_panda.rename({0:'signifigance'},axis='columns',inplace=True)
    
    #2-18-22 plb
    ##we used to conver this, but now we are putting this conversion in the original pipeline
    ##temp_fold_panda['fold']=temp_fold_panda['fold'].apply(convert_fold_to_log_fold)
    #temp_fold_panda['fold']=temp_fold_panda['fold'].apply(convert_fold_to_log_fold)
    temp_fold_panda['signifigance']=temp_signifigance_panda['signifigance']
    #snap from dash plotly docs. idk what it is. something genomics.
    temp_fold_panda['snap']='from: '+temp_fold_panda['from'].astype(str)+' to: '+temp_fold_panda['to'].astype(str)
    temp_fold_panda.drop(['from','to'],inplace=True,axis='columns')
    temp_fold_panda['metabolite']=temp_metabolite
    return temp_fold_panda




if __name__=="__main__":
    #basic usage instructions
    #we hijacked this code from the volcano plot render code

    #we will go through every single bin,calculate the amount in each zone, add it to a list

    fold_type='fold_change_total_intensity'
    signifigance_type='signifigance_welch'
    fold_cutoff=2
    signifigance_cutoff=0.01
    
    #this is different from fold cutoff
    #it is here in case we integrate into snakemake
    min_fold_change=0
    #input_panda_address='../results/'+str(min_fold_change)+'/step_6_b_generate_signifigance_test_matrices/binvestigate_with_signifigance_matrices.bin'
    input_panda_address='../../results/'+str(min_fold_change)+'/step_6_b_generate_signifigance_test_matrices/binvestigate_with_signifigance_matrices.bin'

    full_data_panda=pd.read_pickle(input_panda_address)
    print(full_data_panda.columns)
    yes_signifigance_yes_fold=list()
    yes_signifigance_no_fold=list()
    no_signifigance_no_fold=list()
    no_signifigance_yes_fold=list()

    ##signifigance_and_fold_enough=list()
    ##either_signifigance_or_fold_not_enough=list()
    #fold_list_enough=list()
    #fold_list_not_enough=list()
    metabolite_list=list()


    total_x_position_list=list()
    total_y_position_list=list()

    for index,series in full_data_panda.iterrows():
        print(index)
        fold_panda=full_data_panda.at[index,fold_type]
        signifigance_panda=full_data_panda.at[index,signifigance_type]
        metabolite=full_data_panda.at[index,'name']
        result_panda=coerce_our_structure_to_plotly_volcano(fold_panda,signifigance_panda,metabolite)

        #since the volcano plot is symmetric, keep only 1 half
        result_panda=result_panda.loc[result_panda['fold']>0]
        #coerce the "zero" p values to the min for that
        #seems like the code already does that earlier in the pipelein
        #result_panda['signifigance']=result_panda['signifigance'].where(cond=result_panda['signifigance']>0,other=result_panda['signifigance'].min())

        #print(result_panda)
        #hold=input('hold')
        yes_signifigance_yes_fold.append(
            len(result_panda.loc[
                (result_panda.signifigance < signifigance_cutoff) &
                (result_panda.fold > fold_cutoff)
            ].index)
        )
        yes_signifigance_no_fold.append(
            len(result_panda.loc[
                (result_panda.signifigance < signifigance_cutoff) &
                (result_panda.fold < fold_cutoff)
            ].index)
        )
        no_signifigance_yes_fold.append(
            len(result_panda.loc[
                (result_panda.signifigance > signifigance_cutoff) &
                (result_panda.fold > fold_cutoff)
            ].index)
        )
        no_signifigance_no_fold.append(
            len(result_panda.loc[
                (result_panda.signifigance > signifigance_cutoff) &
                (result_panda.fold < fold_cutoff)
            ].index)
        )
        metabolite_list.append(metabolite)

        if index==0:
            total_panda=result_panda[['fold','signifigance']].copy(deep=True)
        elif index!=0:
            print('here')
            total_panda=total_panda.append(result_panda[['fold','signifigance']])
        #print(total_panda.append(result_panda[['fold','signifigance']]))
        #print(total_panda)
        # total_x_position_list=total_x_position_list+(
        #     result_panda.loc[(result_panda['fold']>0)]['fold'].to_list()
        # )
        # total_y_position_list=total_y_position_list+(
        #    result_panda.loc[(result_panda['fold']>0)]['signifigance'].to_list()
        # )
        #  --------------------------------------------------------------------------------  #





        #total_y_position_list=[-1*np.log10(x) for x in total_y_position_list]



        # print(total_y_position_list)
        # sns.heatmap(
        #     np.array([total_y_position_list,total_x_position_list])
        # )
        # plt.show()

        # sns.heatmap(

        # )
    #total_y_position_list=[np.log10(x) for x in total_y_position_list]
        #hold=input('hold')
    # my_dict={
    #     'signifigance_and_fold_enough':signifigance_and_fold_enough,
    #     'either_signifigance_or_fold_not_enough':either_signifigance_or_fold_not_enough,
    #     'metabolite':metabolite_list
    # }


    print(total_panda)

    total_panda=total_panda.loc[total_panda['fold']>0]

    total_panda['signifigance']=np.log(total_panda['signifigance'])
    total_panda['signifigance']=total_panda['signifigance'].mul(-1)

    #plt.clf()
    #fig=plt.figure()
    #fig.set_size_inches(10,10)
    
    #my_histogram,x_edges,y_edges=np.histogram2d(total_x_position_list,total_y_position_list,bins=[500,500])
    my_histogram,x_edges,y_edges=np.histogram2d(total_panda['fold'],total_panda['signifigance'],bins=[100,100])
    print(x_edges)
    print(y_edges)
    #print(my_histogram)
    #print(y_edges)
    print(my_histogram)
    my_histogram=np.log10(my_histogram)
    print(my_histogram)
    my_histogram=np.where(np.isfinite(my_histogram),my_histogram,0)
    print(my_histogram)
    #[print(np.log10(x)) for x in y_edges]
    #y_edges=np.log10(y_edges)
    #print(my_histogram)
    extent = [x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]]


    # #directions for median figure
    # fig,ax=plt.subplots()
    # divider=make_axes_locatable(ax)
    # plt.title('Mann-Whitney u-Test p-values vs. Fold Change of medians')
    # plt.ylabel('-log10(p-value)')
    # plt.xlabel('-log2(fold-change)')
    # tick_spacing=2
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    # plt.vlines(x=2,ymin=0,ymax=706,colors='g',linewidth=1)
    # plt.hlines(y=2,xmin=0,xmax=19.5,colors='g',linewidth=1)
    # cax = divider.append_axes('right', size='5%', pad=0.05)
    # image=ax.imshow(my_histogram.T,extent=extent,origin='lower',aspect='auto',cmap='magma')
    # fig.colorbar(image,cax=cax,orientation='vertical')
    # plt.show()
    # #plt.savefig('./median.png')

    #directions for average figure
    fig,ax=plt.subplots()
    divider=make_axes_locatable(ax)
    plt.title('Welch t-Test p-values vs. Fold Change of Averages')
    plt.ylabel('-log10(p-value)')
    plt.xlabel('-log2(fold-change)')
    tick_spacing=2
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plt.vlines(x=2,ymin=0,ymax=750,colors='g',linewidth=1)
    plt.hlines(y=2,xmin=0,xmax=20,colors='g',linewidth=1)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    image=ax.imshow(my_histogram.T,extent=extent,origin='lower',aspect='auto',cmap='magma')
    fig.colorbar(image,cax=cax,orientation='vertical')
    plt.show()
    #plt.savefig('./average.png')


    print('yes_signifigance_yes_fold '+str(sum(yes_signifigance_yes_fold)))
    print('yes_signifigance_no_fold '+str(sum(yes_signifigance_no_fold)))
    print('no_signifigance_no_fold '+str(sum(no_signifigance_no_fold)))
    print('no_signifigance_yes_fold '+str(sum(no_signifigance_yes_fold)))
    print(len(full_data_panda.at[0,'species']))
