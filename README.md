# lowcygier
web scraper 

## Prerequsite

1. Install all dependecies:
`pip install -r requirements`
2. setup `config.cfg`:
```
[telegram]
id=
token=
```
3. provide correct path in `start.sh`:
```bash
#!/bin/bash

cd <provide correct full path to src folder> 
source ./env/bin/activate >> /tmp/asdf.log 2>&1
./lab_project.py >> /tmp/asdf.log 2>&1
```
4. add job to cron:
`crontable -e`
```bash
# m h  dom mon dow   command
*/30 * * * * /home/m/LINUX2020/webscraper/lab/start.sh
```

