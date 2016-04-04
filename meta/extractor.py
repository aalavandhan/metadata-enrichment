class MetadataExtractor:
  def __init__(self, metadata):
    self.metadata = metadata

  def extract(self):
    return map(lambda v: v.decode('UTF-8'), self.metadata.values())
