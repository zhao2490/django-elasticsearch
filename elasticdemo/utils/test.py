from elasticsearch import Elasticsearch

es = Elasticsearch()

print(es.search(index='sifou'))