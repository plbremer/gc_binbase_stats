import pandas as pd
import dash_bio as dashbio
#import dash_core_components as dcc
from dash import Dash
import numpy as np
import dash_core_components as dcc
import dash_html_components as html



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
    temp_fold_panda['signifigance']=temp_signifigance_panda['signifigance']
    #snap from dash plotly docs. idk what it is. something genomics.
    temp_fold_panda['snap']='from: '+temp_fold_panda['from'].astype(str)+' to: '+temp_fold_panda['to'].astype(str)
    temp_fold_panda.drop(['from','to'],inplace=True,axis='columns')
    temp_fold_panda['metabolite']=temp_metabolite

    return temp_fold_panda


def create_volcano_plot(temp_panda):
    print(temp_panda)
    hold=input('hold')
    
    my_plot=dashbio.VolcanoPlot(
        dataframe=temp_panda,
        p='signifigance',
        effect_size='fold',
        snp='snap',
        gene='metabolite'
    ) 
    #fig = create_volcano(dataframe, title=dict(text='XYZ Volcano plot'))

    #plotly.offline.plot(fig, image='png')

    #dcc.Graph(figure=my_plot)
    return my_plot


if __name__=="__main__":
    #basic usage instructions
    #choose the row of the metabolite that you want
    #choose the intensity fold change that you want
    #choose the signifigance test that you want
    #run the app and you can see the volcano plot
    
    
    min_fold_change=0
    #input_panda_address='../results/'+str(min_fold_change)+'/step_6_b_generate_signifigance_test_matrices/binvestigate_with_signifigance_matrices.bin'
    input_panda_address='../../results/'+str(min_fold_change)+'/step_6_b_generate_signifigance_test_matrices/binvestigate_with_signifigance_matrices.bin'

    full_data_panda=pd.read_pickle(input_panda_address)

    fold_panda=full_data_panda.at[0,'fold_change_median_intensity']
    signifigance_panda=full_data_panda.at[0,'signifigance_mannwhitney']
    metabolite=full_data_panda.at[0,'name']

    panda_for_volcano=coerce_our_structure_to_plotly_volcano(fold_panda,signifigance_panda,metabolite)

    print(panda_for_volcano)
    temp_volcano=create_volcano_plot(panda_for_volcano)

    app = Dash(__name__)

    app.layout=html.Div(
        dcc.Graph(
            id='my_volcano',
            figure=temp_volcano
        )
    )
    
    app.run_server(debug=True)




