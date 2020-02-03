#!/bin/bash

source ./getbinancedataconfig.sh

for n in {1..60}; do
  for pair in $pairs; do
    timestamp=$(date "+%Y.%m.%d-%H.%M.%S.%N")
    depthfilename=$datafolder'/'depth$pair$timestamp
    echo retrieving $timestamp $pair
    #get the order book/depth of the pair
    curl -sH "X-MBX-APIKEY: $binanceapikey" -X GET 'https://api.binance.com/api/v3/depth?symbol='$pair >$depthfilename &

    aggtradesfilename=$datafolder'/'aggtrades$pair$timestamp
    #get the last 500 trades aggregated
    curl -sH "X-MBX-APIKEY: $binanceapikey" -X GET 'https://api.binance.com/api/v3/aggTrades?symbol='$pair >$aggtradesfilename &

    #get the last 500 trades
    #curl -H "X-MBX-APIKEY: $binanceapikey" -X GET 'https://api.binance.com/api/v3/aggTrades?symbol='$pair
  done
  sleep 1
done
