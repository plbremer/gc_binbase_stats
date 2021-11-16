import requests
from pprint import pprint
import json

if __name__ == "__main__":



    base='http://127.0.0.1:5000/'

    temp_incoming_json_dict={"additional_slider_min_fold_change": [5], "additional_toggleswitch": [True], "aggregate_on_page_rangeslider": None, "aggregate_on_page_spinners": 1, "compounds": [["18"]], "from_disease": [["No"]], "from_organ": [["A18.024.937"]], "from_species": [["161934","123"]], "to_disease": [["No"]], "to_organ": [["A12.207.152", "A12.207.152.693", "A12.207.152.846"]], "to_species": [["15367", "147368", "204232"]]}
    #test=json.dumps(temp_incoming_json_dict)
    #print(test)

    #temp_incoming_json_string={'whole_json':'{"additional_slider_min_fold_change": [5], "additional_toggleswitch": [true], "aggregate_on_page_rangeslider": null, "aggregate_on_page_spinners": 1, "compounds": [["18"]], "from_disease": [["No"]], "from_organ": [["A18.024.937"]], "from_species": [["161934"]], "to_disease": [["No"]], "to_organ": [["A12.207.152", "A12.207.152.693", "A12.207.152.846"]], "to_species": [["15367", "147368", "204232"]]}'}


    #my_generated_query=
    response=requests.post(base+'foldchangetable/',json=temp_incoming_json_dict)

    #pprint(response.json())