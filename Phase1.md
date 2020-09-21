# Milestone 1

## Web-Scraping
A scrapy project which scrapes the manufacturer sites for SDSs and save the scraped files in database.

### Steps
1. Develop initial scrapers for all the provided manufacturer.
2. Identify common flows and techniques in all the scrapers.
3. Implement a base class of spiders for drived specialized spiders to inherit and customize for particular manufacturer. 

# Milestone 2

## Web-Application
A django web-application which will implement a relational database models to hold the data of manufacturers and scraped items.

### Steps
1. Identify and define the relational database models to hold the data scraped.
2. Normalize or De-normalize according to the performance requirements.
3. Implement a Django API and management commands to post the data scraped.
4. Implement an admin panel to search and filter the data and perform common actions.

# Resources

## Server Setup
Setup a linux server to host the django web application and to run scrapers.

### Specifications
- OS: Ubuntu >= 18.4
- RAM: 16 GB
- CPU: 4
- Network Bandwidth: > 8 GiB
- Disk Space: 512 GB (For Now)
- Database Server: MariaDB

## Developers:
Two developers will be assigned to the project.

1. M Junaid Ikhlaq (30 hours/week)
2. Rafay Javed     (30 hours/week)
