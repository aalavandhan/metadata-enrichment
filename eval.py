from xtika.parser import *
import elasticsearch

from os import listdir, stat, remove
from os.path import join, isdir, getsize, isfile
from shutil import move, copyfile
from tika import language

import os
import errno
from util.timeout import timeout
from urlparse import urlparse

import cbor


import ntpath, re, sys, time, traceback, base64, hashlib,pdb

TEMP = "/Users/nithinkrishna/Desktop/temp"

MOUNT_NAME = 'common-crawl'

log = open("out.log", "a")

def genereateId(file):
  hasher = hashlib.sha1(file.split(MOUNT_NAME)[1])
  return base64.urlsafe_b64encode(hasher.digest()[0:10])

def parseCommonCrawlFile(path):
  res = cbor.load(open(path, "rb"))
  return json.loads(res)

class NEREvaluator:
  def __init__(self, compositeNER):
    self.data = compositeNER

  def opennlp(self):
    e = json.loads( self.data['openNLP entities'] )
    return e

  def corenlp(self):
    e = json.loads( self.data['coreNLP entities'] )
    return e

  def nltk(self):
    e = json.loads( self.data['nltk entities'] )
    return e

  def overlap(self):
    ENTITY_KEYS = ['DATE', 'ORGANIZATION', 'TIME', 'LOCATION', 'PERSON']

    opennlp = self.opennlp()
    corenlp = self.corenlp()
    nltk    = self.nltk()

    e1 = reduce(lambda m, e:  m + map(lambda x: x['name'], opennlp[e]) , opennlp, [ ])
    e2 = reduce(lambda m, e:  m + map(lambda x: x['name'], corenlp[e]), corenlp, [ ])
    e3 = reduce(lambda m, e:  m + map(lambda x: x['name'], nltk[e]), nltk, [ ])

    return {
      'opennlp': len(e1),
      'corenlp': len(e2),
      'nltk'   : len(e3),
      'opennlp-corenlp': len( set(e1) & set(e2) ),
      'corenlp-nltk'   : len( set(e2) & set(e3) ),
      'nltk-opennlp'   : len( set(e3) & set(e1) ),
      'union'   : len( set(e1) & set(e2) & set(e3) ),
      'joint-agreement': list(set(e1) & set(e2) & set(e3)),
    }

  def measurements(self):
    q = json.loads( self.data['quantities'] )['measurements']

    def qty(m):
      p = { }
      p['value'] = m['parsedValue'] if 'parsedValue' in m else 0
      p['normalizedValue'] = m['normalizedQuantity'] if 'normalizedQuantity' in m else 0
      p['unit']  = m['rawUnit']['name'] if 'rawUnit' in m and 'name' in m['rawUnit'] else 'XXX'
      p['unitType']  = m['rawUnit']['type'] if 'rawUnit' in m and 'type' in m['rawUnit'] else 'XXX'
      p['normalizedUnit']  = m['normalizedUnit']['name'] if 'normalizedUnit' in m and 'name' in m['normalizedUnit'] else 'XXX'
      p['normalizedUnitType']  = m['normalizedUnit']['type'] if 'normalizedUnit' in m and 'type' in m['normalizedUnit'] else 'XXX'
      return p

    def getQty(q, m):
      if m['type'] == 'value':
        q.append( qty(m['quantity']) )
      elif m['type'] == 'interval':
        if 'quantityLeast' in m:
          q.append( qty(m['quantityLeast']) )
        if 'quantityMost' in m:
          q.append( qty(m['quantityMost']) )
      return q

    return reduce(getQty, q, [ ])


class InformationExtractor:
  def __init__(self, file):
    self.id = genereateId(file)
    self.path = join(TEMP, self.id)
    self.tpath = join(TEMP, self.id + "~")
    copyfile(file, self.path)

    # fileData = parseCommonCrawlFile(file)
    # self.fileContent = fileData['response']['body']

    # Persist request data
    # self.requestData = dict(fileData)
    # self.requestData['response']['body'] = ''

    self.requestData = { }

    # try:
    #   self.requestData['domain'] = urlparse(self.requestData['url']).hostname
    # except:
    #   pass

    self.metadata = { }

  def loadMD(self):
    md = TikaWrapper(self.path).getMetadata()
    self.metadata = {
      'id': self.id,
      'content-type': md['Content-Type'],
      'tika-metadata': md,
      'size': getsize(self.path),
      'language': language.from_file(self.path),
      'crawl': self.requestData
    }


  def runNER(self):
    f = open(self.tpath, "w+")
    f.write(TikaWrapper(self.path).getContent().encode('UTF-8'))
    f.close()

    extracted = TikaWrapper(self.tpath).getInterstingRegions()
    f = open(self.tpath, "w+")
    f.write(extracted.encode('UTF-8'))
    f.close()

    evaL = NEREvaluator( TikaWrapper(self.tpath).runNER() )

    self.metadata['language'] = language.from_file(self.tpath)

    self.metadata['ner'] = {
      'opennlp': evaL.opennlp(),
      'corenlp': evaL.corenlp(),
      'nltk'   : evaL.nltk(),
      'overlap': evaL.overlap(),
    }

    try:
      self.metadata['measurements'] = evaL.measurements()
    except:
      self.metadata['measurements'] = [ ]

  #@timeout(80, os.strerror(errno.ETIMEDOUT))
  def extract(self):
    self.loadMD()

    try:
      self.runNER()
    except Exception as e:
      print "NER EXCEPTION {0}".format(e)
      pass

    # delete temp files
    remove(self.path)
    remove(self.tpath)
    return self.metadata


def dfs_traversal(path, ELASTIC):
  if isfile(path) and path.split("/")[-1]:
    print path
    md = InformationExtractor(path).extract()
    ELASTIC.index(index='polar2', body=md, id=md['id'], doc_type="ner")

    print "Successfully processed " + path
    print md
    return

  for f in listdir(path):
    try:
      dfs_traversal(join(path, f), ELASTIC)
    except Exception as e:
      log.write( "******** ERROR while processing ******** {0}\n".format(path)   )
      log.write( "******** ERROR while processing ******** {0}\n".format(e.args) )
      log.write( "******** ERROR while processing ******** {0}\n".format(e)      )
      traceback.print_exc(file=log)

if __name__ == '__main__':
  MOUNT_POINT = sys.argv[1]
  ELASTIC     = elasticsearch.Elasticsearch('http://104.236.190.155:9200')
  dfs_traversal(MOUNT_POINT, ELASTIC)

