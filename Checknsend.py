import requests
import time

# Replace <YOUR-API-KEY> with your own Etherscan API key
eth_api_key = "replacehere"
matic_api_key = "replacehere"
# Replace <YOUR-ETHEREUM-ADDRESS> with the Ethereum address you want to check, might be the same for Polygon considering EVM like ecosysstem. 
address = "eth_address"
tron_address = "tron_address"
# Replace <YOUR-SLACK-WEBHOOK-URL> with the URL of your Slack webhooka
webhook_url = "SLACKwebhook"

inactive_threshold = 1200 #seconds




### [ERC20] Etherscan API call to get last transactions.
response = requests.get(f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={eth_api_key}")
eth_data = response.json()
##### First tx (most recent) & Timestamp get
eth_last_transaction = eth_data['result'][0]
eth_last_transaction_timestamp = int(eth_last_transaction['timeStamp'])
##### Time difference.
eth_time_difference = time.time() - eth_last_transaction_timestamp


### [MATIC ERC20]
response = requests.get(f"https://api.polygonscan.com/api?module=account&action=txlist&address={address}&sort=desc&apikey={matic_api_key}")
matic_data = response.json()
matic_last_transaction = matic_data['result'][0]
matic_last_transaction_timestamp = int(matic_last_transaction['timeStamp'])
matic_time_difference = time.time() - matic_last_transaction_timestamp


### TRON & TRC20
## suggestion: what about using timedifference[n] for each hw?
response2 = requests.get(f"https://api.trongrid.io/v1/accounts/{tron_address}/transactions")
tron_data = response2.json()
tron_last_transaction = tron_data['data'][0]
tron_last_transaction_timestamp = (int(tron_last_transaction["block_timestamp"]))/1000
tron_time_difference = time.time() - tron_last_transaction_timestamp

# Final checking.

def watcher(currency, time_difference, watcher_address):
  if time_difference > inactive_threshold:
    requests.post(webhook_url, json={
      "text": f"The last {currency} transaction for address {watcher_address} was more than {inactive_threshold/60} minutes ago!",
    })

watcher("eth", eth_time_difference, address)
watcher("matic", matic_time_difference, address)
watcher("tron", tron_time_difference, tron_address)
