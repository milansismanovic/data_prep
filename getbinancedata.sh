#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
source $DIR/config
date_name=$(date '+%Y.%m.%d')
echo putting data to $datafolder'/'$date_name
mkdir -p $datafolder'/'$date_name
for n in {1..60}; do
  for pair in $pairs; do
    timestamp=$(date "+%Y.%m.%d-%H.%M.%S.%N")
    depthfilename=$datafolder'/'$date_name'/'depth$pair$timestamp'.json'
    echo retrieving $timestamp $pair
    #get the order book/depth of the pair
    curl -sH "X-MBX-APIKEY: $binanceapikey" -X GET 'https://api.binance.com/api/v3/depth?symbol='$pair >$depthfilename &

    aggtradesfilename=$datafolder'/'$date_name'/'aggtrades$pair$timestamp'.json'
    #get the last 500 trades aggregated
    curl -sH "X-MBX-APIKEY: $binanceapikey" -X GET 'https://api.binance.com/api/v3/aggTrades?symbol='$pair >$aggtradesfilename &

    #get the last 500 trades
    #curl -H "X-MBX-APIKEY: $binanceapikey" -X GET 'https://api.binance.com/api/v3/aggTrades?symbol='$pair
  done
  sleep 1
done
