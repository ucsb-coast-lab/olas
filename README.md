# olas
## Tweeter for Spot Buoy

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

