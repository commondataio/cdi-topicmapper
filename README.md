# cdi-topicmapper
Open data topics mapping experiments, code and data

This repository is the part of the Common Data Index project (https://github.com/commondataio)

This repository includes data dumps from Common Data Index database with frequency lists of themes and keywords.

Data dumped as csv files with field names and count of occurences to 'data' directory.

Code as added to the 'scripts' directory. 


## Possible solutions

### Double/Triple classification

Geodata themes from EN ISO 19115 https://inspire.ec.europa.eu/metadata-codelist/TopicCategory and EU Data Themes https://op.europa.eu/en/web/eu-vocabularies/concept-scheme/-/resource?uri=http://publications.europa.eu/resource/authority/data-theme
Scientific themes could be taken from Re3Data schema

Advantages: Sync with Data.europe.eu and European data portals
Disadvantages: A lot of datasets not covered by both classifications


### Datacite / Re3Data subjects

http://schema.re3data.org/3-1/re3dataV3-1.xsd



### Custom theme reference list

Create custom themes reference list after keywords and topics analysis. 


## Other links
* Harvard Dataverse https://dataverse.harvard.edu/


## General approach

1. Select most common topics and create simplified list of topics
2. Add mapper from reference topics to original themes and keywords
3. Create simple Python function to identify topic by themes or keywords provided


