# Safety Data Sheet Store
This system is meant to collect, manipulate and serve the Safety Data Sheets from palanthora of manufacturers and providers.

## Proposed Stack:
- Scrapy / ScrapyD
- Django
- MariaDB

## Scrapy
We will be using the `scrapy` framework for implementing the web-scraping modules for each SDS source site.
The Extract Transform Load (ETL) pipelines will also be rewritten in scrapy. 

The following are the proposed pipelines:

### Relevant Text Extractor
This pipeline will be responsible for extracting the relevant area of SDS.

### Product Extractor
This pipeline will be responsible for extracting the product name form the SDS and will be customizable in terms of constants and techniques used for extraction i.e. regex and ordering.

### Manufacturer Extractor
This pipeline will be responsible for extracting the manufacturer name from the SDS and will be customizable in terms of constants and techniques used for extraction i.e. regex and ordering.

### Hazard-Code Extractor
This pipeline will be responsible for extracting the hazard-codes from `Section 2` of the SDS and will be customizable in terms of constants and techniques used for extraction i.e. regex and ordering.

### Revision Date Extractor
This pipeline will be responsible for extracting the raw revision date based on the strategy specified by an individual spider class. This raw revision date will be cleaned and formatted in `Date Extractor and Formatter Pipeline`.

### Published Date Extractor
This pipeline will be responsible for extracting the raw published date based on the strategy specified by an individual spider class. This raw published date will be cleaned and formatted in `Date Extractor and Formatter Pipeline`.

### Print Date Extractor
This pipeline will be responsible for extracting the raw print date based on the strategy specified by an individual spider class. This raw print date will be cleaned and formatted in `Date Extractor and Formatter Pipeline`.

### Previous Date Extractor
This pipeline will be responsible for extracting the raw previous date based on the strategy specified by an individual spider class. This raw previous date will be cleaned and formatted in `Date Extractor and Formatter Pipeline`.

### Date Extractor and Formatter
This pipeline will be responsible for extracting dates and converting it to the standard format i.e. `dd.mm.yyyy` from raw dates in each of date field.


## Django
Django will be used to implement the relational database models, required schedule tasks and any management commands that will be used in our system.
The website will use the maria-db backend to interact with the database.

### Admin Panel:
We will also provide an admin panel to sort of manage and manually check and update the extracted data based on django.

## Maria DB
The system will use Maria DB server as main Database Server.

## Relational Model:
Following is the relational model of the database:
 
![](db_design%20v02.png)
