import json
import re

import numpy as np
import os
import time

from envbash import load_envbash

# run the config variables set script
from setuptools.command.test import test

CONFIG_FILENAME = 'config'
if not os.path.isfile('%s' % CONFIG_FILENAME):
    print('config file named \'%s\' not found' % CONFIG_FILENAME)
    exit(10)
load_envbash(CONFIG_FILENAME)

input_file_dir = os.environ['datafolder']
if not os.path.exists(input_file_dir):
    print('input_file_dir does not exist or is not configured: \'%s\'' % input_file_dir)
    exit(10)

output_file_dir = os.environ['output_file_dir']
if not os.path.exists(output_file_dir):
    print('output_file_dir does not exist or is not configured: \'%s\'' % output_file_dir)
    exit(10)

currency_pairs = os.environ['pairs'].split(" ")

start_time = time.time()

# target_futures_seconds = 60  # how many seconds in the future of the depth should the target be
# target_amount_of_trades = 100

# get all files
all_files = os.listdir(input_file_dir)
all_files.sort()

output_data = []
for currency_pair in currency_pairs:
    trades_files = [x for x in all_files if 'aggtrades' + currency_pair in x]
    depth_files = [x for x in all_files if 'depth' + currency_pair in x]

    if len(trades_files) == 0:
        continue
    file_date = re.search(r"(\d+\.\d+\.\d+)", trades_files[0]).group()
    print('working on %s' % (file_date + currency_pair))

    # read the input files and put the relevant values in a 2d matrix output_data and write it out
    for i in range(0, len(trades_files) - 1):
        timestamp = ''
        # bids = ''
        # asks = ''
        depthfilename = input_file_dir + os.path.sep + depth_files[i]
        with open(depthfilename) as json_file:
            depth = json.load(json_file)
            json_file.close()
        timestamp = int(depth['lastUpdateId'])
        bids = np.array(depth['bids']).astype(np.float)
        asks = np.array(depth['asks']).astype(np.float)

        # get the trades_files
        tradesfilename = input_file_dir + os.path.sep + trades_files[i]
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
        # print(output_data_entry)

        output_data.append(output_data_entry)

    # write fused data to csv file
    print(file_date)
    output_file_name = output_file_dir + os.path.sep + file_date + currency_pair + '.csv'
    print('saving file to %s' % output_file_name)
    np.savetxt(output_file_name, output_data, delimiter=',')

# enrich step
# TODO add prices for 5,10,..,60minutes,4h,12h,24h,7d,30d,1y - do this in a normalize step
# TODO do normalization operations to bids, asks, trades here

print('execution time : %s' % (time.time() - start_time))
