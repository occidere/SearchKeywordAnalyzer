import modules.parser as parser
import json

json_result = parser.get_json_result(top20_list=parser.get_top20_list())
json_string_result = json.loads(json_result)
print(json_string_result)
