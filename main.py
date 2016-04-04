import tika
import tika.detector

from ner.custom_extractor import *
from ner.stanford_extractor import *
from ner.geo_topic import *

from meta.extractor import *
from meta.grobid import *

from xtika.parser import *

import elasticsearch

from os import listdir, stat
from os.path import join, isdir, getsize

import sys
import traceback

import os
import errno
from util.timeout import timeout

import time

INTERESTED = [
  "text-html",
  "application-xhtml+xml",
  "image-jpeg",
  "application-pdf",
  "image-png",
  "image-gif",
  "application-rss+xml",
  "application-xml",
]

GROBID_TYPES = [
  "application-pdf",
]

TAG_RATIO_TYPES = [
  "text-html",
  "application-xhtml+xml",
  "application-rss+xml",
  "application-xml",
]

NON_TEXT_TYPES = [
  "image-jpeg",
  "image-png",
  "image-gif",
]

class InformationExtractor:
  def __init__(self, file, type):
    self.file = file
    self.xtika = TikaWrapper(file)
    self.extracted = { }
    self.fileType = type


  def extractContent(self):
    if self.fileType in NON_TEXT_TYPES:
      metadata = self.xtika.getMetadata()

      def xDecode(md):
        if md.__class__.__name__ == "list":
          return "\n".join(map(lambda x: x.decode('UTF-8'), md))
        else:
          return md.decode('UTF-8')

      self.content = "\n".join(map(xDecode, metadata.values()))
      self.extracted["additional"] = metadata
    elif self.fileType in TAG_RATIO_TYPES:
      self.content = self.xtika.getInterstingRegions()
    else:
      self.content = self.xtika.getContent()

    try:
      self.content = self.content.decode("utf-8")
    except Exception as e:
      # Do Nothing
      pass

  def extractJournal(self):
    # Additional Parsers
    grobidInfo = self.xtika.parseWtihGrobid()
    self.extracted['journal'] = GrobidParser(grobidInfo).filter()

  def extractEntities(self):
    trained = StanfordExtractor(self.content).extract()
    custom  = CustomEntityExtractor(self.content).extract()

    self.extracted['entities'] = {
      'emails' : custom['emails'],
      'phones' : custom['phones'],
      'urls'   : custom['urls'],
      'sweet'  : custom['sweet'],
      'LOCATION'     : trained['LOCATION'],
      'ORGANIZATION' : trained['ORGANIZATION'],
      'DATE'         : trained['DATE'],
      'MONEY'        : trained['MONEY'],
      'PERSON'       : trained['PERSON'],
      'PERCENT'      : trained['PERCENT'],
      'TIME'         : trained['TIME'],
    }

  def extractLocations(self):
    locations = map(lambda l: l['name'], self.extracted['entities']['LOCATION'])
    if len(locations) > 0:
      gt = GeoTopic(locations)
      self.extracted['geo'] = gt.getInfo()
      self.extracted['locations'] = gt.getLocations()

  def setIdentifiers(self):
    doi = self.xtika.getDOI()
    self.extracted["doi"] = doi
    self.extracted["id"] = doi.replace('http://bit.ly/','')
    self.extracted["local-path"] = self.file
    self.extracted["mime-type"] = self.fileType

  @timeout(30, os.strerror(errno.ETIMEDOUT))
  def extract(self):
    self.extractContent()

    self.extractEntities()

    self.extractLocations()

    if self.fileType in GROBID_TYPES:
      self.extractJournal()

    self.setIdentifiers()

    return self.extracted


def listFolders(path):
  return filter(lambda f: isdir(join(path, f)), listdir(path))

PATH   = sys.argv[1]
TYPE = "image-jpeg"

log = open("error.log", "a")

es = elasticsearch.Elasticsearch('http://104.236.190.155:9200')

for f in listFolders(PATH):
  for file in listdir(join(PATH, f)):

    path = join(PATH, f, file)

    try:
      print " --- Began Extraction {0} ---".format(path)
      extracted = InformationExtractor(path, TYPE).extract()
      decoded = json.loads(json.dumps(extracted).decode('UTF-8'))
      es.index(index='polar', doc_type=TYPE, body=decoded, id=extracted["id"])
      print " --- Successfully Completed {0} ---".format(path)
      time.sleep(1.5)
    except Exception as e:
      log.write(" --- ERROR while processing {0} ----\n".format(path))
      log.write("{0}\n".format(e))
      log.write(traceback.format_exc())





