# rancher-firedrill

## Set the following environment variables:

```
slack_channel = os.environ.get('SLACK_CHANNEL')
webhook_url   = os.environ.get('WEBHOOK_URL')
rancher_url   = os.environ.get('RANCHER_URL')
rancher_access_key = os.environ.get('RANCHER_ACCESS_KEY')
rancher_secret_key = os.environ.get('RANCHER_SECRET_KEY')  
alert_time         = os.environ.get('ALERT_TIME')
```

* `ALERT_TIME` - the time (in seconds) to alert; ie how often the firedrill.py script makes an iteration.

## Build it:
  * `make build`

## Deploy it:
  * `make rancher_deploy`

---

## Notes:

* To curl raw webhook integration via an HTTP POST:
  * `curl -X POST --data-urlencode 'payload={"channel": "#container-reporting", "username": "Rancher", "text": "Real time alerts.", "icon_emoji": ":rancher:"}' https://hooks.slack.com/services/UUID/UUID`

