from django.test import TestCase
from elasticsearch import Elasticsearch

# Create your tests here.

es = Elasticsearch()
# es.index(index='p1', doc_type='doc', id=1, body={'name':'吴彦祖','age':18})

# print(es.get(index='p1', doc_type='doc', id=1))

# body = {
#     'query':{
#         'match':{
#             'age':18
#         }
#     }
# }
# print(es.search(index='p1', doc_type='doc', body=body, _source='name'))

print(es.get_source(index='p1', doc_type='doc', id=1))

print(es.info())

# index
body = {
    'mappings':{
        'doc':{
            'properties':{
                'name':{
                    'type':'text',
                    'analyzer':'ik_smart'
                },
                'age':{
                    'type':'text',
                    'index':'true'
                }
            }
        }
    }
}

# print(es.indices.delete(index='p2'))

# print(es.indices.create(index='p2', body=body))

print(es.indices.get_mapping(index='p2'))
