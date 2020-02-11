# data_prep
## Input
### Binance Raw Data
the data from Binance looks like this
order book
```
{
  "lastUpdateId": 1027024,
  "bids": [
    [
      "4.00000000",     // PRICE
      "431.00000000"    // QTY
    ]
  ],
  "asks": [
    [
      "4.00000200",
      "12.00000000"
    ]
  ]
}

trades
[
  {
    "id": 28457,
    "price": "4.00000100",
    "qty": "12.00000000",
    "quoteQty": "48.000012",
    "time": 1499865549590,
    "isBuyerMaker": true,
    "isBestMatch": true
  }
]
```
## Output
### Binance Normalization
features
```
time
bids 100
asks 100
aggtrades 100
historic data now,3s,30s,1m,5m,10m,...60m,1h,24h,7d,30d,1y
spread min(asks) - max(bids)

target
stddev last 3 days for the range
future 3s price difference within the stddev range


normalization
fx pair normalizaion to min,max 1 year +/-10%
```

which fx pairs
most liquid pairs:
```
pair		volume
BTC/USDT	255
BCH/USDT	55
ETH/USDT	39
----
ETC/USDT	29
DASH/USDT	26
BNB/USDT	25
EOS/USDT	22
BTC/NGN		21
LTC/USDT	18
```

aggtrades data
```
[
  {
    "a": 26129,         // Aggregate tradeId
    "p": "0.01633102",  // Price
    "q": "4.70443515",  // Quantity
    "f": 27781,         // First tradeId
    "l": 27781,         // Last tradeId
    "T": 1498793709153, // Timestamp
    "m": true,          // Was the buyer the maker?
    "M": true           // Was the trade the best price match?
  }
]

Kline/Candlestick data
[
  [
    1499040000000,      // Open time
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore.
  ]
]
```
