import requests
import time

# Replace <YOURAPIKEY> with your own Etherscan API key
etherscan_api_key = "YOURAPIKEY"
polygonscan_api_key = "YOURAPIKEY"
# Replace <YOUR-ETHEREUM-ADDRESS> with the Ethereum address you want to check
address = "0x0"
# Replace <YOURSLACKWEBHOOKURL> with the URL of your Slack webhooka
webhook_url = "YOURSLACKWEBHOOKURL"

inactive_threshold = 1200


### Etherscan API call to get last transactions.
response = requests.get(f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={etherscan_api_key}")
data = response.json()

### [MATIC ERC20]
response = requests.get(f"https://api.polygonscan.com/api?module=account&action=txlist&address={address}&sort=desc&apikey={polygonscan_api_key}")
matic_data = response.json()

##### First tx (most recent) & Timestamp get
eth_last_transaction = data['result'][0]
polygon_last_transaction = matic_data['result'][0]
last_transaction_timestamp = int(last_transaction['timeStamp'])

##### Time difference.
time_difference = time.time() - last_transaction_timestamp

# Final checking.
if time_difference > inactive_threshold:
  requests.post(webhook_url, json={
    "text": f"The last transaction for address {address} was more than {inactive_threshold/60} minutes ago!",
  })
