import dash  
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import dash_core_components as dcc
import dash_daq as daq
import dash_table as dt
import json
from pprint import pprint
import pandas
from dash.dependencies import Input, Output, State

'''
at the moment, the way that this works is, you kill step 14 4 times, once for compound species organ disease
and each time, you come here and run the thing for the iteration that you killed it for

take the output table and put it into the shrink text file
'''



external_stylesheets = [dbc.themes.CERULEAN]
app=dash.Dash(__name__,external_stylesheets=external_stylesheets,show_undo_redo=True)

#to get the dagre layout for cytoscape
cyto.load_extra_layouts()


annotation_address='/home/rictuar/coding_projects/fiehn_work/gc_bin_base/text_files/results/1/step_14_reduce_hierarchy_complexity/organ_list.csv'
json_address='/home/rictuar/coding_projects/fiehn_work/binvestigate_webapp/dash_app_input/cyto_format_organ.json'

annotations_panda=pandas.read_csv(annotation_address,sep='¬')

temp_json_file=open(json_address,'r')
network_dict=json.load(temp_json_file)
temp_json_file.close()



for temp_element in network_dict['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here

    #pprint(temp_element['data'])
    #print(annotations_panda.loc[(annotations_panda['node_id'].astype(str))==temp_element['data']['id'],'english_name'].values)

    temp_element['data']['label']=annotations_panda.loc[
        (annotations_panda['node_id'].astype(str))==temp_element['data']['id'],'english_name'
    ].values[0]

    temp_element['selectable']=True
    #print(annotations_panda.loc[annotations_panda['node_id']==temp_element['data']['id'],'we_map_to'].values[0]+'asdf')
    #hold=input('---------')
    if annotations_panda.loc[annotations_panda['node_id'].astype(str)==temp_element['data']['id'],'we_map_to'].values[0]=='Yes':
        #print('hi')
        temp_element['classes']='mapped_to'
    else:
        #print('hi2')
        temp_element['classes']='combination'





    #temp_element['classes']='not_selected'
    #temp_element['data']['label']=replace_space_with_newline(temp_element['data']['label'])

'''
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

basic_stylesheet=[
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
        'selector':'.mapped_to',
        'style':{
            'background-color':'green'
        }
    },
    {
        'selector':'.combination',
        'style':{
            'background-color':'red'
        }
    }
]


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
                            id='cytoscape',
                            layout={'name':'dagre'},
                            elements=network_dict['elements'],
                            stylesheet=basic_stylesheet,
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
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        #a header
                        dt.DataTable(
                            id='my_table',
                            columns=[
                                #{'name': 'row_num', 'id': 'row_num'},
                                {'name': 'nodes_to_keep', 'id': 'nodes_to_keep'}
                            ],
                            data=[]
                        )
                    ]
                ),
                width='auto'
            )
        )
    ]
)

def delete_node_reconnect_cyto_elements(temp_elements,temp_tapnode):

    #scroll through nodes and delete the element where [data][id] is the tempnode[id]
    #scroll through the edges
    #there are some number of edges where the element in question is a source
    #some number of edges where the element in question is a target
    #both need to be deleted
    #make an edge between each source and each target instance

    targets_when_node_is_source=list()
    sources_when_node_is_target=list()
    indices_to_keep=list()
    for i,temp_edge in enumerate(temp_elements['edges']):
        if temp_edge['data']['source']==temp_tapnode['id']:
            targets_when_node_is_source.append(temp_edge['data']['target'])
        elif temp_edge['data']['target']==temp_tapnode['id']:
            sources_when_node_is_target.append(temp_edge['data']['source'])
        else:
            indices_to_keep.append(i)
    
    new_edges=list()

    print(sources_when_node_is_target)
    print(targets_when_node_is_source)


    for i in range(len(targets_when_node_is_source)):
        for j in range(len(sources_when_node_is_target)):
            new_edges.append(
                {
                    'data':{
                        'key':0,
                        'source':sources_when_node_is_target[j],
                        'target':targets_when_node_is_source[i]
                    }
                }
            )


    print(new_edges)
    #hold=input('hold')

    updated_edges=list()
    for i in indices_to_keep:
        updated_edges.append(temp_elements['edges'][i])
    updated_edges=updated_edges+new_edges
    temp_elements['edges']=updated_edges



    #find the node and remove it
    temp_node_index=0
    for i, temp_node in enumerate(temp_elements['nodes']):
        if temp_node['data']['id']==temp_tapnode['id']:
            temp_node_index=i
            break

    temp_elements['nodes'].pop(temp_node_index)

    return temp_elements

            




@app.callback(
    [Output(component_id='my_table',component_property='data'),
    Output(component_id='cytoscape',component_property='elements')],
    [Input(component_id='cytoscape',component_property='tapNodeData')],
    [State(component_id='cytoscape',component_property='elements')]
)
def update_app(
    cytoscape_tapnodedata,
    cytoscape_elements
):
    print('------------------------------------------------------------')
    pprint(network_dict['elements'])
    print('------------------------------------------------------------')
    pprint(cytoscape_tapnodedata)    

    cytoscape_elements=delete_node_reconnect_cyto_elements(cytoscape_elements,cytoscape_tapnodedata)

    # table_output=[
    #     {
    #         'nodes_to_keep':{i:temp_node['data']['id'] for i,temp_node in enumerate(cytoscape_elements['nodes'])}
    #     }
    # ]

    table_output=[
        {'nodes_to_keep':temp_node['data']['id']}  for temp_node in cytoscape_elements['nodes']
    ]
    #table_output_panda=pandas.DataFrame.from_dict(table_output)
    #table_output=table_output_panda.to_dict(orient='records')

    #table_output=[temp_node['data']['id'] for temp_node in cytoscape_elements['nodes']]
    print(table_output)

    return table_output,cytoscape_elements

if __name__ == "__main__":
    app.run_server(debug=True)