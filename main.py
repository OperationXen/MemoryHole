import os
import sys
import re
from time import sleep
from datetime import datetime

import praw
import requests


next_link_regex = '\"next-button.+https:\/\/old\.reddit\.com\/r\/ukpolitics\/\?count=([\d]+).+after=([\S]+)\"'

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"})

agent = "linux:memory_hole:0.1"
client_id = sys.argv[1]
client_secret = sys.argv[2]

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=agent)

terminate = False
response = session.get('https://old.reddit.com/r/ukpolitics/')
while terminate == False:
    sleep(3)
    try:
        result = re.search(next_link_regex, str(response.content))
        next_offset = result.group(2)
    except:
        exit(1)
    response = session.get(f"https://old.reddit.com/r/ukpolitics/?count=100&after={next_offset}")
    [_, identifier] = next_offset.split('_')
    submission = reddit.submission(id=identifier)
    submission_date = datetime.utcfromtimestamp(submission.created).strftime('%Y-%m-%d %H:%M:%S')
    print(f"{next_offset}, {submission_date}, {submission.title}")