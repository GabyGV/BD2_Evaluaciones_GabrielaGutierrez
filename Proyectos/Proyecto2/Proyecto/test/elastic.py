
from elasticsearch import Elasticsearch







client = Elasticsearch(
    f"http://localhost:53599/"
)

searchParam = {"terms": {"group_id": [2]}}
response = client.search(index="groups", query=searchParam)
_sourceJson = response["hits"]["hits"][0]["_source"]["doc"]["docs"]



print(_sourceJson)