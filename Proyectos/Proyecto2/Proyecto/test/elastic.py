
from elasticsearch import Elasticsearch







client = Elasticsearch(
    f"http://localhost:61707/"
)


resp = client.search(index="groups", query={"match_all": {}})


print(resp)