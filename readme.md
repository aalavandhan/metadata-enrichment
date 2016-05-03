##Metadata Enrichment

This is a python wrapper which interfaces around tika-python. It calls various
tika-parsers in sequence  to perform metadata extraction and content enrichment.

It expects the grobid and geotropic servers to be running in the defined ports.

```
python main.py <PATH TO FILES>

```
##Metadata Evaluation

Evaluation script runs compositeNER tika parser to run NER and save metadata in elastic search
