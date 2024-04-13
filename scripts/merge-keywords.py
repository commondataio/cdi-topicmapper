import csv
import sys
import os

FILES = ['ckan_keywords.csv',
'dcat_keywords.csv',
'geonetwork_keywords.csv',
'opendatasoft_keywords.csv',
'udata_keywords.csv',
]

def dict2csv(data, headers, filename, limit=None):
  f = open(filename, 'w', encoding='utf8')
  writer = csv.writer(f, delimiter=',')
  output = sorted(data.items(), key=lambda x: x[1], reverse=True)
  if limit is not None:
    for row in output:
      if row[1] < limit:
          break
      writer.writerow(row)
  else:
    writer.writerows(output)
  f.close()


def run():
  keywords = {}
  for filename in FILES:
    f = open(os.path.join('..','data', filename), 'r', encoding='utf8')
    reader = csv.reader(f, delimiter=',')  
    for row in reader:
       if len(row) != 2: continue
       v = keywords.get(row[0], 0)
       keywords[row[0]] = v + int(row[1])
  dict2csv(keywords, ['name', 'value'], os.path.join('..', 'refined', 'all_keywords.csv'))
  dict2csv(keywords, ['name', 'value'], os.path.join('..', 'refined', 'top_keywords.csv'), limit=1000)
    

if __name__ == "__main__":
    run()