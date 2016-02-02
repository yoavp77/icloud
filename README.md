# icloud

#
# icloudbattery.py
check the battery level on all your icloud devices and text (or email) yourself a reminder to charge them.
requires redis for caching to ensure you dont spam yourself.

the config file looks like this:
{"iclouduser@me.com": ["PASSWORD", "mobile_number@carrier.com"] }

