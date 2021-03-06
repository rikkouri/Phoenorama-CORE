'''
Created on Mar 17, 2012

@author: r00tme
'''
# List of modules to import when celery starts.
CELERY_IMPORTS = ("scanner.openvas.tasks", "scanner.nmap.tasks")

## Result store settings.
CELERY_RESULT_BACKEND = "amqp"
#CELERY_RESULT_DBURI = "sqlite:///mydatabase.db"

## Broker settings.
#BROKER_URL = "amqp://guest:guest@localhost:5672//"
BROKER_URL = "amqp://guest:guest@phoenorama.org:5672//"
#BROKER_URL = "amqp://guest:guest@10.0.1.16:5672//"

## Worker settings
## If you're doing mostly I/O you can have more processes,
## but if mostly spending CPU, try to keep it close to the
## number of CPUs on your machine. If not set, the number of CPUs/cores
## available will be used.
#CELERYD_CONCURRENCY = 10

#CELERY_ANNOTATIONS = {"tasks.add": {"rate_limit": "10/s"}}

CELERY_DISABLE_RATE_LIMITS = True