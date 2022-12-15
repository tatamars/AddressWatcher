import requests
import time

# Replace <YOUR-API-KEY> with your own Etherscan API key
api_key = "YOUR-API-KEY"
# Replace <YOUR-ETHEREUM-ADDRESS> with the Ethereum address you want to check
address = "0x993D89343035F703172451Bf426A3A52eB1F7cdF"
# Replace <YOUR-SLACK-WEBHOOK-URL> with the URL of your Slack webhook
webhook_url = "YOUR-SLACK-WEBHOOK-URL"



### Etherscan API call to get last transactions.
response = requests.get(f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={api_key}")
data = response.json()

##### First tx (most recent) & Timestamp get
last_transaction = data['result'][0]
last_transaction_timestamp = int(last_transaction['timeStamp'])

##### Time difference.
time_difference = time.time() - last_transaction_timestamp

# Final checking.
if time_difference > 600:
  requests.post(webhook_url, json={
    "text": f"The last transaction for address {address} was more than 10 minutes ago!",
  })
