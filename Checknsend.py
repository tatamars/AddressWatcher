import requests
import time

# Replace <YOUR-API-KEY> with your own Etherscan API key
api_key = "1XY9N68UFK14YAEY6N31N3RT5IVM5DMZIQ"

# Replace <YOUR-ETHEREUM-ADDRESS> with the Ethereum address you want to check
address = "0x993D89343035F703172451Bf426A3A52eB1F7cdF"

# Replace <YOUR-SLACK-WEBHOOK-URL> with the URL of your Slack webhook
webhook_url = "https://hooks.slack.com/services/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"

# Send a request to the Etherscan API to get the last transaction for the specified address
response = requests.get(f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={api_key}")

# Get the response data as a JSON object
data = response.json()

# Get the first (i.e. most recent) transaction from the response data
last_transaction = data['result'][0]

# Get the timestamp of the last transaction, in seconds since the Unix epoch
last_transaction_timestamp = int(last_transaction['timeStamp'])

# Calculate the time difference between the current time and the timestamp of the last transaction
time_difference = time.time() - last_transaction_timestamp

# Check if the time difference is greater than 10 minutes (600 seconds)
if time_difference > 600:
  # If it is, send an alert message to Slack
  requests.post(webhook_url, json={
    "text": f"The last transaction for address {address} was more than 10 minutes ago!",
  })
