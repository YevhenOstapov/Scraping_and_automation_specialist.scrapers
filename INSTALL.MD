### 1. Create .env file on base directory
>  next to the conf.py file, create an .env file
> :warning: **Required!**
```text
    .
    ├── ...
    ├── scraping_and_automation_specialist   # Base dir
    │   ├── google_data_manager        
    │   │   └── ...      
    │   ├── scheduling
    │   │   └── ...
    │   ├── scrapers
    │   │   ├── credentials.json
    │   │   └── ...
    │   ├── static
    │   │   └── ...
    │   ├── .env    # <<<     
    │   ├── .env-example          
    │   ├── conf.py
    │   ├── utils.py
    │   ├── docker-compose-dev.yml
    │   ├── Dockerfile
    │   └── ...
    └── ...
```
>###### Populate with example from .env-example file
---
### 2. Add a credentials.json file for google authorization inside the static directory if it's not there
[Google Sheets API docs](https://developers.google.com/sheets/api/reference/rest)
--
[Create credentials file](https://developers.google.com/workspace/guides/create-credentials)
--
---
### 3. Docker
Up docker containers
```commandline
$ docker-compose -f docker-compose-dev.yml up -d --build
```
Down docker containers with deleting all images and volumes
```commandline
$ docker-compose -f docker-compose-dev.yml down -v --rmi "all"
```
Docker logs
```commandline
$ docker scheduling logs -f
```
Run tasks
```commandline
$ docker-compose -f docker-compose-dev.yml exec scheduling celery shell
```
```shell
Python 3.9.12 (main, Apr 20 2022, 01:56:56) 
[GCC 10.3.1 20211027] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from scheduling.tasks import run
>>> run.delay()
<AsyncResult: d3a1b56c-e4b3-40ef-816a-902f90f31733>
>>>
```
After running the task, the logs should look like this 
```text
[2022-04-20 08:17:49,646: WARNING/ForkPoolWorker-9] Started data checker
[2022-04-20 08:17:49,646: WARNING/ForkPoolWorker-1] Start scrapper task
[2022-04-20 08:17:49,647: WARNING/ForkPoolWorker-9] 

[2022-04-20 08:17:49,647: WARNING/ForkPoolWorker-1]  
[2022-04-20 08:17:50,659: WARNING/ForkPoolWorker-1] Total count of products on start: 
[2022-04-20 08:17:50,659: WARNING/ForkPoolWorker-1]  
[2022-04-20 08:17:50,659: WARNING/ForkPoolWorker-1] 395
[2022-04-20 08:17:50,659: WARNING/ForkPoolWorker-1]  
```
---
#### GOOD LUCK
