#!/usr/bin/python
#
# check the battery level on all your icloud devices and text (or email) yourself a reminder to charge them.
# requires redis for caching to ensure you dont spam yourself.
# 
# the config file looks like this:
# {"iclouduser@me.com": ["PASSWORD", "mobile_number@carrier.com"] }
#

import smtplib
import sys
import redis
import datetime
from pyicloud import PyiCloudService
import json

# check for the existence of a key in redis
def check_cache(key):
  r = redis.StrictRedis(host='localhost', port=6379, db=0)
  if ( r.get(key) == None): 
    rc = False
  else:
    rc = True
  return (rc)

# set a key in redis
def set_cache(key):
  r = redis.StrictRedis(host='localhost', port=6379, db=0)
  value = r.set(key, int(datetime.datetime.now().strftime("%s")) * 1000)

# delete a key from redis
def del_cache(key):
  r = redis.StrictRedis(host='localhost', port=6379, db=0)
  r.delete(key)

def mail_out(address, msg):
  server = smtplib.SMTP('localhost')
  server.set_debuglevel(0)
  server.sendmail('user@example.com', address, msg)
  server.quit()

# check all icloud devices
def check_icloud():
  # credentials 
  with open('/etc/.icloud/settings') as data_file:    
    credentials = json.load(data_file)
  # iterate over devices in this account
  for user, settings in credentials.iteritems():
    # api into icloud
    api = PyiCloudService(user, settings[0])
    # iterate over devices
    for device in api.devices:
      # store battery level
      battery_level = device.status()['batteryLevel'] * 100
      # check for low battery devices
      if battery_level < 20:
        # check for existing cache entry - send an email and create one if it's missing
        if (not check_cache(device.status()['deviceDisplayName'])):
          set_cache(device.status()['deviceDisplayName'])
          mail_out(settings[1],device.status()['deviceDisplayName'] + ' battery ' + str(battery_level) + '%')
      # if the battery is good - clear cache entry if one exists
      else:
        if (check_cache(device.status()['deviceDisplayName'])):
          del_cache(device.status()['deviceDisplayName'])
  
if __name__ == '__main__':
  check_icloud()
