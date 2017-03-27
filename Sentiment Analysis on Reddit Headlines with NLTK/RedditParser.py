import requests
import json
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

# Set your header according to the form below
# <platform>:<app ID>:<version string> (by /u/<reddit username>)

# Add your username below
hdr = {'User-Agent': 'windows:r/politics.single.result:v1.0' +
       '(by /u/<YOURUSERNAME>)'}
url = 'https://www.reddit.com/r/politics/.json'
req = requests.get(url, headers=hdr)
json_data = json.loads(req.text)

# Uncomment the next line to enable pretty print of JSON file
# posts = json.dumps(json_data['data']['children'], indent=4, sort_keys=True)

data_all = json_data['data']['children']
num_of_posts = 0
while len(data_all) <= 100:
    time.sleep(2)
    last = data_all[-1]['data']['name']
    url = 'https://www.reddit.com/r/politics/.json?after=' + str(last)
    req = requests.get(url, headers=hdr)
    data = json.loads(req.text)
    data_all += data['data']['children']
    if num_of_posts == len(data_all):
        break
    else:
        num_of_posts = len(data_all)

sia = SIA()
pos_list = []
neg_list = []
for post in data_all:
    res = sia.polarity_scores(post['data']['title'])
    # Uncomment the following line to get the polarity results
    # for each post as shown in article's image
    # print(res)
    if res['compound'] > 0.2:
        pos_list.append(post['data']['title'])
    elif res['compound'] < -0.2:
        neg_list.append(post['data']['title'])

with open("pos_news_titles.txt", "w", encoding='utf-8',
          errors='ignore') as f_pos:
    for post in pos_list:
        f_pos.write(post + "\n")

with open("neg_news_titles.txt", "w", encoding='utf-8',
          errors='ignore') as f_neg:
    for post in neg_list:
        f_neg.write(post + "\n")
