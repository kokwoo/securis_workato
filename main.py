import json

import yaml
from nested_lookup import nested_lookup

# Open the JSON file
with open("ebay_version.json", "r") as json_file:
    json_data = json.load(json_file)

# Recusive function to list all the nested json into a 2D array of [key, key_level]
def json_level_key(json_obj, level=0, data=[]):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            data.append([level, key])
            json_level_key(value, level + 1, data)
    elif isinstance(json_obj, list):
        for i, item in enumerate(json_obj):
            data.append([level, f"[{i}]"])
            json_level_key(item, level, data)
    return data


def create_picklist(enum_array):
    original_array = enum_array
    new_array = [[x.lower().replace("_", " ").capitalize(), x] for x in original_array]
    return new_array


# Convert the payload of each key into Workato format
def convert_payload(key, value):
    obj = {}
    obj["name"] = key
    obj["label"] = key
    if value in ["number", "integer", "boolean"]:
        obj["type"] = ":" + value
        obj["control_type"] = ":" + value
    elif value == "string":
        pass
    elif isinstance(value, dict):
        obj["type"] = ":object"
        obj["properties"] = []
    elif isinstance(value, list):
        obj["type"] = ":array"
        if isinstance(value[0], dict):
            obj["of"] = ":object"
            obj["properties"] = []
        else:
            obj["of"] = ":" + value[0]
    elif "Enum" in value:
        enum_name = value.split(":")[1].strip()
        obj["control_type"] = ":select"
        obj["pick_list"] = create_picklist(enum_name[1:-1].split(","))
        obj["toggle_hint"] = "Select from option list"
        obj["toggle_field"] = {}
        obj["toggle_field"]["name"] = key
        obj["toggle_field"]["label"] = key
        obj["toggle_field"]["control_type"] = ":text"
        obj["toggle_field"]["type"] = ":string"
        obj["toggle_field"]["toggle_hint"] = "Use custom value"
        obj["toggle_field"]["hint"] = ""
    return obj


def get_respective_values(key):
    lookup_values = nested_lookup(key, json_data)
    if key == "[0]":
        return "arr"
    return lookup_values[0]


workato_objdef = []
base_level = 0

keys_levels = json_level_key(json_data)

for key_level in keys_levels:
    key = key_level[1]
    curr_level = key_level[0]
    value = get_respective_values(key)

    if value == "arr":
        pass
    else:
        tup = convert_payload(key, value)
        if curr_level == 0:
            workato_objdef.append(tup)
        else:
            objdef = workato_objdef
            for i in range(curr_level):
                objdef = objdef[-1]["properties"]
            objdef.append(tup)

# Create the json file here - The actual workato format is still different we definitely still need to edit it
# but this should speed up the process of typing them out one by 1
with open("workato_object_definition.json", "w") as outfile:
    json.dump(workato_objdef, outfile, indent=4)


# Print the JSON object to the terminal / an alternative to the json file for easier copy pasting
json_string = json.dumps(workato_objdef, indent=6)
json_string = json_string.replace('"', "")
print(json_string)
