from elasticsearch import Elasticsearch

es = Elasticsearch()


def create_es_index():
    """ 创建es索引 """
    body = {
        "mappings": {
            "doc": {
                "dynamic": "false",
                "properties": {
                    "title": {
                        "type": "text",
                        "analyzer": "ik_max_word"
                    },
                    "content": {
                        "type": "text",
                        "analyzer": "ik_smart"
                    },
                    "action_type": {
                        "type": "text"
                    },
                    "uid": {
                        "type": "text"
                    }
                }
            }
        }
    }
    # es.indices.create(index='sifou', body=body)
    print(es.indices.get_mapping(index='sifou'))

create_es_index()