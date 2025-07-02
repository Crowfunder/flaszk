# How to schedule regular synchronization (and indexing) with Cron
Scheduled and regular synchronization and indexing are not supported by the application right now, but it can be realised with **Cron**.

## Step 1: Create a Script
The first step will be creating a script that conducts the task of running synchronization. All the script needs to do is basically invoke an appropriate client endpoint. 

The script should be placed in a known directory, save its path. Example below.
#### /home/user/.bin/sync.sh 
```sh
#!/bin/bash
PORT = '5000'

# Sync with remotes
curl -sSL 'http://127.0.0.1:$PORT/client/sync/all'

# Regenerate index of local documents
# WARNING: May be lengthy, it may not be necessary
#          to run it as often as syncing.
curl -sSL 'http://127.0.0.1:$PORT/client/index'
```
Make sure to run `chmod +x` on it to make it executable!

## Step 2: Open your Cron Tab
To start editing your Cron Tab, run the following command:
```sh
crontab -e
```

## Step 3: Create a Cron Job
Add a line with schedule of running your script. Below example of a job, for exact cron job format documentation google it.
```sh
30 * * * * /home/user/.bin/sync.sh > /dev/null 2>&1 
```
This job will run out sync script every hour, at 30 minutes mark, and redirect the output to /dev/null (no output).


