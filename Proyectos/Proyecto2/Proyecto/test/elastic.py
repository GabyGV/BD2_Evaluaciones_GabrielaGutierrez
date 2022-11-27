
from elasticsearch import Elasticsearch







client = Elasticsearch(
    f"http://localhost:53599/"
)


resp = client.search(index="groups", query={"match_all": {}})


print(resp)