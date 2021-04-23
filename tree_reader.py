import requests
import json
import pandas as pd
import re

def receive_url_return_dict(url_beginning,bin_id):

    temp_response=requests.get(url_beginning+bin_id)
    #print(temp_response)
    json_object=temp_response.json()
    #print(json_object)
    return json_object

class TreeReader():

    def __init__(self):
        pass

    def assign_dict(self,temp_dict):
        self.sunburst_dict=temp_dict        


    def reformat_tree_attribute(self):
        self.sunburst_dict['species']=list()
        self.sunburst_dict['organ']=list()
        self.sunburst_dict['count']=list()
        self.sunburst_dict['intensity']=list()

        species_keys=list(self.sunburst_dict['value'].keys())
        species_keys.sort()
        #print(species_keys)

        for species_key in species_keys:

            organ_keys=list(self.sunburst_dict['value'][species_key].keys())
            organ_keys.sort()

            for organ_key in organ_keys:

                temp_count=self.sunburst_dict['value'][species_key][organ_key]['count']
                temp_intensity=self.sunburst_dict['value'][species_key][organ_key]['intensity']

                self.sunburst_dict['species'].append(species_key)
                self.sunburst_dict['organ'].append(organ_key)
                self.sunburst_dict['count'].append(temp_count)
                self.sunburst_dict['intensity'].append(temp_intensity)      

        del self.sunburst_dict['value']

    def dict_to_panda(self):
        #self.panda_representation=pd.DataFrame.from_dict(self.sunburst_dict)    
        self.panda_representation=pd.DataFrame(columns=list(self.sunburst_dict.keys()))
        temp=(list(self.sunburst_dict.keys()))
        #print(temp)
        #print(self.panda_representation)
        #print(self.sunburst_dict['count'])
        
        self.panda_representation=self.panda_representation.append({
            '_id':self.sunburst_dict['_id'],
            'count':self.sunburst_dict['count'],
            'species':self.sunburst_dict['species'],
            'organ':self.sunburst_dict['organ'],
            'intensity':self.sunburst_dict['intensity'],
        },ignore_index=True)

    def do_everything(self,temp_dict):
        self.assign_dict(temp_dict)
        #self.make_key_list
        self.reformat_tree_attribute()
        #self.dict_to_panda()        

if __name__ == '__main__':
    my_base='https://binvestigate.fiehnlab.ucdavis.edu/rest/bin/classificationTree/'
    my_bin='2'
    my_json=receive_url_return_dict(my_base,my_bin)

    my_TreeReader=TreeReader()
    my_TreeReader.do_everything(my_json)
    print(my_TreeReader.panda_representation)

