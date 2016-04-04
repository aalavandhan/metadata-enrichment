import tika
from   tika      import parser
from   tika.tika import *

import json

import pdb

TIKA_SERVER = 'http://localhost:9998'

class TikaWrapper:
  def __init__(self, file):
    self.file = file

  def __call(self, params):
    (status, response) = callServer('put', TIKA_SERVER, '/rmeta', open(self.file, 'r'),  params)

    if status != 200:
      raise "Tika Parse Exception"

    return json.loads(response)[0]

  def getDOI(self):
    metadata = self.__call({ 'Content-Type': 'application/doi', 'X-filename': self.file })
    return metadata['doi'].decode('string_escape')

  def parseWtihGrobid(self):
    metadata = self.__call({ 'Content-Type': 'application/grobid' })
    return metadata

  def getInterstingRegions(self):
    metadata = self.__call({ 'Content-Type': 'application/tag-ratio' })
    return metadata['trr-extracted']

  def getContent(self):
    return parser.from_file(self.file, TIKA_SERVER)['content']

  def getMetadata(self):
    return parser.from_file(self.file, TIKA_SERVER)['metadata']
