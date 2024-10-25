import asyncio
import json
import requests
from web3 import Web3
from websockets import connect
from datetime import datetime
import time
import json

infura_ws_url = ''
infura_http_url = ''
w3 = Web3(Web3.HTTPProvider(infura_http_url))

counter = 0
data_list = []

TOKEN = "6682596858:"
chat_id = "6390066260"

message = "Start crawling ethereum blockchain"
print(message)
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
print(requests.get(url).json()) # this sends the message
# Used if you want to monitor ETH transactions to a specific address
for i in range(18676419, 18676419-216000, -1):
    # Your code here
    print(i)
    print('counter: ', counter)
    transactions = w3.eth.get_block(i,full_transactions=True)['transactions']
    

    for x in transactions:
        my_dict = dict(x)
        
        if 'input' in my_dict:
            transaction_input = my_dict['input'].hex()
            transaction_nonce = my_dict['nonce']
            transaction_index = my_dict['transactionIndex']
            transaction_to = my_dict['to']
            transaction_blocknumber = my_dict['blockNumber']
            if ((transaction_index == 0) or (transaction_index == 1)) and (transaction_input.startswith('0xc9567bf9') or transaction_input.startswith('0x93bf5705')):
                new_dict = {}
                new_dict['input'] = transaction_input
                new_dict['nonce'] = transaction_nonce
                new_dict['transactionIndex'] = transaction_index
                new_dict['to'] = transaction_to
                new_dict['blockNumber'] = transaction_blocknumber
                data_list.append(new_dict)
                print(data_list)
                counter +=1

            
save_dict = {}
save_dict['data'] = data_list
with open(r'C:\Users\Hilmi\Desktop\Development\uniswapv2thegraph\addresses.json', 'w') as fp:
          json.dump(save_dict, fp)        

            

print("Counter: ", counter)   
print("Finished")

message = "Crawling ended"
print(message)
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"