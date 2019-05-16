# A Library for Energy Data Curation and Examination

A web framework and backend for the download, management, processing and analysis for data relating to the operation of the electricity and gas systems of Great Britain.

Incorporating:

- Historical metering data for electricity generation and demand (from the Elexon P114 dataset)
- Balancing Mechanism data relating to power stations, large demand and renewable energy systems
- Physical data describing location, operating parameters and constraints of infrastructure and generating assets
- Renewable generation subsidies

# Requirements
Tested architecture versions shown in brackets
- [Python](https://www.python.org/) (3.7)
- [Django](https://www.djangoproject.com/) (2.1)
- [Postgresql](https://www.postgresql.org/)
- [Psycopg2](http://initd.org/psycopg/)
- [Pandas](https://pandas.pydata.org/) (0.24.0)
- [Django-TQDM](https://pypi.org/project/django-tqdm/) (0.0.3)

Note that for data retrieval the following are required:
- Elexon account with access to BMRA data services - see https://www.elexon.co.uk/guidance-note/bmrs-api-data-push-user-guide/
- Subscription-based access to the Elexon-published P114 data - see https://www.elexon.co.uk/data-flow/settlement-report-saa-i014-also-known-as-the-s0142/

# Documentation
- Installation
- [P114 raw data description](./docs/P114_data_description.md)
- [BMRA raw data description](./docs/BM_data_description.md)
- Database ORM Documentation
- Example [Jupyter](https://jupyter.org/) notebooks
