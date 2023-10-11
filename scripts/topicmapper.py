import json
import csv
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


import typer


app = typer.Typer()

MAPPER_FILE = '../refined/prepared.csv'
DATA_THEMES_FILE = '../reference/data_themes.yaml'
ISO19115_FILE = '../reference/iso19115.yaml'
RULES_THEME_FILE = '../reference/rules_data_theme.yaml'
RULES_GEO_FILE = '../reference/rules_geo.yaml'


@app.command()
def convert():
    """Convert mapped data to yaml rules"""
    themes = {}
    f = open(DATA_THEMES_FILE, 'r', encoding='utf8')
    themes_data = yaml.load(f, Loader=Loader)
    f.close()
    for row in themes_data:
        print(row)
        themes[row['id']] = row['name']

    data_geo = []
    data_theme = []
    texts = []
    f = open(MAPPER_FILE, 'r', encoding='utf8')
    reader = csv.DictReader(f, delimiter=',') 
    for row in reader:
        print(row)
        text = row['Name']
        if len(row['Data theme']) > 0:
            parts = row['Data theme'].split(',')
            record = {'key': text, 'topics' : []}
            for part in parts:
                record['topics'].append(themes[part])
            data_theme.append(record)
        if len(row['EN ISO 19115']) > 0:
            parts = row['EN ISO 19115'].split(',')
            record = {'key': text, 'topics' : []}
            for part in parts:
                record['topics'].append(part)
            data_geo.append(record)
    f.close()
    f = open(RULES_THEME_FILE, 'w', encoding='utf8')
    f.write(yaml.dump(data_theme, Dumper=Dumper))
    f.close()
    f = open(RULES_GEO_FILE, 'w', encoding='utf8')
    f.write(yaml.dump(data_geo, Dumper=Dumper))
    f.close()

@app.command()
def identify(text):
    """Identifies license by text provided. Very slow and ineffective. Temporary solution test license mapping for Common Data Index"""
    themes= {}
    f = open(RULES_THEME_FILE, 'r', encoding='utf8')
    themes_data = yaml.load(f, Loader=Loader)
    f.close()
    for row in themes_data:
        themes[row['key']] = row['topics']

    geo = {}
    f = open(RULES_GEO_FILE, 'r', encoding='utf8')
    geo_data = yaml.load(f, Loader=Loader)
    f.close()
    for row in geo_data:
        geo[row['key']] = row['topics']
    

    notfound = True
    if text in themes.keys():
       print('Topics for text %s: %s' % (text, ','.join(themes[text])))
       notfound = False    
    if text in geo.keys():
       print('Geo topics for text %s: %s' % (text, ','.join(geo[text])))
       notfound = False    
    if notfound:
       print('Topics not found')

if __name__ == "__main__":
    app()