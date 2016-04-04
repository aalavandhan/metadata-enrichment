# To fetch location information from elasticsearch documents
# into an OFFLINE csv so that it works with Khooshe

import elasticsearch

es = elasticsearch.Elasticsearch('http://104.236.190.155:9200')

es.search(index="polar", doc_type='application-pdf', size="20", body={
  "from": 10
})
