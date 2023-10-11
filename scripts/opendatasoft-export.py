import sys
import csv
import os
from pymongo import MongoClient
import typer

app = typer.Typer()

def dict2csv(data, headers, filename, limit=None):
  f = open(filename, 'w', encoding='utf8')
  writer = csv.writer(f, delimiter=',')
  output = sorted(data.items(), key=lambda x: x[1], reverse=True)  
  writer.writerows(output)
  f.close()


@app.command()
def run():
  keywords = {}
  topics = {}
  client = MongoClient()
  db = client['cdicommondata']
  coll = db['opendatasoft']
  n = 0
  total = coll.count_documents({})
  for record in coll.find():
    record = record['record']['dataset']['metas']['default']
    n += 1
    if n % 10000 == 0:
      print('Processed %d of %d (%0.2f%%). Topics %d, keywords %d' % (n, total, n * 100.0/total, len(topics), len(keywords)))      
    if not isinstance(record, dict): continue
    if 'keyword' in record.keys() and record['keyword'] is not None:
      if isinstance(record['keyword'], str):
        k_list = [record['keyword']]
      else:
        k_list = record['keyword']
      for k in k_list:
        v = keywords.get(k, 0)
        keywords[k] = v + 1

    if 'theme' in record.keys() and record['theme'] is not None:
      if isinstance(record['theme'], str):
        k_list = [record['theme']]
      else:
        k_list = record['theme']
      for k in k_list:
        v = topics.get(k, 0)
        topics[k] = v + 1

  dict2csv(topics, ['name', 'value'], '../data/opendatasoft_topics.csv')
  dict2csv(keywords, ['name', 'value'], '../data/opendatasoft_keywords.csv')

if __name__ == "__main__":
  app()