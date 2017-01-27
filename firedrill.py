#!/usr/local/bin/python

import requests, urllib, urllib2, sys, json, time, subprocess, re, base64, os

slack_channel = os.environ.get('SLACK_CHANNEL')
webhook_url   = os.environ.get('WEBHOOK_URL')
rancher_url   = str(os.environ.get('RANCHER_URL'))
rancher_access_key = os.environ.get('RANCHER_ACCESS_KEY')
rancher_secret_key = os.environ.get('RANCHER_SECRET_KEY')  
alert_time         = os.environ.get('ALERT_TIME')

# NOTES:
# python firedrill.py

# Return a list of containers with label 
def get_containers():

    containerData = None

    try:
        url = "https://" + rancher_url  + "/v1?limit=1000"
        print url

        passman  = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, rancher_access_key, rancher_secret_key)
        urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))

        req      = urllib2.Request(url)
        response = urllib2.urlopen(req)

        html     = response.read()
        jsonObj  = json.loads(html) 

        url = "https://" + rancher_url + "/v1/containers?limit=1000"

        passman  = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, rancher_access_key, rancher_secret_key)
        urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))

        req      = urllib2.Request(url)
        response = urllib2.urlopen(req)
        html     = response.read()

        containerData  = json.loads(html) 

        degradedArr = []
        data = None

        for container in containerData['data']:
            if container['state'] == "stopped" and (container['transitioning'] != "yes") and not ('io.rancher.container.system' in container['labels']):
                data = {}
                host_data  = get_host_data(container['links']['hosts'])

                hostname   = host_data['hostname']
                data['hostname'] = hostname

                ip_address = host_data['publicEndpoints'][0]['ipAddress']
                data['ip'] = ip_address

                host_id    = container['hostId']
                data['host-id'] = host_id

                image_id        = container['imageUuid']
                data['image_id'] = image_id

                service_name = container['labels']['io.rancher.stack_service.name']
                data['service_name'] = '*' + service_name + '*'

                print "CONTAINER FOUND IN DEGRADED STATE!!" + str(data)
                print "WARNING SLACK!" + slack_channel

                degradedArr.append(data)

        if len(degradedArr) > 0:
            post_slack(degradedArr, slack_channel)

    except subprocess.CalledProcessError as e:
        print e.output


def get_host_data( link ):
    passman  = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, link, rancher_access_key, rancher_secret_key)
    urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))

    req      = urllib2.Request(link)
    response = urllib2.urlopen(req)
    html     = response.read()

    hostData = json.loads(html) 

    return hostData['data'][0]
 

def post_slack( degraded_arr, slack_channel ):
    #data = json.dumps(degraded_arr)
    url  = webhook_url

    payload = {
        "username": "rancher-alerts",
        "text": json.dumps(degraded_arr), #message you want to send
        "channel": slack_channel #Channel set above
    }

    req = requests.post(webhook_url, json.dumps(payload), headers={'content-type': 'application/json'}) #request to post the message


def main():
    # Continually iterate and do your thing:
    while 1:

        print "URL: " + rancher_url
        print "another iteration..."

        # change this into an argument in the future to slow the pace of processing.
        get_containers()
        time.sleep(int(alert_time))

if __name__ == "__main__":
    main()

