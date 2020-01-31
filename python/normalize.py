import json
import numpy as np
import os

input_file_dir = '/home/tensor/binance/devdata/'
output_file_dir = '/home/tensor/binance/devnormalizedata/'

# target_futures_seconds = 60  # how many seconds in the future of the depth should the target be
# target_amount_of_trades = 100

# get all files
all_files = os.listdir(input_file_dir)
all_files.sort()

# get the trades_files
trades_files = [x for x in all_files if 'aggtrades' in x]
depth_files = [x for x in all_files if 'depth' in x]

# read the input files and put the relevant values in a 2d matrix output_data and write it out
output_data = []
for i in range(0, len(trades_files) - 1):
    timestamp = ''
    bids = ''
    asks = ''
    depthfilename = input_file_dir + depth_files[i]
    with open(depthfilename) as json_file:
        depth = json.load(json_file)
        json_file.close()
    timestamp = int(depth['lastUpdateId'])
    bids = np.array(depth['bids']).astype(np.float)
    asks = np.array(depth['asks']).astype(np.float)

    tradesfilename = input_file_dir + trades_files[i]
    with open(tradesfilename) as json_file1:
        trades_raw = json.load(json_file1)
        json_file1.close()
    # get the price and the quantity as pairs like bid and ask entries
    pick_price_quantity = lambda trade: (trade['p'], trade['q'])
    trades = np.array([pick_price_quantity(p) for p in trades_raw]).astype(np.float)
    # print(trades)

    # prepare csv output data
    output_data_entry = np.array(timestamp)  # timestamp
    output_data_entry = np.append(output_data_entry, bids)  # bids
    output_data_entry = np.append(output_data_entry, asks)  # asks
    output_data_entry = np.append(output_data_entry, trades)  # trades

    # calculate average price
    # pick_price = lambda trade: trade['p']
    # price_array = np.array([pick_price(p) for p in trades_raw]).astype(np.float).astype(np.float)
    # price_avg = np.average(price_array)
    # output_data_entry = np.append(output_data_entry, price_avg)  # target
    print(output_data_entry)

    output_data.append(output_data_entry)

# write fused data to csv file
np.savetxt(output_file_dir+'fused.csv', output_data, delimiter=',')

# enrich step
# TODO add prices for 5,10,..,60minutes,4h,12h,24h,7d,30d,1y - do this in a normalize step
# TODO do normalization operations to bids, asks, trades here
# TODO calculate target value
