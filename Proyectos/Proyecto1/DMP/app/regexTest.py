from unicodedata import name


jobs = {
    "job_id": "job606",
    "status": "new",
    "msg": "",
    "control_data_source": "destination_es",
    "stages" : [
        {
            "name": "extract",
            "source_queue": "extract",
            "destination_queue": "%{transform->transformation->add_car}%"
        },
        {
            "name": "transform",
            "transformation": [
                {
                    "name": "add_car",
                    "type": "sql_transform",
                    "table": "car",
                    "expression": "SELECT %{field_description}% FROM %{table}% WHERE %{field_owner}% = %{doc_field}%",
                    "source_data_source": "database_car",
                    "destination_data_source": "destination_es",
                    "doc_field": "id",
                    "source_queue": "sql_queue",
                    "destination_queue": "%{transform->transformation->myregex}%",
                    "fields_mapping": {
                        "field_description": "description",
                        "field_owner": "owner"
                    }
                },
                {
                    "name": "myregex",
                    "type": "regex_transform",
                    "regex_config": {
                        "regex_expression": "^.* ([a-zA-z]{3}-[0-9]{3}) .*$",
                        "group": "1",
                        "field": "description"
                    },
                    "field_name": "placa",
                    "source_queue": "regex_queue",
                    "destination_queue": "%{load}%"
                }
            ]
        },
        {
            "name": "load",
            "source_queue": "ready",
            "destination_data_source": "destination_es",
            "index_name": "persona"
        }
    ]
}

def limpieza (dic):
    dest_queue = dic
    dest_queue = dest_queue.replace("%", "", 2)
    dest_queue = dest_queue.replace("{", "")
    dest_queue = dest_queue.replace("}", "")
    
    print("Solamente el destination_queue limpio: ", dest_queue)
    return (dest_queue.split("->"))

def get_destination_queue_load(dic):
    for elem in dic["stages"]:
        if (elem["name"] == "load"):
            print(elem["source_queue"])
            return elem["source_queue"]

def get_destination_queue_extract(dic):
    search_list = limpieza(dic["stages"][0]["destination_queue"])
    for element in search_list:
        for defi in dic["stages"]:
            if (defi["name"] == "load"):
                return get_destination_queue_load(dic)
            if (defi["name"] == search_list[0]):
                for trans in defi[search_list[1]]:
                    print(trans)
                    if (trans["name"] == search_list[2]):
                        return trans["source_queue"]
                

def get_destination_queue_transform(dic, name):
    for trans in dic["stages"][1]["transformation"]:
        search_list = limpieza(trans["destination_queue"])
        if (trans["name"] == name):
            if(search_list[0] == "load"):
                return get_destination_queue_load(dic)
            for elem in dic["stages"][1][search_list[1]]:
                if(elem["name"] == search_list[2]):
                    return elem["source_queue"]
    return 0


if (jobs["stages"][0]["name"]=="extract"):
    destination_queue_load = get_destination_queue_load(jobs)
    destination_queue_extract = get_destination_queue_extract(jobs)
    destination_queue_transform = get_destination_queue_transform(jobs, "add_car")
    destination_queue_transform = get_destination_queue_transform(jobs, "myregex")
    print("Extract: ",destination_queue_extract)
    print("Load: ",destination_queue_load)
    print("Transform: ", destination_queue_transform)
