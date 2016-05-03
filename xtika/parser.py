import tika
from   tika      import parser
from   tika.tika import *

import json

TIKA_SERVER = 'http://localhost:9998'

class TikaWrapper:
  def __init__(self, file):
    self.file = file

  def __call(self, params):
    (status, response) = callServer('put', TIKA_SERVER, '/rmeta', open(self.file, "r"),  params)

    if status != 200:
      raise "Tika Parse Exception"

    d = json.loads(response)[0]

    if 'X-TIKA:content' in d:
      content = d.pop('X-TIKA:content')
    else:
      content = ''

    return {
      'metadata': d,
      'content' : content
    }

  def getDOI(self):
    metadata = self.__call({ 'Content-Type': 'application/doi', 'X-filename': self.file })['metadata']
    return metadata['doi'].decode('string_escape')

  def parseWtihGrobid(self):
    metadata = self.__call({ 'Content-Type': 'application/grobid' })['metadata']
    return metadata

  def getInterstingRegions(self):
    metadata = self.__call({ 'Content-Type': 'application/tag-ratio' })['metadata']
    return metadata['trr-extracted']

  def runNER(self):
    metadata = self.__call({ 'Content-Type': 'application/ner' })['metadata']
    return metadata

  def get(self):
    return self.__call({ })

  def getContent(self):
    return self.__call({ })['content']

  def getMetadata(self):
    return self.__call({ })['metadata']
