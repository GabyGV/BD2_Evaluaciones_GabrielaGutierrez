
from elasticsearch import Elasticsearch







client = Elasticsearch(
    f"http://localhost:58265/"
)

searchParam = {"terms": {"group_id": [5]}}
response = client.search(index="groups", query=searchParam)
_sourceJson = response["hits"]["hits"][0]["_source"]["doc"]["docs"]



print(_sourceJson)