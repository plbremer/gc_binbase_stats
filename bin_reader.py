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



class BinReader():

    def __init__(self):
        pass

    def assign_dict(self,temp_dict):
        self.bin_dict=temp_dict

    #def make_key_list(self):
    #    '''
    #    alphabetize as keys are unordered
    #    '''
    #    self.bin_keys=list(self.bin_dict.keys())
    #    self.bin_keys.sort()
    
    def reformat_spectrum_attribute(self,key):
        '''
        create two new keys based on key
        go through key, add values to two new keys
        typecast to float
        '''
        self.bin_dict[key+'_mz']=[]
        self.bin_dict[key+'_intensity']=[]
        
        #for annotations_spectrum in self.bin_dict[key]:
        annotations_spectrum=self.bin_dict[key]
        temp_mz_list=list()
        temp_intensity_list=list()
        temp_string_split=re.split(' |:',annotations_spectrum)
        #we add every even index to the mz list of lists (all the mz)
        self.bin_dict[key+'_mz'].append(temp_string_split[0::2])
        #we add every odd index to the intensity list of lists
        self.bin_dict[key+'_intensity'].append(temp_string_split[1::2])
        del self.bin_dict[key]

    def dict_to_panda(self):
        self.panda_representation=pd.DataFrame.from_dict(self.bin_dict)

    def do_everything(self,annotation_dict):
        self.assign_dict(annotation_dict)
        #self.make_key_list
        self.reformat_spectrum_attribute('spectra')
        #self.dict_to_panda()

if __name__ == '__main__':

    my_base='https://binvestigate.fiehnlab.ucdavis.edu/rest/bin/'
    my_bin='2'
    my_json=receive_url_return_dict(my_base,my_bin)

    my_BinReader=BinReader()
    my_BinReader.do_everything(my_json)

    print(my_BinReader.panda_representation)