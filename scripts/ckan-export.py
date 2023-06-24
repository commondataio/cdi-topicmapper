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
  db = client['ckan']
  coll = db['dataset']
  n = 0
  total = coll.count_documents({})
  for record in coll.find():
    record = record['record']    
    n += 1
    if n % 10000 == 0:
      print('Processed %d of %d (%0.2f%%). Topics %d, keywords %d' % (n, total, n * 100.0/total, len(topics), len(keywords)))        
    if not isinstance(record, dict): continue
    if 'tags' in record.keys() and record['tags'] is not None:
      k_list = record['tags']
      for k in k_list:
        name = k['display_name'] if 'display_name' in k.keys() else k['name']
        v = keywords.get(name, 0)
        keywords[name] = v + 1
    if 'groups' in record.keys() and record['groups'] is not None:
      k_list = record['groups']
      for k in k_list:
        name = k['display_name'] if 'display_name' in k.keys() else k['name']
        if isinstance(name, str):
          v = topics.get(name, 0)
          topics[name] = v + 1

  dict2csv(topics, ['name', 'value'], '../data/ckan_topics.csv')
  dict2csv(keywords, ['name', 'value'], '../data/ckan_keywords.csv')

if __name__ == "__main__":
  app()