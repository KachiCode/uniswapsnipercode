from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime, date
import subprocess
import statistics
import requests

now = datetime.now()
datenow = date(now.year, now.month, now.day)

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  
  'limit':'4800',
  'sort' : 'date_added',
  'sort_dir' : 'desc'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '',
}



session = Session()
session.headers.update(headers)


def sendmessage_totelegram(message):

    TOKEN = ""
    chat_id = ""

    message_to_send = message
    print(message)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message_to_send}"
    print(requests.get(url).json()) # this sends the message

def sendmessage_totelegram_trendingcoin(message):

    TOKEN = ""
    chat_id = ""

    message_to_send = message
    print(message)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message_to_send}"
    print(requests.get(url).json()) # this sends the message


def format(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000}M'
        return f'{round(num / 1000000, 1)}M'
    return f'{num // 1000}K'

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)



for x in data["data"]:
  x["market_cap"] = x["quote"]["USD"]["market_cap"]
  x["volume"] = x["quote"]["USD"]["volume_24h"]
  x["price"] = x["quote"]["USD"]["price"]

crypto_dict = {}
crypto_dict_volume = {}
for x in data["data"]:
  crypto_dict[str(x["id"])] =  {k: x[k] for k in ('name', 'symbol', 'date_added','market_cap','volume','price')}
  

### Get previous prices
with open(r"/home/bice/Desktop/test/uniswapsniper/data.json") as json_file:
    prev_volumes = json.load(json_file)





for x in crypto_dict:

  name = crypto_dict[x]['name']
  market_cap = crypto_dict[x]['market_cap']
  volume = crypto_dict[x]['volume']

  if (market_cap > 90000000) or (market_cap < 40000):
    continue
  

  if x in prev_volumes:
    
    prev_volumes_list = prev_volumes[x]

    if len(prev_volumes_list) < 5:
      prev_volumes_list.append(volume)
      prev_volumes[x] = prev_volumes_list
      continue




    stdev = statistics.stdev(prev_volumes_list)
    median = statistics.median(prev_volumes_list)
    difference = (volume - median)
    crypto_dict[x]['difference'] = difference
    crypto_dict[x]['stdev'] = stdev
    if ((difference) > 5000000) & (stdev < 1000000):

      message_to =  "Name: " + name + " Market_cap:" + str(market_cap) + " Volume: " + str(format(volume)) + " Increase in volume: " + str(format(difference))
      sendmessage_totelegram_trendingcoin(message_to)
      

    prev_volumes_list.append(volume)
    prev_volumes[x] = prev_volumes_list[-5:]

  else:
    prev_volumes[x] = [volume]



crypto_dict_top_gainers = {k: crypto_dict[k] for k in crypto_dict if 'difference' in crypto_dict[k] and 'stdev' in crypto_dict[k]}
if len(crypto_dict_top_gainers)>0:
  crypto_dict_top_gainers_reduced = {k: crypto_dict[k] for k in crypto_dict_top_gainers if (crypto_dict_top_gainers[k]['stdev'] < 1000000)  }

  sorted_top_gainers = sorted(crypto_dict_top_gainers_reduced.items(), key=lambda item: item[1]['difference'], reverse=True)[:3]
  top_gainers_final = dict(sorted_top_gainers)
  
  message_to = ''

  for x in top_gainers_final:
    name = top_gainers_final[x]['name']
    volume = top_gainers_final[x]['volume']
    difference = top_gainers_final[x]['difference']
    message_to +=  "Name: " + name + " Market_cap:" + str(market_cap) + " Volume: " + str(format(volume)) + " Increase in volume: " + str(format(difference)) + "%0A"
  sendmessage_totelegram(message_to)



timestamp_dict = {}

timestamp_dict['timestamp'] = now.strftime("%m/%d/%Y, %H:%M:%S")




with open(r"/home/bice/Desktop/test/uniswapsniper/data.json", 'w') as fp:
    json.dump(prev_volumes, fp)

with open(r"/home/bice/Desktop/test/uniswapsniper/timestamp.json", 'w') as fp:
    json.dump(timestamp_dict, fp)



print("Succesful")


# repository_path = 'cd /home/hilmi/Desktop/Project/cryptotrackerdata && git add . '
# add_command = 'git add .'
# commit_command = 'git commit -m "Update Data"'
# git_push_command = 'git push'

# ls_command = 'ls'

# combined_command = (
#     'cd /home/hilmi/Desktop/Project/cryptotrackerdata && '
#     'git add . && '
#     'git commit -m "Update Data" && '
#     'git push'
# )


# combined_command_string = 'cd /home/hilmi/Desktop/Project/cryptotrackerdata && git add . && git commit -m "Update Data" && git push'

# try:
#      # Change the current working directory to the repository path
#      result1 = subprocess.run(combined_command_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#      print("Command:", combined_command_string)
#      print("Standard Output:")
#      print(result1.stdout)
#      print("Standard Error:")
#      print(result1.stderr)
#      print("Return Code:", result1.returncode)
#      print("=" * 30)
#      subprocess.check_call(['cd', repository_path], shell=True)
# except subprocess.CalledProcessError:
#      print("Failed to change directory to the repository path.")
#      exit(1)

# try:
#     # Change the current working directory to the repository path
#     result0 = subprocess.run(ls_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     print("Command:", ls_command)
#     print("Standard Output:")
#     print(result0.stdout)
#     print("Standard Error:")
#     print(result0.stderr)
#     print("Return Code:", result0.returncode)
#     print("=" * 30)
#     subprocess.check_call(['cd', repository_path], shell=True)
# except subprocess.CalledProcessError:
#     print("Failed to change directory to the repository path.")
#     exit(1)

# try:
    
#     result2 = subprocess.run(add_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     print("Command:", add_command)
#     print("Standard Output:")
#     print(result2.stdout)
#     print("Standard Error:")
#     print(result2.stderr)
#     print("Return Code:", result2.returncode)
#     print("=" * 30)
# except subprocess.CalledProcessError:
#     print("Failed to add files.")
#     exit(1)

# try:
#     result3 = subprocess.run(commit_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     print("Command:", commit_command)
#     print("Standard Output:")
    
#     print(result3.stdout)
#     print("Standard Output:")
#     print(result3.stdout)
#     print("Standard Error:")
#     print(result3.stderr)
#     print("Return Code:", result3.returncode)
#     print("=" * 30)
# except subprocess.CalledProcessError:
#     print("Failed to commit files.")
#     exit(1)

# try:
#     result4 = subprocess.run(git_push_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     print("Command:", git_push_command)
#     print("Standard Output:")
#     print(result4.stdout)
#     print("Standard Output:")
#     print(result4.stdout)
#     print("Standard Output:")
#     print(result4.stdout)
#     print("Standard Error:")
#     print(result4.stderr)
#     print("Return Code:", result4.returncode)
#     print("=" * 30)
# except subprocess.CalledProcessError:
#     print("Failed to push files.")
#     exit(1)
