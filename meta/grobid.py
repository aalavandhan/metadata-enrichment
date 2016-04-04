import json
import os

import pdb

class GrobidParser:
  def __init__(self, metadata):
    self.metadata = metadata

  def _getFeature(self, data, key):
    keys = key.split("-")

    try:
      feature = reduce(lambda m, k: m[k], keys, data)
    except:
      feature = None

    return feature

  def getRelated(self, txt):
    if txt.__class__.__name__ == "list":
      query = " ".join(txt)
    elif txt.__class__.__name__ == "dict":
      query = " ".join(txt.values())
    else:
      query = txt

    print " ---- SCHOLAR QUERY ----- {0}".format(query)

    p = os.popen('./util/scholar.py -c 20 --some "{0}" --cookie-file="cookie.txt" --csv'.format(query.decode('UTF-8')))

    def getLine(line):
      parts = line.split('|')

      return {
        'title'   : parts[0],
        'URL'     : parts[1],
        'abstract': parts[10],
      }

    return map(getLine, p.readlines())

  def accumulateRelated(self, authors, title):
    if len(authors) > 0:
      authorRecords = filter(lambda a: len(a['affiliations']) > 0, authors)
      affiliations = reduce(lambda m,a: m + a['affiliations'], authorRecords, [ ])

      if len(affiliations) > 0:
        return self.getRelated(affiliations)

    if title:
      return self.getRelated(title)

    if len(authors) > 0:
      authorRecords = filter(lambda a: a['name'] != None, authors)
      authorNames = map(lambda a: a['name'], authorRecords)

      if len(authorNames) > 0:
        return self.getRelated(authorNames)

    return [ ]


  def getAuthors(self):
    ad = self._getFeature(self.TEI, 'teiHeader-fileDesc-sourceDesc-biblStruct-analytic-author')

    if not ad:
      return [ ]

    print " --- AUTHOR DATA -- {0}".format(ad)

    def getAuthor(a):
      try:
        if a['persName']['forename'].__class__.__name__ == "dict":
          authorName = a['persName']['forename']['content']
        else:
          authorName = a['persName']['forename'][0]['content'] + " " + a['persName']['forename'][1]['content']

        authorName = authorName + " " + a['persName']['surname']
      except:
        authorName = None

      try:
        if a['affiliation'].__class__.__name__ == "dict":
          if a['affiliation']['orgName'].__class__.__name__ == "dict":
            affiliations = [ a['affiliation']['orgName']['content'] ]
          elif a['affiliation']['orgName'].__class__.__name__ == "list":
            affiliations = map(lambda o: o['content'], a['affiliation']['orgName'])
          else:
            affiliations = [ a['affiliation']['orgName'] ]
        else:
          affiliations = map(lambda o: o['content']['orgName'], a['affiliation'])
      except:
        affiliations = [ ]

      return {
        "name": authorName,
        "affiliations": affiliations,
      }

    results = ( [ getAuthor(ad) ] if ad.__class__.__name__ == "dict" else map(getAuthor, ad) )
    #Return valid results
    return filter(lambda r: r['name'] != None or r['affiliations'] != [ ], results)

  def filter(self):
    try:
      self.TEI = json.loads(self.metadata["grobid:header_TEIJSONSource"])["TEI"]
    except:
      return { }

    authors = self.getAuthors()
    title = self._getFeature(self.metadata, "dc:title")
    headerTitle = self._getFeature(self.metadata, "grobid:header_Title")

    print " --- Document Title {0} -- ".format(title)
    print " --- Header Title {0} -- ".format(headerTitle)
    print " --- Authors {0} -- ".format(authors)

    if headerTitle:
      related = self.accumulateRelated(authors, headerTitle)
    else:
      related = self.accumulateRelated(authors, title)


    print " --- FOUND {0} Related articles ---- ".format(len(related))

    return {
      "title": title,
      "created-time":  self._getFeature(self.metadata, "dcterms:created"),
      "header-title": headerTitle,
      "header-authors": self._getFeature(self.metadata, "grobid:header_Authors"),
      "abstract": self._getFeature(self.TEI, 'teiHeader-profileDesc-abstract-p'),
      "date": self._getFeature(self.TEI, 'teiHeader-fileDesc-publicationStmt-date-when'),
      "date-type": self._getFeature(self.TEI, 'teiHeader-fileDesc-publicationStmt-date-type'),
      "authors": authors,
      "foot-note": self._getFeature(self.TEI, 'teiHeader-fileDesc-sourceDesc-biblStruct-note-content'),
      "related-publications": related
    }
