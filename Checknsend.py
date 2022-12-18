import requests
import time

# Replace <YOUR-API-KEY> with your own Etherscan API key
eth_api_key = ""
matic_api_key = ""
# Replace <YOUR-ETHEREUM-ADDRESS> with the Ethereum address you want to check
address = ""
tron_address = ""
# Replace <YOUR-SLACK-WEBHOOK-URL> with the URL of your Slack webhooka
webhook_url = ""

inactive_threshold = 1200 #seconds

# base functions
def get_last_tx_timestamp(response, timestamp_key, subkey):
  last_transaction = response[subkey][0]
  last_transaction_timestamp = int(last_transaction[timestamp_key])
  return last_transaction_timestamp

def check_inactivity(currency, time_difference, watcher_address):
  if time_difference > inactive_threshold:
    requests.post(webhook_url, json={
      "text": f"The last {currency} transaction for address {watcher_address} was more than {inactive_threshold/60} minutes ago!",
    })

# Final checking:

with requests.Session() as session:
  # Etherscan API call to get last Ethereum transactions
  eth_response = session.get(f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={eth_api_key}&type=send")
  eth_timestamp = get_last_tx_timestamp(eth_response.json(), 'timeStamp', 'result')
  eth_time_difference = int(time.time() - eth_timestamp)
  check_inactivity("eth", eth_time_difference, address)
  
  # Matic API call to get last Matic transactions
  matic_response = session.get(f"https://api.polygonscan.com/api?module=account&action=txlist&address={address}&sort=desc&apikey={matic_api_key}&type=send")
  matic_timestamp = get_last_tx_timestamp(matic_response.json(), 'timeStamp', 'result')
  matic_time_difference = int(time.time() - matic_timestamp)
  check_inactivity("matic", matic_time_difference, address)

  # Tron API call to get last Tron transactions
  tron_response = session.get(f"https://api.trongrid.io/v1/accounts/{tron_address}/transactions")
  tron_timestamp = get_last_tx_timestamp(tron_response.json(), 'block_timestamp', 'data')
  tron_time_difference = int(time.time() - (tron_timestamp / 1000))
  check_inactivity("tron", tron_time_difference, tron_address)

##testing
print(f'log: Last time since a eth tx: {eth_time_difference} seconds')
print(f'log: Last time since a matic tx: {matic_time_difference} seconds')
print(f'log: Last time since a tron tx: {tron_time_difference} seconds')
