#!/usr/bin/env bash

## Author: Hyecheol (Jerry) Jang
## Shell script to generate cloudflare.config

# Prompt to get API token
echo "Need Cloudflare API Token with Zone:Read and DNS:Edit Permission"
echo "Please go to Cloudflare Website and Issue API Token and paste below"
echo -e "More Information: https://bit.ly/30HY0C3 \n"
read -p 'Paste API Token here: ' apiToken # Get API Token

# Validate API Token
validToken=$(curl -s -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" \
                      -H "Authorization: Bearer $apiToken" \
                      -H "Content-Type:application/json" | jq .success)
while [ $validToken != "true" ]; do
  echo -e "Token Invalid, Please Double Check and Enter Token Agian \n"
  read -p 'Paste API Token here: ' apiToken # Get API Token
  validToken=$(curl -s -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" \
                      -H "Authorization: Bearer $apiToken" \
                      -H "Content-Type:application/json" | jq .success)
done
echo "Token Valid!!"
unset validToken

# Get all zones associated with the account
apiCall=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones?per_page=50" \
                  -H "Authorization: Bearer $apiToken" \
                  -H "Content-Type: application/json")
if [ $(echo $apiCall | jq .success) != true ]; then # Error Checking
  echo "API call Failed. This may caused by either cloudflare's API server error or poor connectivity of your server"
  echo "Please try again later"
  exit
fi
zoneCount=$(echo $apiCall | jq .result_info.count)

# Get Zone ID
zoneIDs=()
index=0
while [ $index -lt $zoneCount ]; do
  zoneIDs+=($(echo $apiCall | jq -r .result[$index].id ))
  index=$[$index+1]
done
unset zoneCount
unset index
unset apiCall

# Retrieve A records update target
updateTarget=""
count=0
echo -e "\ntype \"y\" for the DNS entry you want to enable dynamic ip update"
echo -e "Otherwise, type \"n\"\n"
for zoneID in ${zoneIDs[@]}; do
  apiCall=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$zoneID/dns_records?type=A" \
                    -H "Authorization: Bearer $apiToken" \
                    -H "Content-Type: application/json" | jq .)

  if [ $(echo $apiCall | jq .success) != true ]; then # Error Checking
    echo "API call Failed. This may caused by either cloudflare's API server error or poor connectivity of your server"
    echo "Please try again later"
    exit
  fi

  # Extract records that want to update
  recordCount=$(echo $apiCall | jq .result_info.count)
  index=0
  while [ $index -lt $recordCount ]; do
    # display record name and prompt
    echo $(echo $apiCall | jq -r .result[$index].name )
    while :; do
      read -r -p "Want to update? [y/n]: " response
      case "$response" in
        [yY])
          updateTarget=$updateTarget","$(echo "{\"name\": $(echo $apiCall | jq .result[$index].name), \"id\": $(echo $apiCall | jq .result[$index].id), \"zone_id\": $(echo $apiCall | jq .result[$index].zone_id)}" | jq .)
          count=$[$count+1]
          echo -e "Add to update target\n"
          break
          ;;
        [nN])
          echo -e "Skipped\n"
          break
          ;;
        *)
          echo "Invalid Input, Select Again"
          ;;
      esac
    done

    index=$[$index+1]
  done
done
unset response
unset zoneID
unset apiCall
unset recordCount
unset index

# Write JSON File
echo $(echo "{\"api\": \"$apiToken\", \"update-target\": ["${updateTarget:1}"]}" | jq .) > config.json
echo "Config file saved as config.json"
echo $count" DNS record will updated"

unset updateTarget
unset apiToken
unset count
