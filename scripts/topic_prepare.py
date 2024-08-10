import sys
import csv
import os
import typer
import json
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


app = typer.Typer()


def load_rules(filename):
    rules = {}  
    f = open(filename, 'r', encoding='utf8')
    data = yaml.load(f, Loader=Loader)            
    f.close()
    for item in data:
        rules[item['key']] = item
    return rules



@app.command()
def run():    
    geo_rules = load_rules('../reference/rules_geo.yaml')
    data_rules = load_rules('../reference/rules_data_theme.yaml')
    out = open('../refined/prepared_original_topics.jsonl', 'w', encoding='utf8')
    outcsv = open('../refined/prepared_original_topics.csv', 'w', encoding='utf8')
    writer = csv.DictWriter(outcsv, fieldnames=['topic', 'c', 'data_rules', 'geo_rules'])
    writer.writeheader()
    f = open('../data/index_dumps/original_topics_20240810.jsonl', 'r', encoding='utf8')
    for line in f:
        item = json.loads(line)
        if item['topic'] in data_rules.keys():
            item['data_rules'] = '|'.join(data_rules[item['topic']]['topics'])
        if item['topic'] in geo_rules.keys(): 
           item['geo_rules'] = '|'.join(geo_rules[item['topic']]['topics'])
        out.write(json.dumps(item) + '\n')
        writer.writerow(item)
    out.close()
    f.close()


if __name__ == "__main__":
  app()