
# coding: utf-8

# # Wave buoy tweet
# 
# 10/28/2019: Draft code for a detailed tweet using the latest wave data. 
# 
# 10/29/2019: This was successful yesterday. Modified today for emojis. 
# 
# 11/7/2019: Working to fix tide predictions. Right now we only can get a calendar day--not the next 24 hours.

# In[1]:



# Set the shell to show all output, instead of last result
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

def convertTheta_to_Cardinal(theta):
    if (theta >= 45 and theta < 135):
        direction = 'east'
    elif (theta >= 135 and theta < 225):
        direction = 'south'
    elif (theta >= 225 and theta < 315):
        direction = 'west'
    else:
        direction = 'north'
    return direction


# In[2]:


spotID = 'SPOT-0186'

import requests       # For grabbing data via API
import json           # For parsing strings in json format
from datetime import datetime, timedelta, timezone
import pytz


# In[25]:


# We need the current time for placing some observations in context. 
# Also, we'll use 'tomorrow' to get the tide predictions
rightnow = datetime.now(timezone.utc)
tomorrow = rightnow + timedelta(days=1)
print(f'Time: %s:%s' % (rightnow.hour, rightnow.minute))
print(f'Now: {rightnow:%Y}{rightnow:%m}{rightnow:%d}')
print(f'tomorrow: {tomorrow:%Y}{tomorrow:%m}{tomorrow:%d}')


# #### Get recent wave data from a SPOTTER.

# In[39]:


# Recent Wave data from the SPOTTER. 
# Details for the Sofar API at: https://spotter.sofarocean.com/api

parameters = {'spotterId': spotID, 'limit': '0', 'includeWindData':'true'}
response = requests.get('https://api.sofarocean.com/api/latest-data',
             headers={'token': '58d76bba4b8c64258a3b19bcafa6ff'},
             params=parameters)
latest = response.json()  # parse out json structure
latest = latest['data'] # move down to the wave data we want
#latest
# Parse timestamp
spot_time = datetime.strptime(latest['waves'][-1]['timestamp'][:-1],'%Y-%m-%dT%H:%M:%S.%f')
spot_time = spot_time.replace(tzinfo=timezone.utc)

#spot_utc = pytz.utc.localize(spot_time) ## We already localized in the line above
spot_pst = spot_time.astimezone(pytz.timezone("America/Los_Angeles"))

Hs = latest['waves'][-1]['significantWaveHeight']/0.3048 # Feet
Tp = latest['waves'][-1]['peakPeriod']
theta = latest['waves'][-1]['peakDirection']

windspd = latest['wind'][-1]['speed']
winddir = convertTheta_to_Cardinal(latest['wind'][-1]['direction'])

# Assemble the wind report
if (windspd < 2):
    wind_str = f'\U0001F32C Calm'
else: 
    wind_str = f'\U0001F32C From the {winddir} at {windspd} kts'
    
wind_report = [wind_str]  # brackets let's us add mulitple entries (cells in matlab-speak)


# #### Get a tide prediction from NOAA

# In[40]:


# Details for NOAA tide API at: https://tidesandcurrents.noaa.gov/api/
# This will always return at least four responses. 

parameters = {'station':'9411340',
              'begin_date':'20191107', 
              'end_date':f'{tomorrow:%Y}{tomorrow:%m}{tomorrow:%d}',
              'time_zone':'gmt',  # could be lst_ldt
              'product':'predictions',
              'units':'english',
              'datum':'mllw',
              'application':'UCSB',
              'interval':'hilo',
              'format':'json'}
response = requests.get('https://tidesandcurrents.noaa.gov/api/datagetter',
             params=parameters)
tide = response.json() 

tide


# In[41]:


# Find the next two relevant tides

tide_predictions = [] # This gets expanded later with *tide_predictions
n_pred = 0
for prediction in tide['predictions']:
    pheight = float(prediction['v'])
    prediction_time = datetime.strptime(prediction['t'],'%Y-%m-%d %H:%M')
    prediction_time = prediction_time.replace(tzinfo=timezone.utc)
    fromnow = prediction_time - rightnow
    if (fromnow.days > -1) and (n_pred < 2):
        if (n_pred < 1):
            pnext = pheight

        n_pred = n_pred + 1 # Limit how many predictions we print
        if prediction['type'] == 'L':
            #next_tide = 'LOW'
            next_tide = '\U0001F1F1'
        else: 
            #next_tide = 'HIGH'
            next_tide = '\U0001F1ED'
            
        if (round(fromnow.seconds/3600,1) > 1):
            plural = 's'
        else:
            plural = ''
                
        pt = prediction_time.astimezone(pytz.timezone("America/Los_Angeles"))
        tide_str = f'{next_tide} {pheight:.1f} ft @ {pt:%I}:{pt:%M} {pt:%p}'
        #tide_str = f'The next {next_tide} is predicted to be {pheight:.1f} feet {fromnow.seconds/3600:.0f} hour{plural} from now'
        print(tide_str) # Check it
        # Print for later
        tide_predictions = tide_predictions + [tide_str]
                                                                


# In[42]:


parameters = {'station':'9411340',
              'date':'latest', 
              'time_zone':'gmt', 
              'product':'water_level',
              'units':'english',
              'datum':'mllw',
              'application':'UCSB',
              'format':'json'}
response = requests.get('https://tidesandcurrents.noaa.gov/api/datagetter',
             params=parameters)
noaa_latest = response.json()  

tide_height = float(noaa_latest['data'][0]['v'])
tide_time = datetime.strptime(noaa_latest['data'][0]['t'],'%Y-%m-%d %H:%M')
tide_time = tide_time.replace(tzinfo=timezone.utc)

if (pnext > tide_height):
    tideis =  'and rising'   #'\U0001F4C8'
else:
    tideis = 'and falling'  #'\U0001F4C9' 

tide_age = rightnow - tide_time


# In[43]:


#credits = 'More wave data at https://ucsbcoastlab.org/buoy/'
credits = 'Wave history at https://coastlab.sofarocean.com'
#credits = ''


reports = [
    '',    
    f'\U0000231A {spot_pst:%A}, {spot_pst:%B} {spot_pst.day} at {spot_pst:%I}:{spot_pst:%M} {spot_pst:%p}',
    '',    
    f'\U0001F30A {Hs:.1f} ft @ {Tp:.0f} secs from {theta:.0f}º',
    *wind_report,
    f'\U00003030 {tide_height:.1f} ft {tideis}',
    *tide_predictions,
    '',
    credits]

f = open('latest.txt', 'w')
print('The latest @ucsantabarbara ocean report', *reports, sep="\n",file=f)
f.close()
print('The latest @ucsantabarbara ocean report', *reports, sep="\n")


# In[10]:


# Prep the twitter environment

# Load credentials from json file
with open("./twitter_credentials.json", "r") as file:
    creds = json.load(file)  # Gives you consumer key/secret and access token/secret

import tweepy

# Authenticate to Twitter
auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])

api = tweepy.API(auth)

try:
    test = api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


# In[ ]:


### NOW TWEET IT
if(True):
    with open('latest.txt','r') as f:
        api.update_status(f.read())

