{
   "application-pdf":{
      "properties":{
         "doi":{
            "type":"string"
         },
         "entities":{
            "properties":{
               "DATE":{
                  "type":"nested",
                  "properties":{
                     "count":{
                        "type":"long"
                     },
                     "name":{
                        "type": "multi_field",
                        "fields": {
                             "name": { "type": "string" },
                             "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                         }
                     }
                  }
               },
               "LOCATION":{
                  "type":"nested",
                  "properties":{
                     "count":{
                        "type":"long"
                     },
                     "name":{
                        "type": "multi_field",
                        "fields": {
                             "name": { "type": "string" },
                             "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                         }
                     }
                  }
               },
               "MONEY":{
                  "type":"nested",
                  "properties":{
                     "count":{
                        "type":"long"
                     },
                     "name":{
                        "type": "multi_field",
                        "fields": {
                             "name": { "type": "string" },
                             "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                         }
                     }
                  }
               },
               "ORGANIZATION":{
                  "type":"nested",
                  "properties":{
                     "count":{
                        "type":"long"
                     },
                     "name":{
                        "type": "multi_field",
                        "fields": {
                             "name": { "type": "string" },
                             "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                         }
                     }
                  }
               },
               "PERCENT":{
                  "type":"nested",
                  "properties":{
                     "count":{
                        "type":"long"
                     },
                     "name":{
                        "type": "multi_field",
                        "fields": {
                             "name": { "type": "string" },
                             "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                         }
                     }
                  }
               },
               "PERSON":{
                  "type":"nested",
                  "properties":{
                     "count":{
                        "type":"long"
                     },
                     "name":{
                        "type": "multi_field",
                        "fields": {
                             "name": { "type": "string" },
                             "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                         }
                     }
                  }
               },
               "TIME":{
                  "type":"nested",
                  "properties":{
                     "count":{
                        "type":"long"
                     },
                     "name":{
                        "type": "multi_field",
                        "fields": {
                             "name": { "type": "string" },
                             "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                         }
                     }
                  }
               },
               "emails":{
                  "type":"nested",
                  "properties":{
                     "count":{
                        "type":"long"
                     },
                     "name":{
                        "type": "multi_field",
                        "fields": {
                             "name": { "type": "string" },
                             "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                         }
                     }
                  }
               },
               "phones":{
                  "type":"nested",
                  "properties":{
                     "count":{
                        "type":"long"
                     },
                     "name":{
                        "type": "multi_field",
                        "fields": {
                             "name": { "type": "string" },
                             "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                         }
                     }
                  }
               },
               "sweet":{
                  "type":"nested",
                  "properties":{
                     "count":{
                        "type":"long"
                     },
                     "name":{
                        "type": "multi_field",
                        "fields": {
                             "name": { "type": "string" },
                             "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                         }
                     }
                  }
               },
               "urls":{
                  "type":"nested",
                  "properties":{
                     "count":{
                        "type":"long"
                     },
                     "name":{
                        "type": "multi_field",
                        "fields": {
                             "name": { "type": "string" },
                             "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                         }
                     }
                  }
               }
            }
         },
         "locations":{
            "type" : "geo_point",
            "lat_lon": true,
            "geohash": true
         },
         "geo":{
            "type":"nested",
            "properties":{
               "admin1Code":{
                  "type": "multi_field",
                  "fields": {
                       "admin1Code": { "type": "string" },
                       "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                   }
               },
               "admin2Code":{
                  "type": "multi_field",
                  "fields": {
                       "admin2Code": { "type": "string" },
                       "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                   }
               },
               "countryCode":{
                  "type": "multi_field",
                  "fields": {
                       "countryCode": { "type": "string" },
                       "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                   }
               },
               "location":{
                  "type" : "geo_point",
                  "lat_lon": true,
                  "geohash": true
               },
               "name":{
                  "type": "multi_field",
                  "fields": {
                       "name": { "type": "string" },
                       "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                   }
               }
            }
         },
         "id":{
            "type":"string"
         },
         "journal":{
            "properties":{
               "abstract":{
                  "type":"string"
               },
               "authors":{
                  "type":"nested",
                  "properties":{
                     "affiliations":{
                        "type": "multi_field",
                        "fields": {
                          "affiliations": { "type": "string" },
                          "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                        }
                     },
                     "name":{
                        "type": "multi_field",
                        "fields": {
                             "name": { "type": "string" },
                             "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                         }
                     }
                  }
               },
               "created-time":{
                  "type":"date",
                  "format":"strict_date_optional_time||epoch_millis"
               },
               "date":{
                  "type":"date",
                  "format":"strict_date_optional_time||epoch_millis"
               },
               "date-type":{
                  "type":"string"
               },
               "foot-note":{
                  "type":"string"
               },
               "header-authors":{
                  "type":"string"
               },
               "header-title":{
                  "type":"string"
               },
               "title":{
                  "type": "multi_field",
                  "fields": {
                       "title": { "type": "string" },
                       "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                   }
               },
               "related-publications":{
                  "type":"nested",
                  "properties":{
                    "title":{
                        "type": "multi_field",
                        "fields": {
                             "title": { "type": "string" },
                             "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                         }
                    },
                    "URL":{
                      "type": "multi_field",
                      "fields": {
                           "URL": { "type": "string" },
                           "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                       }
                    },
                    "abstract":{
                      "type": "multi_field",
                      "fields": {
                           "abstract": { "type": "string" },
                           "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
                       }
                    }
                  }
               }
            }
         },
         "local-path":{
            "type":"string"
         },
         "mime-type":{
            "type": "multi_field",
            "fields": {
                 "mime-type": { "type": "string" },
                 "raw":  { "type": "string", "index": "not_analyzed", "null_value": "NULL" }
             }
         }
      }
   }
}
