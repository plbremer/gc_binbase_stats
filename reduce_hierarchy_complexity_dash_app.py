import dash  
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import dash_core_components as dcc
import dash_daq as daq
import dash_table as dt
import json
from pprint import pprint



compound_annotation_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/1/step_14_reduce_hierarchy_complexity/compound_list.csv'
compound_annotations_panda=pandas.read_pickle(compound_annotation_address,sep='¬')

compound_json_address='/home/rictuar/coding_projects/fiehn_work/binvestigate_webapp/dash_app_input/cyto_format_compound.json'
temp_json_file=open(compound_json_address,'r')
compound_network_dict=json.load(temp_json_file)
temp_json_file.close()


for temp_element in compound_network_dict['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here

    
    
    try:
        temp_element['data']['label']='Bin: '+temp_element['data']['common_name']
    except KeyError:
        temp_element['data']['label']=temp_element['data']['name']
    temp_element['selectable']=True
    temp_element['classes']='not_selected'
    #temp_element['data']['label']=replace_space_with_newline(temp_element['data']['label'])

species_json_address='/home/rictuar/coding_projects/fiehn_work/binvestigate_webapp/dash_app_input/cyto_format_species.json'
temp_json_file=open(species_json_address,'r')
species_network_dict_from=json.load(temp_json_file)
temp_json_file.close()
for temp_element in species_network_dict_from['elements']['nodes']:
    pprint(temp_element)
    hold=input('hold')

    #same logic as compound
    temp_element['data']['label']=temp_element['data']['scientific_name']
    temp_element['selectable']=True
    temp_element['classes']='not_selected'

organ_json_address='/home/rictuar/coding_projects/fiehn_work/binvestigate_webapp/dash_app_input/cyto_format_organ.json'
temp_json_file=open(organ_json_address,'r')
organ_network_dict_from=json.load(temp_json_file)
temp_json_file.close()
for temp_element in organ_network_dict_from['elements']['nodes']:
    #same logic as compound
    temp_element['data']['label']=temp_element['data']['mesh_label']
    temp_element['selectable']=True
    temp_element['classes']='not_selected'

disease_json_address='/home/rictuar/coding_projects/fiehn_work/binvestigate_webapp/dash_app_input/cyto_format_disease.json'
temp_json_file=open(disease_json_address,'r')
disease_network_dict_from=json.load(temp_json_file)
temp_json_file.close()
for temp_element in disease_network_dict_from['elements']['nodes']:
    #same logic as compound
    temp_element['data']['label']=temp_element['data']['mesh_label']
    temp_element['selectable']=True
    temp_element['classes']='not_selected'






'''


app.layout=html.Div(
    [
        #title
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        #a header
                        html.H1('cyto'),
                        html.Br(),
                        html.Br(),
                        html.Br()
                    ]
                ),
                width='auto',
            ),
            justify='center'
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    children=[
                        #compounds
                        cyto.Cytoscape(
                            id='cytoscape_compound',
                            layout={'name':'dagre'},
                            elements=compound_network_dict['elements'],
                            stylesheet=[
                                {
                                    'selector':'node',
                                    'style':{
                                        'content':'data(label)',
                                        'text-wrap':'wrap',
                                        'text-max-width':100,
                                        'font-size':13
                                    }
                                    
                                },
                                {
                                    'selector':'.selected',
                                    'style':{
                                        'background-color':'red'
                                    }
                                },
                                #'text-wrap':'wrap'
                            ],
                            minZoom=0.3,
                            maxZoom=5
                        )
                    ]
                ),
                width='auto',
                align='center'
            ),
            justify='center'
        ),

'''