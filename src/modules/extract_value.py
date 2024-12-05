import json


def get_value_by_keys(json_file_path, keys):
    try:
        with open(json_file_path, "r") as file:
            data = json.load(file)
        if keys[0] not in data:
            raise KeyError("Key not found")
        value = data[keys[0]]
        for index in range(len(keys) - 1):
            value = value[keys[index + 1]]
        return value
    except FileNotFoundError:
        raise FileNotFoundError("File not found")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON file")


def get_company_by_image_name(image_name):
    if "BSG" in image_name:
        return "BlackSky"
    elif "ssc" in image_name:
        return "planet"
