import requests
import json
import pandas as pd
import re
import simplejson
import sys

from bin_reader import BinReader
from tree_reader import TreeReader

class BinvestigateWriter():

    def __init__(self,temp_min,temp_max,temp_bin_reader_url,temp_tree_reader_url):
        self.bin_id_min=temp_min
        self.bin_id_max=temp_max
        self.bin_reader_url=temp_bin_reader_url
        self.tree_reader_url=temp_tree_reader_url


    def get_keys_from_lowest_id(self):


        gotten_keys=False

        attempting_bin_id=self.bin_id_min

        while(gotten_keys==False):
            temp_bin_response=requests.get(self.bin_reader_url+attempting_bin_id)
            temp_tree_response=requests.get(self.tree_reader_url+attempting_bin_id)

            #print(attempting_bin_id)
            #print(temp_bin_response.status_code)
            #print(temp_tree_response.status_code)
            #hold=input('hold')
            if (temp_bin_response.status_code != 200) or (temp_tree_response.status_code != 200):

                print('no connection with bin '+attempting_bin_id)
                attempting_bin_id=str( int(attempting_bin_id)+1 )

                if attempting_bin_id>=self.bin_id_max:
                    return 'all_empty'
                
                continue

                


            elif (temp_bin_response.status_code == 200) and (temp_tree_response.status_code == 200):
                attempting_bin_id=str( int(attempting_bin_id)+1 )
                temp_BinReader=BinReader()
                try:
                    temp_BinReader.do_everything(temp_bin_response.json())
                except simplejson.errors.JSONDecodeError:
                    print('keys json decode error with bin '+str(int(attempting_bin_id)-1))
                    continue

                temp_TreeReader=TreeReader()
                try:
                    temp_TreeReader.do_everything(temp_tree_response.json())
                except simplejson.errors.JSONDecodeError:
                    print('keys json decode error with tree '+str(int(attempting_bin_id)-1))
                    continue
                both_reader_keys=list(temp_BinReader.bin_dict.keys())+list(temp_TreeReader.sunburst_dict.keys())
                #print('succeeded with bin id one less than '+attempting_bin_id)
                #print(both_reader_keys)
                #gotten_keys=True
                self.grand_dict={temp_key:[] for temp_key in both_reader_keys}
                
                #fucking hack to put group into the keys
                if 'group' not in self.grand_dict.keys():
                    self.grand_dict['group']=[]
                
                return 'success'
                
            #hold=input('hold')

        
        #self.grand_dict=dict()
        ##############
        #DO THING THAT SKIPS THIS ENTIRE BATCH IF FAIl
        ##############
        #print(self.grand_dict)
            
    def fill_grand_dict(self):

        #gotten_keys=False

        #attempting_bin_id=self.bin_id_min


        #while(gotten_keys==False):
        for i in range(int(self.bin_id_min),int(self.bin_id_max)):
            temp_bin_response=requests.get(self.bin_reader_url+str(i))
            temp_tree_response=requests.get(self.tree_reader_url+str(i))

            #print(attempting_bin_id)
            #print(temp_bin_response.status_code)
            #print(temp_tree_response.status_code)
            #hold=input('hold')
            if (temp_bin_response.status_code != 200) and (temp_tree_response.status_code != 200):
                #attempting_bin_id=str( int(attempting_bin_id)+1 )
                print('no connection with bin '+str(i))
                continue

            elif (temp_bin_response.status_code == 200) and (temp_tree_response.status_code == 200):
                #attempting_bin_id=str( int(attempting_bin_id)+1 )
                temp_BinReader=BinReader()
                try:
                    temp_BinReader.do_everything(temp_bin_response.json())
                except simplejson.errors.JSONDecodeError:
                    print('values json decode error with bin '+str(i))
                    continue

                temp_TreeReader=TreeReader()
                try:
                    temp_TreeReader.do_everything(temp_tree_response.json())
                except simplejson.errors.JSONDecodeError:
                    print('values json decode error with tree '+str(i))
                    continue
                
                this_bins_entire_dict={**temp_BinReader.bin_dict,**temp_TreeReader.sunburst_dict}

                for key in self.grand_dict.keys():
                    #fucking hack to work around the group
                    try:
                        self.grand_dict[key].append(this_bins_entire_dict[key])
                    except KeyError:
                        if key=='group':
                            self.grand_dict['group'].append('null')
                        elif key=='inchikey':
                            self.grand_dict['inchikey'].append('null')
                        else:
                            #print('test')
                            print(key)
                            sys.exit()

                
                #both_reader_keys=list(temp_BinReader.bin_dict.keys())+list(temp_TreeReader.sunburst_dict.keys())
                #print('succeeded with bin id one less than '+attempting_bin_id)
                #print(both_reader_keys)
                #gotten_keys=True
                
            #hold=input('hold')

        #self.grand_dict=dict()
        #self.grand_dict={temp_key:[] for temp_key in both_reader_keys}
        #print(self.grand_dict)    

    def grand_dict_to_panda(self):
        self.panda_representation=pd.DataFrame.from_dict(self.grand_dict)

    def write_panda_to_pickle(self,base_path):
        self.panda_representation.to_pickle(path=base_path+self.bin_id_min+'.bin',compression='infer',protocol=5)
    
    def do_everything(self,base_path):
        able_to_find=self.get_keys_from_lowest_id()
        #print('bin id min')
        #print(self.bin_id_min)
        if able_to_find == 'success':
            self.fill_grand_dict()
            self.grand_dict_to_panda()
            self.write_panda_to_pickle(base_path)
        elif able_to_find== 'all_empty':
            temp=open('/home/rictuar/coding_projects_database/gc_binbase_results_'+self.bin_id_min+'.null','w')
            temp.write('null')
            temp.close()
    
    #/home/rictuar/coding_projects_database/gc_binbase_results_

if __name__ == '__main__':



    #for i in range(1,1000000,10000):
    this_min=1
    this_max=1000
    this_gap=10

    
    for i in range(this_min,this_max,this_gap):
        
        temp_logfile_location='/home/rictuar/coding_projects_database/logfiles/log_'+str(i)+'.log'
        #print='./log_'+str(i)+'.log'
        temp_logfile=open(temp_logfile_location,'w')
        sys.stdout=temp_logfile


        my_BinvestigateWriter=BinvestigateWriter(str(i),str(i+this_gap),
        #my_BinvestigateWriter=BinvestigateWriter('700000','700010',
            'https://binvestigate.fiehnlab.ucdavis.edu/rest/bin/',
            'https://binvestigate.fiehnlab.ucdavis.edu/rest/bin/classificationTree/')
        
        my_BinvestigateWriter.do_everything('/home/rictuar/coding_projects_database/gc_binbase_results_')        



        #print(i)

    #hold=input('hold')
    #my_BinvestigateWriter=BinvestigateWriter('1','10',
    #my_BinvestigateWriter=BinvestigateWriter('700000','700010',
    #    'https://binvestigate.fiehnlab.ucdavis.edu/rest/bin/',
    #    'https://binvestigate.fiehnlab.ucdavis.edu/rest/bin/classificationTree/')
    #my_BinvestigateWriter.do_everything('/home/rictuar/coding_projects_database/gc_binbase_results_')
    #my_BinvestigateWriter.get_keys_from_lowest_id()
    #my_BinvestigateWriter.get_keys_from_lowest_id
    #my_BinvestigateWriter.fill_grand_dict()
    #my_BinvestigateWriter.grand_dict_to_panda()
    #print(my_BinvestigateWriter.panda_representation)
    #my_BinvestigateWriter.write_panda_to_pickle('/home/rictuar/coding_projects_database/gc_binbase_results_')