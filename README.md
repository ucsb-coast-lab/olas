# olas
## Tweeter for Spot Buoy 
Twitter Account: https://twitter.com/ucsb_buoy

### Server Deployment
This application is currently being run on the UCSB ERI server. The server runs the command in the unix file at 7 AM, 10 AM, 1 PM and 4 PM. 
To make updates: 
- Connect to UCSB VPN with Pulse Secure
- run
  - `ssh coastlab@sylk.eri.ucsb.edu`
  - Use the password for the Coast Lab ERI functional account(This can be obtained from a Coast Lab admin)
- Once logged in navigate to the OceanReport directory by running `cd ../coast/ocean-report/olas`
- Making changes to any of the files as needed and test if the functionality still works
- Push all changes to master and the server will run the code at the correct times

### Version History
- 10/28/2019: Draft code for a detailed tweet using the latest wave data. 
- 10/29/2019: This was successful yesterday. Modified today for emojis. 
- 11/7/2019: Fixed tide predictions to return beyond a calendar day.
- 11/11/2019: Added file paths so to facilitate calling as a script
- 3/11/2020: Organized into function definitions and main function and Created GitHub Repo 

### Crontab 
- 00 7 * * * python3 /home/pi/olas/olas_v1.1.py >> ~/olas/cron.log 2>&1
- 00 10 * * * python3 /home/pi/olas/olas_v1.1.py >> ~/olas/cron.log 2>&1
- 00 13 * * * python3 /home/pi/olas/olas_v1.1.py >> ~/olas/cron.log 2>&1
- 00 16 * * * python3 /home/pi/olas/olas_v1.1.py >> ~/olas/cron.log 2>&1

### Credentials and Tokens
- The twitter credentials should be in the root directory in a file called twitter_credentials.json. The information should be formatted as follows:
`{"CONSUMER_KEY": "YOUR KEY", "CONSUMER_SECRET": "YOUR SECRET", "ACCESS_TOKEN": "YOUR TOKEN", "ACCESS_SECRET": "YOUR SECRET"}`

- The spotter api token should also be in the root directory in a file called spot_token.json. The information should be formatted as follows: 
`{"SPOT_TOKEN" : "YOUR SPOTTER TOKEN"}`
