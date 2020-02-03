#!/bin/bash

pairfile=/home/tensor/binance/pairs.txt
#datafolder=/home/tensor/binance/data
#datafolder=/host_shared/binance/data
datafolder=/home/tensor/binance/data

for n in {1..60}; do
  while read pair; do
    timestamp=$(date "+%Y.%m.%d-%H.%M.%S.%N")
    depthfilename=$datafolder'/'depth$pair$timestamp
    echo retrieving $timestamp $pair
    #get the order book/depth of the pair
    curl -sH "X-MBX-APIKEY: frkoQw9fUbbdk3PH2ZzxmkVA7v97AvLcDojMgQGRX9UqWQe3bwzG38U91lE7nXyr" -X GET 'https://api.binance.com/api/v3/depth?symbol='$pair >$depthfilename &

    aggtradesfilename=$datafolder'/'aggtrades$pair$timestamp
    #get the last 500 trades aggregated
    curl -sH "X-MBX-APIKEY: frkoQw9fUbbdk3PH2ZzxmkVA7v97AvLcDojMgQGRX9UqWQe3bwzG38U91lE7nXyr" -X GET 'https://api.binance.com/api/v3/aggTrades?symbol='$pair >$aggtradesfilename &

    #get the last 500 trades
    #curl -H "X-MBX-APIKEY: frkoQw9fUbbdk3PH2ZzxmkVA7v97AvLcDojMgQGRX9UqWQe3bwzG38U91lE7nXyr" -X GET 'https://api.binance.com/api/v3/aggTrades?symbol='$pair
  done <$pairfile
  sleep 1
done
